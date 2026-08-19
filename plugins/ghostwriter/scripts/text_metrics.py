#!/usr/bin/env python3
"""Deterministic text metrics for the ghostwriter plugin.

Computes the countable numbers that profile/editor SKILL.md previously asked
the model to count by eye: sentence-length stats, paragraph-length stats,
contraction rate, hapax legomenon rate, shared-opener runs, and rhythm runs.

Usage: python3 text_metrics.py <path-to-text-file>
Prints a single JSON object to stdout. Does not judge voice, tone, ornament,
or anything requiring language understanding -- those stay in the model's
hands, this only replaces counting.
"""
import json
import re
import sys

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


def hapax_rate(text):
    words = [w.lower() for w in WORD_RE.findall(text) if len(w) > 1 or w.isalpha()]
    if not words:
        return {"distinct_words": 0, "hapax_words": 0, "hapax_rate": None}
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    distinct = len(freq)
    hapax = sum(1 for c in freq.values() if c == 1)
    return {
        "distinct_words": distinct,
        "hapax_words": hapax,
        "hapax_rate": hapax / distinct,
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
        "vocabulary": hapax_rate(text),
        "paragraphs": paragraph_reports,
        "shared_opener_runs": shared_opener_runs(all_sentences),
        "rhythm_runs": rhythm_runs(all_sentences),
    }


def main():
    if len(sys.argv) != 2:
        print("usage: text_metrics.py <path-to-text-file>", file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        text = f.read()
    print(json.dumps(analyze(text), indent=2))


if __name__ == "__main__":
    main()
