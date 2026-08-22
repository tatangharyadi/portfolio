#!/usr/bin/env python3
"""Deterministic text metrics for the ghostwriter plugin.

Computes the countable numbers that profile/editor SKILL.md previously asked
the model to count by eye: sentence-length stats, paragraph-length stats,
contraction rate, vocabulary richness (MATTR, MTLD), shared-opener runs, and rhythm runs.

Usage: python3 text_metrics.py <path-to-text-file>
Prints a single JSON object to stdout. Does not judge voice, tone, ornament,
or anything requiring language understanding -- those stay in the model's
hands, this only replaces counting.
"""
import base64
import binascii
import difflib
import json
import re
import sys
import unicodedata

CONTRACTION_RE = re.compile(
    r"\b\w+'(t|s|re|ve|ll|d|m)\b", re.IGNORECASE
)

# expandable phrase -> nothing; just used as a lookup of "could have contracted"
EXPANDABLE_PHRASES = [
    "do not", "does not", "did not", "is not", "are not", "was not", "were not",
    "have not", "has not", "had not", "will not", "would not", "could not",
    "should not", "cannot", "can not", "must not", "might not",
    "i am", "you are", "he is", "she is", "it is", "we are", "they are",
    "i have", "you have", "we have", "they have",
    "i will", "you will", "he will", "she will", "it will", "we will", "they will",
    "i would", "you would", "he would", "she would", "we would", "they would",
    "let us", "who is", "who are", "there is", "there are", "that is",
    "what is", "here is", "here are",
]
EXPANDABLE_RE = re.compile(
    r"\b(" + "|".join(p.replace(" ", r"\s+") for p in EXPANDABLE_PHRASES) + r")\b",
    re.IGNORECASE,
)

SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'])")
WORD_RE = re.compile(r"[A-Za-z']+")


HEADING_RE = re.compile(r"^#{1,6}\s.*$", re.MULTILINE)

# Cap on the (prefix/suffix-trimmed) span diffed in _normalization_drift.
# difflib.SequenceMatcher with autojunk=False runs up to cubic on long,
# densely-repetitive divergent input -- measured ~0.3s at 1000 chars in the
# worst case (a string where nearly every position mismatches), so this
# stays well under a second even there. Real drift regions are far smaller
# once trimmed, so this ceiling is rarely reached in practice.
_DRIFT_DIFF_LIMIT = 1000

# Characters with no legitimate reason to appear in typed prose -- zero-width
# spacing/joining marks, a mid-file byte-order mark, variation selectors (used
# by some LLM-watermarking schemes to encode hidden bits), and deprecated
# invisible separators. Finding any of these is a technical defect, not a
# style judgment -- unlike NBSP or curly quotes below, which are ordinary
# characters a human could type deliberately.
ZERO_WIDTH_CHARS = {
    "​": "ZERO WIDTH SPACE",
    "‌": "ZERO WIDTH NON-JOINER",
    "‍": "ZERO WIDTH JOINER",
    "⁠": "WORD JOINER",
    "﻿": "ZERO WIDTH NO-BREAK SPACE (BOM)",
    "᠎": "MONGOLIAN VOWEL SEPARATOR",
    "͏": "COMBINING GRAPHEME JOINER",
}
# Categories emoji pictographs and modifiers fall into -- used to recognize a
# ZERO WIDTH JOINER that's stitching two emoji into one glyph (e.g. the family
# or profession emoji sequences) rather than smuggling a hidden payload.
_EMOJI_LIKE_CATEGORIES = {"So", "Sk"}


def _is_emoji_like(ch):
    return bool(ch) and unicodedata.category(ch) in _EMOJI_LIKE_CATEGORIES


_VARIATION_SELECTOR_SKIP = {"︎", "️"}


def _nearest_emoji_neighbor(text, i, step):
    """Walk from i in `step` direction, skipping presentation variation
    selectors (U+FE0E/FE0F), and report whether the first substantive
    character found is emoji-like. Real ZWJ emoji sequences like the
    rainbow flag (U+1F3F3 U+FE0F U+200D U+1F308) put a variation selector
    between the base emoji and the joiner, so a naive immediate-neighbor
    check misses them."""
    j = i + step
    while 0 <= j < len(text) and text[j] in _VARIATION_SELECTOR_SKIP:
        j += step
    return _is_emoji_like(text[j]) if 0 <= j < len(text) else False


def _find_zwj_hits(text):
    """Positions of ZERO WIDTH JOINER not sandwiched between two emoji."""
    return [
        i for i, ch in enumerate(text)
        if ch == "‍"
        and not (
            _nearest_emoji_neighbor(text, i, -1)
            and _nearest_emoji_neighbor(text, i, 1)
        )
    ]
# U+FE0F (VARIATION SELECTOR-16) is excluded: it's the ordinary emoji
# presentation selector and appears any time typed prose quotes an emoji, so
# including it produces false positives unrelated to watermarking.
VARIATION_SELECTOR_RE = re.compile(r"[\U0000FE00-\U0000FE0E\U000E0100-\U000E01EF]")

# Explicit bidirectional-formatting controls (embed/override/isolate, plus the
# Arabic Letter Mark) -- these have no reason to appear in typed prose and are
# a known hidden-payload vector (bidi smuggling), same class of defect as the
# zero-width characters above.
BIDI_CONTROL_RE = re.compile(r"[؜‪-‮⁦-⁩]")

# Invisible math operators (function application, invisible times/plus,
# invisible separator) -- adjacent to the word-joiner codepoint above but a
# separate block, with no legitimate reason to appear in prose.
INVISIBLE_OPERATOR_RE = re.compile(r"[⁡-⁤]")

# Unicode tag characters -- originally for subdividing flag emoji, but also a
# documented "ASCII smuggling" vector where arbitrary hidden ASCII text is
# encoded on tag codepoints and rides invisibly inside otherwise normal text.
TAG_CHARS_RE = re.compile(r"[\U000E0001\U000E0020-\U000E007F]")

# A legitimate use of tag characters: subdivision flag emoji (e.g. Scotland,
# Wales, England) are a black-flag base followed by tag chars spelling the
# region code and closing with a cancel tag. Strip these before counting
# TAG_CHARS_RE hits so a human typing one of these flags does not fail the
# zero-tolerance gate below.
FLAG_TAG_SEQUENCE_RE = re.compile(r"\U0001F3F4[\U000E0020-\U000E007A]*\U000E007F")

# Ordinary characters a human could type or introduce deliberately -- exotic
# spacing from word processors and copy-paste, plus soft hyphen, which arrives
# routinely from `&shy;` in HTML, word-processor hyphenation, and PDF text
# extraction. Reported as a count, not treated as a defect on its own.
EXOTIC_SPACE_CHARS = {
    " ": "NO-BREAK SPACE",
    " ": "OGHAM SPACE MARK",
    " ": "EN QUAD",
    " ": "EM QUAD",
    " ": "EN SPACE",
    " ": "EM SPACE",
    " ": "THREE-PER-EM SPACE",
    " ": "FOUR-PER-EM SPACE",
    " ": "SIX-PER-EM SPACE",
    " ": "FIGURE SPACE",
    " ": "PUNCTUATION SPACE",
    " ": "THIN SPACE",
    " ": "HAIR SPACE",
    " ": "NARROW NO-BREAK SPACE",
    " ": "MEDIUM MATHEMATICAL SPACE",
    "　": "IDEOGRAPHIC SPACE",
    "­": "SOFT HYPHEN",
}

# Scripts that commonly supply homoglyphs for Latin text -- a Cyrillic or
# Greek letter substituted into an otherwise-Latin word is invisible at a
# glance but a distinct hidden-data channel from anything above (it hides in
# plain sight rather than being literally unrenderable).
_HOMOGLYPH_SCRIPTS = ("CYRILLIC", "GREEK")
_WORD_CHARS_RE = re.compile(r"\w{2,}", re.UNICODE)


def _script_of(ch):
    try:
        name = unicodedata.name(ch)
    except ValueError:
        return None
    for script in ("LATIN",) + _HOMOGLYPH_SCRIPTS:
        if name.startswith(script + " "):
            return script
    return None


def _mixed_script_words(text):
    """Words that mix Latin with a commonly-confused script (Cyrillic/Greek)."""
    seen = set()
    hits = []
    for word in _WORD_CHARS_RE.findall(text):
        scripts = {s for s in (_script_of(ch) for ch in word) if s}
        if len(scripts) > 1 and word not in seen:
            seen.add(word)
            hits.append({"word": word, "scripts": sorted(scripts)})
    return hits


# Codepoint ranges already classified by a specific check above (including
# U+FE0F, deliberately exempted from VARIATION_SELECTOR_RE as the ordinary
# emoji presentation selector). The generic Cf/Cc fallback below must treat
# these as handled too, or it would re-flag the very codepoints those checks
# already report -- or, for FE0F, defeat the emoji carve-out.
def _already_classified(cp):
    if chr(cp) in ZERO_WIDTH_CHARS:
        return True
    if 0xFE00 <= cp <= 0xFE0F or 0xE0100 <= cp <= 0xE01EF:
        return True
    if cp == 0x061C or 0x202A <= cp <= 0x202E or 0x2066 <= cp <= 0x2069:
        return True
    if 0x2061 <= cp <= 0x2064:
        return True
    if cp == 0xE0001 or 0xE0020 <= cp <= 0xE007F:
        return True
    return False


def _unclassified_control_hits(text):
    """Fallback net: any Cf/Cc character not already handled by a specific
    check above, plus any Private Use Area codepoint (category Co --
    U+E000-F8FF and the two supplementary PUA planes). PUA codepoints have
    no assigned meaning and no legitimate reason to appear in typed prose;
    they're a documented hidden-payload vector same as tag characters, and
    -- unlike Cf/Cc -- category Co isn't a format/control character, so it
    would otherwise slip past this fallback net entirely uncaught. Both
    halves are a LOW-severity signal, same footing as an exotic space, not a
    defect on their own."""
    counts = {}
    contexts = {}
    for i, ch in enumerate(text):
        if ch in "\n\r\t":
            continue
        cp = ord(ch)
        if _already_classified(cp):
            continue
        category = unicodedata.category(ch)
        is_pua = (
            0xE000 <= cp <= 0xF8FF
            or 0xF0000 <= cp <= 0xFFFFD
            or 0x100000 <= cp <= 0x10FFFD
        )
        if category in ("Cf", "Cc") or is_pua:
            counts[cp] = counts.get(cp, 0) + 1
            contexts.setdefault(cp, text[max(0, i - 20):i + 20].replace("\n", " "))
    return [
        {
            "char": f"U+{cp:04X}",
            "name": unicodedata.name(chr(cp), "UNNAMED"),
            "count": count,
            "context": contexts[cp],
        }
        for cp, count in sorted(counts.items())
    ]


# A run long enough to plausibly be an encoded payload rather than a coincidental
# run of alphanumerics -- 24+ base64-alphabet characters (6 groups of 4) or 32+
# hex characters. Both thresholds are deliberately loose; this is a candidate
# signal for a human to look at, not a decoder, so it should over-report rather
# than miss a real payload.
_BASE64_CANDIDATE_RE = re.compile(r"(?:[A-Za-z0-9+/]{4}){6,}(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?")
_HEX_CANDIDATE_RE = re.compile(r"\b[0-9a-fA-F]{32,}\b")


def _decoded_preview(candidate):
    """Try to decode a base64 candidate and confirm it's mostly-printable text,
    not just alphanumerics that happen to be a multiple of 4 long. Returns the
    decoded preview string, or None if it doesn't decode to plausible content."""
    try:
        raw = base64.b64decode(candidate, validate=True)
    except (ValueError, binascii.Error):
        return None
    if not raw:
        return None
    try:
        decoded = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None
    printable = sum(1 for c in decoded if c.isprintable() or c in "\n\r\t")
    if printable / len(decoded) < 0.9:
        return None
    return decoded[:80]


def _encoded_payloads(text):
    """Runs of characters that could be a Base64- or hex-encoded hidden
    payload riding inside otherwise ordinary prose -- a smuggling channel a
    codepoint-by-codepoint scan can't see, since every character involved is
    plain ASCII. Reported as a count, not treated as a defect on its own: a
    git commit SHA, a UUID, or a legitimate short code quoted in the text
    will also match this pattern, so a hit here is a candidate for a human
    to look at, not proof of a hidden payload -- only a Base64 candidate
    that actually decodes to printable text is reported with a preview;
    hex candidates are reported as-is since decoding tells us nothing about
    their content."""
    hits = []
    seen_spans = set()
    for m in _BASE64_CANDIDATE_RE.finditer(text):
        candidate = m.group(0)
        if len(candidate) < 24:
            continue
        preview = _decoded_preview(candidate)
        if preview is None:
            continue
        span = m.span()
        seen_spans.add(span)
        hits.append({
            "type": "base64",
            "match": candidate[:40] + ("..." if len(candidate) > 40 else ""),
            "decoded_preview": preview,
            "context": text[max(0, span[0] - 20):span[1] + 20].replace("\n", " "),
        })
    for m in _HEX_CANDIDATE_RE.finditer(text):
        span = m.span()
        if span in seen_spans:
            continue
        hits.append({
            "type": "hex",
            "match": m.group(0)[:40] + ("..." if len(m.group(0)) > 40 else ""),
            "decoded_preview": None,
            "context": text[max(0, span[0] - 20):span[1] + 20].replace("\n", " "),
        })
    return hits


def _normalization_drift(text):
    """Compare the text against its NFC and NFKC normalized forms. A
    mismatch means some characters are riding as decomposed combining
    sequences or compatibility-equivalent codepoints rather than their
    ordinary composed form -- a Unicode-level substitution a plain
    codepoint scan for specific known characters wouldn't catch. Reported
    as a count, not treated as a defect on its own: legitimate text
    normalizes non-identically too (e.g. an accented letter typed as
    base+combining-mark, or certain CJK/full-width punctuation under
    NFKC), so this is a candidate for a human to look at, not proof of
    tampering. SequenceMatcher with autojunk=False (needed here since
    autojunk would silently junk frequent characters on sequences over 200
    elements, wrecking character-level matching on normal prose) runs up
    to cubic on long, densely-repetitive divergent spans -- a draft with
    heavy decomposed accents (e.g. a macOS paste, or French/Vietnamese
    content) can otherwise hang for minutes. Trimming the matching
    prefix/suffix first collapses the realistic case (a handful of
    decomposed characters in otherwise-composed prose) to a near-instant
    diff; _DRIFT_DIFF_LIMIT then caps the remaining span so even a
    pathologically repetitive divergence (which trimming alone can't
    shrink, since every position differs) stays fast."""
    results = {}
    for form in ("NFC", "NFKC"):
        normalized = unicodedata.normalize(form, text)
        if normalized == text:
            results[form] = {"drift": False, "count": 0, "context": None}
            continue
        shorter = min(len(text), len(normalized))
        prefix = 0
        while prefix < shorter and text[prefix] == normalized[prefix]:
            prefix += 1
        suffix = 0
        while (suffix < shorter - prefix
               and text[len(text) - 1 - suffix] == normalized[len(normalized) - 1 - suffix]):
            suffix += 1
        mid_text = text[prefix:len(text) - suffix]
        mid_normalized = normalized[prefix:len(normalized) - suffix]
        context = text[max(0, prefix - 20):prefix + 20].replace("\n", " ")
        if max(len(mid_text), len(mid_normalized)) > _DRIFT_DIFF_LIMIT:
            results[form] = {
                "drift": True,
                "count": None,
                "context": context,
                "truncated": True,
            }
            continue
        matcher = difflib.SequenceMatcher(None, mid_text, mid_normalized, autojunk=False)
        diffs = [op for op in matcher.get_opcodes() if op[0] != "equal"]
        results[form] = {
            "drift": True,
            "count": len(diffs),
            "context": context,
        }
    return results if any(v["drift"] for v in results.values()) else {}


def watermark_scan(text):
    """Report invisible/hidden Unicode characters and smart-punctuation counts.

    Zero-width characters, a mid-file BOM, and variation selectors are
    reported separately from the exotic-space/dash/quote counts below because
    their presence is usually a technical artifact (often from copy-pasting
    AI output, sometimes a deliberate LLM watermark) rather than a stylistic
    choice -- with narrow, explicitly carved-out exceptions for genuine emoji
    ZWJ sequences, subdivision-flag tag sequences, and soft hyphens, which are
    filtered out above before a hit is counted here.
    """
    invisible_hits = []
    for ch, name in ZERO_WIDTH_CHARS.items():
        if ch == "‍":
            positions = _find_zwj_hits(text)
            if positions:
                idx = positions[0]
                invisible_hits.append({
                    "char": f"U+{ord(ch):04X}",
                    "name": name,
                    "count": len(positions),
                    "context": text[max(0, idx - 20):idx + 20].replace("\n", " "),
                })
            continue
        count = text.count(ch)
        if count:
            idx = text.index(ch)
            invisible_hits.append({
                "char": f"U+{ord(ch):04X}",
                "name": name,
                "count": count,
                "context": text[max(0, idx - 20):idx + 20].replace("\n", " "),
            })
    variation_selectors = len(VARIATION_SELECTOR_RE.findall(text))
    if variation_selectors:
        invisible_hits.append({
            "char": "U+FE00-FE0E / U+E0100-E01EF",
            "name": "VARIATION SELECTOR",
            "count": variation_selectors,
            "context": None,
        })

    bidi_controls = len(BIDI_CONTROL_RE.findall(text))
    if bidi_controls:
        invisible_hits.append({
            "char": "U+061C / U+202A-202E / U+2066-2069",
            "name": "BIDIRECTIONAL CONTROL",
            "count": bidi_controls,
            "context": None,
        })

    invisible_operators = len(INVISIBLE_OPERATOR_RE.findall(text))
    if invisible_operators:
        invisible_hits.append({
            "char": "U+2061-2064",
            "name": "INVISIBLE MATH OPERATOR",
            "count": invisible_operators,
            "context": None,
        })

    tag_chars = len(TAG_CHARS_RE.findall(FLAG_TAG_SEQUENCE_RE.sub("", text)))
    if tag_chars:
        invisible_hits.append({
            "char": "U+E0001 / U+E0020-E007F",
            "name": "UNICODE TAG (ASCII SMUGGLING)",
            "count": tag_chars,
            "context": None,
        })

    invisible_hits.extend(_unclassified_control_hits(text))

    exotic_spaces = {
        name: text.count(ch) for ch, name in EXOTIC_SPACE_CHARS.items() if text.count(ch)
    }

    return {
        "invisible_characters_found": invisible_hits,
        "exotic_spaces_found": exotic_spaces,
        "mixed_script_words_found": _mixed_script_words(text),
        "encoded_payloads_found": _encoded_payloads(text),
        "normalization_drift": _normalization_drift(text),
        # Double and single quote marks are reported separately -- pooling
        # them would let the apostrophe-heavy single-quote count (or the
        # attribute-heavy double-quote count in markup) drown out the other.
        # Each pair is still a meaningful ratio against itself: an
        # all-curly-apostrophe draft with no straight apostrophes suggests
        # auto-curl from a paste; a mix of both suggests multiple sources.
        "curly_double_quotes": text.count("“") + text.count("”"),
        "straight_double_quotes": text.count('"'),
        "curly_single_quotes": text.count("‘") + text.count("’"),
        "straight_single_quotes": text.count("'"),
        "em_dashes": text.count("—"),
        "en_dashes": text.count("–"),
    }


def split_paragraphs(text):
    text = HEADING_RE.sub("", text)
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def split_sentences(paragraph):
    flat = re.sub(r"\s+", " ", paragraph).strip()
    if not flat:
        return []
    parts = SENTENCE_SPLIT_RE.split(flat)
    return [p.strip() for p in parts if p.strip()]


def word_count(sentence):
    return len(WORD_RE.findall(sentence))


def contraction_stats(text):
    contractions = len(CONTRACTION_RE.findall(text))
    expandable = len(EXPANDABLE_RE.findall(text))
    total = contractions + expandable
    rate = contractions / total if total else None
    # With few or no expandable-phrase hits, the rate is dominated by (or
    # entirely derived from) the contraction count alone -- e.g. any text with
    # contractions and zero matched expandable phrases scores a trivial 1.0.
    # Flag it so callers don't present that as a measured baseline.
    low_confidence = expandable < 2
    return {
        "contractions_found": contractions,
        "expandable_forms_found": expandable,
        "contraction_rate": rate,
        "low_confidence": low_confidence,
    }


MATTR_WINDOW = 50
MTLD_TTR_THRESHOLD = 0.72
# Below this many tokens neither measure has enough room to be meaningful.
# 100 rather than the MATTR_WINDOW value itself: at exactly one window MATTR
# is just a single plain TTR wearing a moving-average label, not an average
# of several windows, and MTLD's own literature recommends the same ~100-token
# floor for its factor-counting math to stop degenerating. Below this, both
# report None and low_confidence rather than a number that looks precise but isn't.
MIN_WORDS_FOR_RICHNESS = 100


def mattr(words, window_size=MATTR_WINDOW):
    """Moving-Average Type-Token Ratio: mean TTR over all windows of `window_size`
    consecutive tokens, sliding one token at a time.

    Length-robust by construction (every window is the same size), unlike a
    single whole-text TTR or hapax rate, which shrink as a text grows. Higher
    means richer vocabulary. Returns None if the text is shorter than one
    window -- there's nothing to slide. In practice callers gate on the
    higher MIN_WORDS_FOR_RICHNESS floor (100 words) before reaching here, so
    this window-length check rarely fires through vocabulary_richness(); it's
    a direct-call safeguard, not the effective minimum.
    """
    n = len(words)
    if n < window_size:
        return None
    counts = {}
    for w in words[:window_size]:
        counts[w] = counts.get(w, 0) + 1
    ttrs = [len(counts) / window_size]
    for i in range(window_size, n):
        old = words[i - window_size]
        counts[old] -= 1
        if counts[old] == 0:
            del counts[old]
        new = words[i]
        counts[new] = counts.get(new, 0) + 1
        ttrs.append(len(counts) / window_size)
    return sum(ttrs) / len(ttrs)


def _mtld_factors(words, ttr_threshold):
    factors = 0
    types = set()
    token_count = 0
    for w in words:
        token_count += 1
        types.add(w)
        if len(types) / token_count <= ttr_threshold:
            factors += 1
            types = set()
            token_count = 0
    if token_count > 0:
        ttr = len(types) / token_count
        # Partial factor for the leftover tail that never dropped to
        # threshold -- proportional to how close it got.
        factors += (1 - ttr) / (1 - ttr_threshold)
    return len(words) / factors if factors > 0 else float(len(words))


def mtld(words, ttr_threshold=MTLD_TTR_THRESHOLD):
    """Measure of Textual Lexical Diversity: average token span needed for TTR
    to decay to `ttr_threshold`, computed forward and backward and averaged.

    Higher means richer vocabulary -- same direction as MATTR, unlike Yule's
    K in the measure this replaced. Returns None below MIN_WORDS_FOR_RICHNESS;
    the factor-counting math degenerates (too few/no resets) on short text.
    """
    if len(words) < MIN_WORDS_FOR_RICHNESS:
        return None
    forward = _mtld_factors(words, ttr_threshold)
    backward = _mtld_factors(list(reversed(words)), ttr_threshold)
    return (forward + backward) / 2


def vocabulary_richness(text):
    words = [w.lower() for w in WORD_RE.findall(text) if len(w) > 1 or w.isalpha()]
    total = len(words)
    distinct = len(set(words))
    low_confidence = total < MIN_WORDS_FOR_RICHNESS
    return {
        "total_words": total,
        "distinct_words": distinct,
        "mattr": None if low_confidence else mattr(words),
        "mattr_window": MATTR_WINDOW,
        "mtld": None if low_confidence else mtld(words),
        "low_confidence": low_confidence,
    }


def opener(sentence):
    words = WORD_RE.findall(sentence)
    return " ".join(w.lower() for w in words[:2])


def shared_opener_runs(sentences):
    """Runs of 3+ consecutive sentences (draft-wide) sharing a first word."""
    runs = []
    i = 0
    first_words = [WORD_RE.findall(s)[:1] for s in sentences]
    first_words = [w[0].lower() if w else "" for w in first_words]
    while i < len(sentences):
        j = i
        while j + 1 < len(sentences) and first_words[j + 1] == first_words[i] and first_words[i]:
            j += 1
        run_len = j - i + 1
        if run_len >= 3:
            runs.append({
                "opener": first_words[i],
                "count": run_len,
                "sentences": sentences[i:j + 1],
            })
        i = j + 1
    return runs


def rhythm_runs(sentences, window=5, min_run=3):
    """Runs of 3+ consecutive sentences whose word counts stay within `window`."""
    lengths = [word_count(s) for s in sentences]
    runs = []
    i = 0
    while i < len(sentences):
        j = i
        while (
            j + 1 < len(sentences)
            and max(lengths[i:j + 2]) - min(lengths[i:j + 2]) <= window
        ):
            j += 1
        run_len = j - i + 1
        if run_len >= min_run:
            runs.append({
                "count": run_len,
                "lengths": lengths[i:j + 1],
                "sentences": sentences[i:j + 1],
            })
        i = j + 1
    return runs


def analyze(text):
    paragraphs = split_paragraphs(text)
    all_sentences = []
    paragraph_reports = []

    for para in paragraphs:
        sentences = split_sentences(para)
        if not sentences:
            continue
        all_sentences.extend(sentences)
        lengths = [word_count(s) for s in sentences]
        c_stats = contraction_stats(para)
        paragraph_reports.append({
            "text_preview": para[:80],
            "sentence_count": len(sentences),
            "shortest_sentence_words": min(lengths),
            "longest_sentence_words": max(lengths),
            "avg_sentence_words": round(sum(lengths) / len(lengths), 1),
            "contraction_rate": c_stats["contraction_rate"],
            "contractions_found": c_stats["contractions_found"],
            "expandable_forms_found": c_stats["expandable_forms_found"],
        })

    sentence_lengths = [word_count(s) for s in all_sentences]
    sentence_lengths_sorted = sorted(sentence_lengths)
    n = len(sentence_lengths_sorted)
    median = (
        sentence_lengths_sorted[n // 2]
        if n % 2
        else (sentence_lengths_sorted[n // 2 - 1] + sentence_lengths_sorted[n // 2]) / 2
    ) if n else None

    para_sentence_counts = [p["sentence_count"] for p in paragraph_reports]

    return {
        "paragraph_count": len(paragraph_reports),
        "sentence_count": n,
        "sentence_length": {
            "shortest": min(sentence_lengths) if n else None,
            "median": median,
            "longest": max(sentence_lengths) if n else None,
        },
        "paragraph_length_in_sentences": {
            "shortest": min(para_sentence_counts) if para_sentence_counts else None,
            "longest": max(para_sentence_counts) if para_sentence_counts else None,
        },
        "contraction": contraction_stats(text),
        "vocabulary": vocabulary_richness(text),
        "watermark": watermark_scan(text),
        "paragraphs": paragraph_reports,
        "shared_opener_runs": shared_opener_runs(all_sentences),
        "rhythm_runs": rhythm_runs(all_sentences),
    }


def main():
    if len(sys.argv) != 2:
        print("usage: text_metrics.py <path-to-text-file>", file=sys.stderr)
        sys.exit(1)
    # utf-8-sig strips a leading BOM (an ordinary artifact of many editors/
    # exporters) so only a mid-file BOM -- the actual technical defect --
    # reaches watermark_scan's ZERO_WIDTH_CHARS check.
    with open(sys.argv[1], "r", encoding="utf-8-sig") as f:
        text = f.read()
    print(json.dumps(analyze(text), indent=2))


if __name__ == "__main__":
    main()
