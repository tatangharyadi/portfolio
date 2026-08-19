---
name: editor
description: Grade a draft against writing/persona.md with a scored audit and hand back a prioritized fix list — does not rewrite; use the writer skill's revision mode to apply fixes
---

# Editor

Take a draft (from `writing/drafts/`, pasted text, or wherever the user points) and audit it
against `writing/persona.md`, as a skeptical outside reviewer with no stake in whether it
passes. This skill grades and hands back specific fixes — it does not rewrite the draft
itself; that's the `writer` skill's revision mode.

## Before auditing

Read `writing/persona.md` in full — the Imitation checklist, AI-tell checklist, the
`Ornament baseline: ...` line under `## Ornamentation`, and the `Contraction baseline: ...`
line under `## Punctuation` feed directly into the scored checks below. If it's missing,
stop and say the `profile` skill needs to run first.

Several checks below key off a specific persona.md field (a documented rate, a named quirk,
a baseline line). persona.md's field is always the primary source; editor's own number, where
one is stated, is a fallback that only fires when the field is genuinely absent — never a
default that persona merely overrides. When a fallback fires, name it in the fix list output
as a fallback, not a silent substitution.

Most of these fields (Sentence rhythm, Structure habits' paragraph length, Ornament baseline,
Contraction baseline) are required by `profile`'s own template, so their fallback should be
rare — treat it as a signal that a `profile` refresh may be overdue, not routine plumbing.
One exception: opener-repetition (sub-check 2 of Sentence rhythm & structure, below) has no
required field — `profile`'s Openings section is qualitative, not a mandated
repetition-quantifying line — so that particular fallback is expected to fire on any persona
that doesn't happen to document a repeated-opener habit. Don't flag it as a missing-field
signal; it's just the normal case for personas without that quirk.

Before scoring, run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/text_metrics.py <draft-file>`
against the draft (or a temp file holding pasted text). If `CLAUDE_PLUGIN_ROOT` is unset or
the path doesn't resolve, fall back to `$(git rev-parse --show-toplevel)/plugins/ghostwriter/scripts/text_metrics.py` —
resolve the repo root explicitly rather than assuming the current working directory is it.
It computes sentence-length stats,
paragraph-length-in-sentences, per-paragraph contraction rate and average sentence length,
overall contraction rate, hapax legomenon rate, shared-opener runs, and rhythm runs directly
from the text — the exact numbers several checks below ask for, without relying on the
model's own counting. Use its output as the ground truth for those numbers; everything
qualitative (whether a device recurs, whether a triad is disguised, whether a hedge reads as
AI-sounding) still needs the model's read of the actual prose, which the script can't judge.
If the script's output looks wrong on a specific paragraph (e.g. a mid-sentence quotation
confusing the sentence splitter), say so and fall back to a manual count for that paragraph
rather than trusting a bad split silently.

## Mindset

Run this audit as a skeptical editor reviewing someone else's submission, not as the author
reviewing their own work. Actively look for reasons to FAIL a check, not reasons to pass it —
if a check could reasonably go either way, mark it FAIL. Satisfying the letter of a check
while missing its intent (e.g. decorating a triad so it reads better without breaking the
underlying three-item skeleton) does not pass it. Every verdict needs evidence: a quote, a
count, or a named example — a bare score or claim with nothing under it is not acceptable
output. If you find yourself wanting to reclassify a sentence from ORNAMENTED to PLAIN, or a
check from FAIL to PASS, without the underlying wording having changed, don't — that's
rationalizing a pass, not evidence of one.

Skepticism cuts toward AI-tell patterns, not toward the writer's legitimate voice. Before
flagging any of the following, confirm it's a cluster of tells, not one instance mistaken
for the whole: polished, grammatically clean prose; mixed casual and formal registers within
one piece; plain or dry prose with none of the specific tells listed in the scored checks
below present; a single em
dash, a single hedge word, or one instance of an "overused" word used correctly; formal or
technical vocabulary the persona's own samples already show it using; a salutation or sign-
off; unsourced claims (most writing is unsourced — that alone proves nothing); a single
Wh-opener used as a genuine question rather than a rhetorical setup; one passive-voice
sentence where the actor is genuinely unknown or irrelevant to the point. Weigh these in
the writer's favor when deciding a borderline check:
- **Specific, hard-to-fabricate detail** (an exact place, a verbatim odd quote, a precise
  number) — AI writing rounds these off, so their presence is evidence of a real voice.
- **Mixed or unresolved feelings** stated plainly, rather than a tidy resolved take.
- **Uneven sentence rhythm** — genuine variety, not the padded-short/padded-long pattern a
  check might mistake for it.
- **A genuine aside, parenthetical, or self-correction mid-thought.**
Don't let this override a real hit — a single em dash that also completes a rule-of-three and
a hedge is still worth flagging — but don't manufacture a FAIL to satisfy the skeptical
mindset when the actual evidence is this thin.

## Hard gates — checked first, override everything else

If any gate fails, stop: the verdict is NEEDS REVISION, skip the numeric score below, and
go straight to the fix list in Output.

**Gate — Accuracy & integrity**
- No invented facts, statistics, names, or quotes presented as factual.
- Any fact needed but not supplied is marked `[PLACEHOLDER]`, not fabricated.
- If revising an existing draft: original meaning and facts are preserved.
- Fictional detail inside an intentionally fictional piece (character names, invented
  settings) does not trigger this gate — it's about claims presented as factual.
- Evidence: confirm every specific factual claim traces to the user's brief or a source, or
  is marked `[PLACEHOLDER]`. Any unmarked invention presented as fact = FAIL.

**Gate — Structural variety (triads)**
- Scan for any sentence built as three parallel clauses or items ("There was X...; Y...;
  and Z...", "She did A; she did B; she did C", "It was A. It was B. It was C.", "not only
  X, but also Y, and ultimately Z").
- A triad stays a triad even when each item carries its own descriptive clause, or when
  connector/ordinal words are inserted between items ("next," "then," "finally," "first...
  second... third"). Judge by the underlying X; Y; and Z skeleton, not the decoration.
- If the draft explicitly names the device it's using ("the sacred triad," "the trilogy
  of," "three truths"), count that as a confirmed triad regardless of how it reads.
- Zero-tolerance: even a single confirmed triad FAILS this gate, no partial credit — this
  has been the most recurring failure across drafts.
- Evidence: quote every triad found in full, including decorated or connector-disguised
  ones. State the count explicitly — "0 triads found" if none, don't skip this silently.

**Gate — Device density**
- Count how many of the draft's paragraphs use the same structural device — a
  build-then-puncture beat, a paired A-vs-B contrast, a repeated-opener escalation —
  regardless of whether persona.md documents that device as this person's habit.
- persona.md documents a device qualitatively (that it happens), never a rate (how often); a
  device the persona legitimately claims still fails this gate once it appears in a majority
  of the draft's paragraphs, because real human writing doesn't lean on one favorite move in
  most paragraphs of a single piece. A device present in a minority of paragraphs is voice;
  the same device in a majority is architecture.
- This started as a weighted sub-check under Sentence rhythm & structure and was promoted to
  a gate: a maximal hit there could only zero out that check's 10-point weight, which left a
  draft that was otherwise clean at 90/100 — still READY. A whole-piece structural problem
  needs gate treatment, the same as triads, not a share of one weighted check.
- Zero-tolerance once the majority threshold is crossed: no partial credit for an otherwise
  strong draft.
- Evidence: count paragraphs using the device against total paragraphs, and quote at least
  two instances of the device recurring. State the fraction explicitly even if it's 0 of N.

## Scored checks (only if all gates pass)

Score each 1 (fully present) / 0.5 (partial) / 0 (absent), with quoted evidence. Weights sum
to 100:

- **Sentence rhythm & structure** — weight 10. Six sub-checks; each is either a
  persona-sourced measurement (read persona.md's actual documented value, don't substitute
  editor's own number) or a generic AI-tell (applies regardless of persona, editor's own
  rule). Score: 1 if none of the six hit; 0.5 if exactly one hits in isolation; 0 if two or
  more hit, or any single one hits as a sustained pattern rather than a one-off.
  1. **Short/long-sentence rate — persona-sourced.** Check the script's `sentence_length`
     output against the persona's Sentence rhythm section's own documented rate (e.g. "very
     short sentences appear roughly once every 2-3 paragraphs," or its stated
     shortest/median/longest word counts) — that section is a required field in profile's
     template, so it should be present. Only if it's genuinely missing, flag it as an
     undocumented field per the policy above and fall back to a generic floor (one sentence
     under 8 words and one over 25 per paragraph of 3+ sentences), naming in the output that
     the fallback was used.
  2. **Shared openers — persona-sourced, generic floor as fallback.** Check the script's
     `shared_opener_runs` output against the persona's Openings or Quirks section: if it
     documents repeated-opener escalation as a habitual move (e.g. "repeats the same
     subject-verb opener across two consecutive sentences for deadpan escalation"), exactly
     that pattern at that documented length is not a hit — only a run longer than what
     persona documents counts. If persona documents no opener-repetition pattern at all, the
     generic AI-tell floor applies instead: no more than 2 sentences share an opener within a
     paragraph (the script's runs are draft-wide, not paragraph-scoped, so confirm a flagged
     run actually falls inside one paragraph before counting it as a hit).
  3. **Paragraph-length pattern — persona-sourced.** Check the script's
     `paragraph_length_in_sentences` output against the persona's own documented range (the
     shortest/longest paragraph-length note under its Structure habits section, if present) —
     a draft whose paragraphs run uniformly longer than that range, or open every single
     paragraph with the shortest length while never reaching the longest, reads as off-voice
     even when individual sentences pass. Being under the persona's paragraph-length ceiling
     is never penalized on its own — only a pattern that never varies (e.g. every paragraph
     landing at the short end, or every one at the long end) counts as a hit. If persona.md
     has no paragraph-length note, flag it as an undocumented field rather than skipping this
     sub-check silently.
  4. **Rhythm-run — generic AI-tell.** Check the script's `rhythm_runs` output: no run of 3+
     consecutive sentences within ~5 words of each other — a monotonous-length pattern reads
     as machine-generated regardless of whose voice is being imitated; no persona reference
     needed.
  5. **Paragraph-template repetition — generic AI-tell.** Consecutive paragraphs shouldn't
     hold the identical internal shape (claim → example → implication, or claim → because →
     restate) throughout, even when their opening words differ — judge the underlying shape
     each paragraph resolves to, not the surface phrasing it opens with; a paragraph that
     varies its opener but still lands the same claim-then-payoff structure as its neighbors
     still counts as a hit. Same reasoning as #4. This is a structural-shape judgment the
     script can't make — read the paragraphs directly.
  6. **Paragraph-to-paragraph consistency — self-referential, no persona field needed.** Use
     the script's per-paragraph `contractions_found` and `avg_sentence_words` fields and
     compare paragraphs against *each other*, not against persona.md's absolute baseline — a
     paragraph can sit inside persona's documented range and still be an outlier if it's the
     only one in the draft with `contractions_found: 0`, or the only one whose average
     sentence length runs well above the rest. Key this off `contractions_found` (the raw
     count), not `contraction_rate` — the rate is `null` whenever a paragraph has zero
     contractions *and* zero matched expandable phrases, which is exactly the zero-contraction
     outlier this sub-check exists to catch; reading the rate there would silently skip it.
     This catches quiet mid-draft drift a single top-to-bottom read can miss, because the
     surrounding paragraphs average it out on a whole-piece read. It's distinct from the
     contraction-ratio check under Formatting & mechanical tells below, which grades the whole
     draft's contraction ratio against persona's absolute baseline — this one grades
     paragraphs against the rest of the same draft. It's also distinct from sub-check 1's
     short-sentence cadence, which is persona-sourced — don't double-count a paragraph that
     trips both; if a paragraph's lack of a short-sentence beat is already caught by sub-check
     1, this sub-check should key only on contraction count and sentence length, not cadence.

  Quote the draft's shortest and longest sentence, name any repeated opener, report the
  draft's shortest and longest paragraph (in sentences), and for sub-check 6 name any
  paragraph whose contraction count or average sentence length diverges from the draft's own
  per-paragraph average, quoting it — as evidence for all six, sourced from the script's
  output plus a quote for context. (Device density — the same class of whole-piece structural
  tell — is its own hard gate above, not a sub-check here, and stays a manual read since
  detecting a recurring rhetorical device isn't something the script measures.)
- **Specificity** — weight 20. Every paragraph needs one concrete, non-interchangeable
  detail (a number, name, or scenario); flag generic filler that could appear unchanged in
  an article on a different topic, and empty quantifiers ("many benefits," "a variety of,"
  "numerous," "several"). Name one concrete detail per paragraph as evidence — a paragraph
  with none fails.
- **Hedging & directness** — weight 10. Flag any of:
  - Formulaic delay-openers ("In today's...", "It's important to note that..."), stacked
    qualifiers ("arguably," "in many ways"), unearned summary-conclusion paragraphs, hype
    constructions ("doesn't just X — it revolutionizes it"), and a perfectly even register
    with no controlled imperfection (a fragment, an aside, a blunt line, direct address to
    the reader).
  - The canonical AI academic-transition list at sentence openers — "Moreover,",
    "Additionally,", "Furthermore,", "Hence,", "Therefore,", "Consequently,", "Nonetheless,",
    "Nevertheless," — unless the persona's Transitions & connectors section documents one of
    these as a word they actually use, in which case check frequency against that baseline
    instead of flagging on sight. This 8-word list is a floor of always-suspect openers, not
    the whole check: beyond it, flag any other empty transition used more than the persona's
    documented Transitions & connectors register supports (e.g. "On the other hand," "That
    being said," "In addition," if the persona's samples don't use them this way).
  - Signposting ("let's dive in," "here's what you need to know"), collaborative-artifact
    leftovers ("I hope this helps," "let me know if you'd like me to expand"), and
    sycophantic tone ("great question," "you're absolutely right") — chatbot-correspondence
    habits, not prose.
  - "Turns out"/"it turns out that" used as a reveal pivot ("Turns out the config had a
    lower timeout") — it manufactures a discovery narrative where a direct statement would
    do; the fix is dropping the pivot phrase, not the fact itself.
  - Announcement sentences of the form "What [verb phrase] was [the revelation]" ("What
    surprised me was...", "What I didn't expect was...", "The thing I realized was..."),
    with or without a following colon — the announcement structure is the tell, not the
    punctuation.
  - Vague attribution ("experts believe," "research suggests," "studies show") with no
    named source — either the source is named or the claim is cut; this overlaps the
    Accuracy & integrity gate but is worth flagging here too since it's a register tell
    independent of whether the claim is literally true.
  - Novelty inflation ("nobody is talking about this," "this changes everything") presented
    as revelation instead of one interpretation among others.
  - Hedge-stacked predictions where a modal verb and a hedge cancel each other out ("could
    potentially," "may eventually," "might possibly") — keep one hedge, not two.
  - Social endorsement closers ("worth your time," "thank me later," generic bookmark/share
    prompts) — chatbot-correspondence habits, same family as the signposting/sycophancy hits
    above.

  Quote one plainly-committed line and flag any hits found.
- **Voice match** — weight 20. Check directly against the persona's Imitation checklist (its
  5 most load-bearing traits) and AI-tell checklist (patterns this person's writing does NOT
  contain), plus the persona's Sentence rhythm, Openings, Transitions & connectors,
  Vocabulary, Function-word tendencies, Punctuation, and Never does sections by name — don't
  substitute a vague "register and punctuation generally" pass for reading each section.
  Function-word tendencies in particular (causal "since"/"as," sentence-initial "Though")
  is easy to skip because it looks like a minor grammatical tic, but it's load-bearing enough
  to appear a second time under Quirks — treat a draft's use or non-use of the persona's
  documented function-word habits as checkable evidence here, same as any other section. Also
  check the draft's lexical-repetition tolerance against the persona's
  documented baseline (its Vocabulary section, if it notes one): if the persona repeats a
  word plainly on recurrence and the draft instead reaches for a synonym each time
  ("elegant variation"), or vice versa, that's a specific, checkable voice mismatch — quote
  an instance where the draft's choice diverges from the documented baseline. If the persona
  documents a `Vocabulary richness baseline` with all three numbers — hapax legomenon rate,
  Yule's K, and Honore's R — compare each against the matching script output for the draft
  (`vocabulary.hapax_rate`, `vocabulary.yules_k`, `vocabulary.honores_r`). If the persona
  predates this three-number baseline and only records a hapax rate, compare that one number
  alone, name it explicitly as a fallback in the writeup, and flag that the persona is due for
  a `profile` refresh to pick up Yule's K and Honore's R. Mind the direction: hapax rate and
  Honore's R both run *higher* for richer vocabulary; **Yule's K runs *lower* for richer
  vocabulary** — a draft with a higher Yule's K than the persona's baseline is flatter, not
  richer. Don't average the three into one number; they're on different scales. If
  `vocabulary.honores_r` is `null` for either the persona's baseline or the draft (an all-hapax
  sample), skip that one comparison and say so rather than treating `null` as a low score —
  fall back to the other two (or the other one, in the fallback case above). All three are
  length-dependent to varying degrees (hapax rate most, Yule's K least), so only score any of
  them as a numeric mismatch when the draft's `vocabulary.total_words` falls roughly within the
  word count noted alongside the persona's baseline (e.g. "~55% hapax rate, Yule's K ~61,
  Honore's R ~1648 (~1550 words)"); if the draft's length differs substantially (roughly 2x+
  shorter or longer), treat all three — including Yule's K — as directional context only: note
  the direction of any divergence without penalizing the score. None of the three is robust
  enough to anchor a scored mismatch across that large a length gap; a length-matched draft is
  needed for a real numeric penalty here, not a judgment call in the moment. A draft running
  noticeably richer or flatter than the documented baseline, on whichever of the three numbers
  is still trustworthy at the draft's length, is a checkable voice mismatch, not just a vibe. Any phrase of
  4+ consecutive words also appearing verbatim in `writing/samples/` is an automatic 0
  regardless of everything else — that's copying, not style. Name 2 specific persona traits
  and confirm they appear.
- **Agency & construction** — weight 10. Flag any of:
  - Inanimate or abstract nouns performing human actions ("the complaint becomes a fix,"
    "the data tells us," "the decision emerges," "the market rewards") — name the actual
    person responsible, or use "you," instead.
  - Passive voice with no named actor ("mistakes were made," "it is believed that").
  - Binary-contrast templates ("Not X, it's Y," "The answer isn't X, it's Y," "It feels like
    X, it's actually Y," "not just X but also Y") — state the true half directly instead of
    setting up the reversal.
  - Sentences opening with a Wh-word (What/When/Where/Which/Who/Why/How) used as a
    rhetorical setup rather than a genuine question — unless the persona's Openings section
    documents question-openers as a habitual move, in which case check frequency against
    that baseline instead of flagging on sight.
  - Narrator-from-a-distance observations floating above the scene instead of naming a
    person or the reader ("Nobody designed this," "People tend to...").
  - Constructed-insight patterns — sentence shapes that manufacture the feel of insight
    rather than earning it:
    - A formula personal-essay opener naming the ranked memory before the incident ("The
      failure I think about most often happened in 2019," "The decision I regret most
      is...").
    - A participial reframe pivot presenting facts then recasting them as meaningful ("Laid
      out that way, it reads like a strategy," "Seen this way, the arc changes").
    - A "more X than Y" comparative framing something by contrast instead of stating it
      directly ("feels more like drift than design") — distinct from the binary-contrast
      template above, which negates ("Not X, it's Y") rather than compares.
    - A mini-aphorism paragraph closer, a 4-7 word fragment that tells the reader the lesson
      instead of trusting them to draw it ("That's the part that stuck," "That's what
      changed").
    - The landing phrase "is the actual/real work" used to deliver a conclusion ("Debugging
      production is the actual work").
    - An aphoristic or chiasmus closer built as a standalone-quotable or reversed-parallel
      line ("The boilerplate is cheaper than the confusion," "Being specific about being
      wrong is more useful than being vague about being right").

  Quote every hit in full. Score 1 if none, 0.5 for one or two isolated hits, 0 for a
  cluster.
- **Overused-word clusters** — weight 5. Treat as a hint, not a ban — one flagged word is
  fine if it's genuinely the most accurate one; the real tell is a *cluster*, or these
  appearing alongside the patterns above. Watch for: "delve", "tapestry",
  "landscape"/"navigate" (figurative), "embark", "unlock", "elevate", "empower", "seamless",
  "leverage" (verb), "robust", "testament", "utilize", "harness" (figurative), "streamline",
  "underscore" (verb), "pivotal", "innovative", "cutting-edge", "realm", "synergy",
  "underpinnings". Check any hit against the persona's Vocabulary and Ornamentation sections
  first — a word the persona's own samples actually use, or one that fits within its
  documented Ornament baseline rate, is not a hit; this list is a generic floor, not an
  override of what persona.md already documents as this person's real vocabulary. List any
  remaining hits and justify or remove each. Score
  1 if no unjustified hits, 0.5 for one or two isolated unjustified hits, 0 for a cluster.
- **Formatting & mechanical tells** — weight 5. Independent of wording, these are
  near-mechanical to check: em dash or en dash use beyond what the persona's punctuation
  profile documents (a single em dash is not automatically a hit — check it against the
  persona's actual frequency first); boldface used as a mechanical emphasis tic rather than
  sparingly; inline-header bullet lists ("**Label:** sentence" repeated down a list); Title
  Case In Headings instead of sentence case; emojis decorating headings or bullets; curly
  quotation marks (" ") stacked with other tells rather than appearing alone (most editors
  auto-curl, so this one only counts in combination). Take the draft's contraction ratio
  from the script's `contraction.contraction_rate` output and compare it
  against the `Contraction baseline` line in `writing/persona.md` (if that line is missing
  because the persona predates this check, fall back to judging contraction use against the
  samples cited elsewhere in the file — persona.md's own quoted evidence, not an editor-owned
  number, so this still counts as persona-primary rather than a generic substitute) — a draft
  that expands contractions the persona
  normally uses reads as over-formalized AI text. Check `contraction.low_confidence` first:
  it's `true` whenever `expandable_forms_found` is under 2, which means the rate is derived
  from too few (or zero) matched expandable phrases to trust as a measurement — a draft with
  several contractions and no matched expandable phrase scores a trivial `1.0` that says
  nothing about actual contraction discipline. When `low_confidence` is true, don't score the
  ratio numerically; fall back to a manual read of contraction use against the persona's
  documented habit instead. Flag any semicolon linking two independent
  clauses in non-academic prose (exception: comma-containing lists, e.g. "Austin, TX; Denver,
  CO") and any mid-sentence colon preceded by an incomplete clause ("The problem: nobody
  tests this," "The answer: start earlier") — both read as AI structural habits in casual or
  narrative prose, check against the persona's own punctuation profile first in case either
  is a documented habit. List every hit with a quote. Score the
  hits, not the absence: 1 if "0 hits found", 0.5 for one or two isolated hits, 0 for a
  cluster of hits or any single hit repeated throughout the draft.
- **Ornament density** — weight 20. Enumerate every sentence in the draft, numbered, tagged
  PLAIN or ORNAMENTED (contains a simile, metaphor, or elevated comparison) — a summary
  ratio alone is not acceptable evidence, show the full numbered list. Compare the ratio to
  the persona's `Ornament baseline` line — a required field in profile's template, so it
  should be present. Only if it's genuinely missing, flag it as an undocumented field per the
  policy above and fall back to a generic 1-in-3 floor, naming in the output that the
  fallback was used. Being under baseline is never penalized — score 1. Over baseline:
  score 1 within 15 percentage points over, 0.5 more than 15 and up to 30 points over, 0
  more than 30 points over.

### Scoring

Sum each check's `weight × score`, divide by 100, and multiply by 100 for a 0-100 score.
Show the full per-check breakdown (score × weight = result) before stating the total — never
state a final score without it.

- **90-100 READY** — use as final, at most trivial polish needed.
- **75-89 MINOR REVISION** — usable, but fix the specific flagged lines before finalizing.
- **Below 75 NEEDS REVISION** — send back to the `writer` skill with the priority fix list
  before treating this as usable.

## Output

This skill grades; it does not rewrite. Produce:

1. A per-check PASS/FAIL/PARTIAL table with the required evidence for each (the three hard
   gates first, then the eight scored checks with weight and weighted result).
2. A prioritized list of every specific line that needs to change and why — triads and
   device density first, since gate failures are the most common and most severe failure
   mode; ornament density, specificity, and voice match are tied for the heaviest weight
   among the rest.
3. A final verdict: READY, MINOR REVISION, or NEEDS REVISION, with the score shown per
   Scoring above. If any hard gate failed, state that explicitly and stop there — skip
   the numeric score entirely, since the gates override scoring.

Hand the fix list back for the `writer` skill's revision mode to apply — don't rewrite the
draft yourself, even partially, even if the fix looks obvious.

If the draft still doesn't sound right for reasons the persona doesn't cover, say so
explicitly rather than forcing a check to pass — that's a signal `writing/persona.md` may
need another `profile` pass with more samples.

## Constraints

- Don't introduce new claims or facts while grading — you're evaluating the draft, not
  editing it.
- Flag, don't silently resolve, anything you're unsure whether the persona would actually
  do — call it out as a specific line in the fix list rather than guessing.
