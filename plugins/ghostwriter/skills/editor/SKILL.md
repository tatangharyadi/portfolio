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

Read `writing/persona.md` in full — the Imitation checklist, AI-tell checklist, and the
`Ornament baseline: ...` line under `## Ornamentation` feed directly into the scored checks
below. If it's missing, stop and say the `profile` skill needs to run first.

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
off; unsourced claims (most writing is unsourced — that alone proves nothing). Weigh these in
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

If either gate fails, stop: the verdict is NEEDS REVISION, skip the numeric score below, and
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

## Scored checks (only if both gates pass)

Score each 1 (fully present) / 0.5 (partial) / 0 (absent), with quoted evidence. Weights sum
to 100:

- **Sentence rhythm & structure** — weight 20. No run of 3+ consecutive sentences within ~5
  words of each other; every paragraph of 3+ sentences needs at least one sentence under 8
  words and one over 25. Within a paragraph, no more than 2 sentences share an opener (same
  first word or same subject-verb-object shape), and consecutive paragraphs shouldn't open
  with the same template or hold the identical internal shape (claim → because → restate)
  throughout. Quote the draft's shortest and longest sentence, and name any repeated opener.
- **Specificity** — weight 20. Every paragraph needs one concrete, non-interchangeable
  detail (a number, name, or scenario); flag generic filler that could appear unchanged in
  an article on a different topic, and empty quantifiers ("many benefits," "a variety of,"
  "numerous," "several"). Name one concrete detail per paragraph as evidence — a paragraph
  with none fails.
- **Hedging & directness** — weight 10. Flag formulaic delay-openers ("In today's...", "It's
  important to note that..."), empty transitions used more than the persona's register
  supports ("Furthermore," "That being said"), stacked qualifiers ("arguably," "in many
  ways"), unearned summary-conclusion paragraphs, hype constructions ("doesn't just X — it
  revolutionizes it"), and a perfectly even register with no controlled imperfection (a
  fragment, an aside, a blunt line, direct address to the reader). Also flag signposting
  ("let's dive in," "here's what you need to know"), collaborative-artifact leftovers ("I
  hope this helps," "let me know if you'd like me to expand"), and sycophantic tone ("great
  question," "you're absolutely right") — these are chatbot-correspondence habits, not prose.
  Quote one plainly-committed line and flag any hits found.
- **Voice match** — weight 20. Check directly against the persona's Imitation checklist (its
  5 most load-bearing traits) and AI-tell checklist (patterns this person's writing does NOT
  contain), plus sentence rhythm, transitions, vocabulary, register, and punctuation
  generally. Any phrase of 4+ consecutive words also appearing verbatim in
  `writing/samples/` is an automatic 0 regardless of everything else — that's copying, not
  style. Name 2 specific persona traits and confirm they appear.
- **Overused-word clusters** — weight 5. Treat as a hint, not a ban — one flagged word is
  fine if it's genuinely the most accurate one; the real tell is a *cluster*, or these
  appearing alongside the patterns above. Watch for: "delve", "tapestry",
  "landscape"/"navigate" (figurative), "embark", "unlock", "elevate", "empower", "seamless",
  "leverage" (verb), "robust", "testament". List any hits and justify or remove each. Score
  1 if no unjustified hits, 0.5 for one or two isolated unjustified hits, 0 for a cluster.
- **Formatting & mechanical tells** — weight 5. Independent of wording, these are
  near-mechanical to check: em dash or en dash use beyond what the persona's punctuation
  profile documents (a single em dash is not automatically a hit — check it against the
  persona's actual frequency first); boldface used as a mechanical emphasis tic rather than
  sparingly; inline-header bullet lists ("**Label:** sentence" repeated down a list); Title
  Case In Headings instead of sentence case; emojis decorating headings or bullets; curly
  quotation marks (" ") stacked with other tells rather than appearing alone (most editors
  auto-curl, so this one only counts in combination). List every hit with a quote. Score the
  hits, not the absence: 1 if "0 hits found", 0.5 for one or two isolated hits, 0 for a
  cluster of hits or any single hit repeated throughout the draft.
- **Ornament density** — weight 20. Enumerate every sentence in the draft, numbered, tagged
  PLAIN or ORNAMENTED (contains a simile, metaphor, or elevated comparison) — a summary
  ratio alone is not acceptable evidence, show the full numbered list. Compare the ratio to
  the persona's `Ornament baseline` line (default 1-in-3 only if that line is missing from
  `writing/persona.md`). Being under baseline is never penalized — score 1. Over baseline:
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

1. A per-check PASS/FAIL/PARTIAL table with the required evidence for each (the two hard
   gates first, then the seven scored checks with weight and weighted result).
2. A prioritized list of every specific line that needs to change and why — triads and
   ornament density first, since those are the most common and most heavily weighted.
3. A final verdict: READY, MINOR REVISION, or NEEDS REVISION, with the score shown per
   Scoring above. If either hard gate failed, state that explicitly and stop there — skip
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
