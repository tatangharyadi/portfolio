---
name: editor
description: Grade a draft against writing/persona.md with a scored audit and hand back a prioritized fix list — does not rewrite; use the writer skill's revision mode to apply fixes
---

# Editor

Take a draft (from `writing/drafts/`, pasted text, or wherever the user points) and audit it
against `writing/persona.md`, as a skeptical outside reviewer with no stake in whether it
passes. This skill grades and hands back specific fixes — it does not rewrite the draft
itself; that's the `writer` skill's revision mode.

## Before editing

Read `writing/persona.md` in full. Check the draft against the "Imitation checklist" section
first — it's the 5 most load-bearing traits, so a draft that fails one of those is worth
flagging before a full section-by-section pass. Then use the "AI-tell checklist" section,
which lists the specific AI-sounding patterns this person's real writing does NOT contain,
as the primary thing to check the draft against. If `writing/persona.md` is missing, stop
and say the `profile` skill needs to run first.

## Mindset

Run this audit as a skeptical editor reviewing someone else's submission, not as the author
reviewing their own work. Actively look for reasons to FAIL a check, not reasons to pass it —
if a check could reasonably go either way, mark it FAIL. Satisfying the letter of a check
while missing its intent (e.g. decorating a triad so it reads better without breaking the
underlying three-item skeleton — see the structural-variety gate below) does not pass it.
Every verdict needs evidence: a quote, a count, or a named example — a bare score or claim
with nothing under it is not acceptable output. Re-read your own verdicts once more against
this mindset before finalizing. If you find yourself wanting to reclassify a sentence from
ORNAMENTED to PLAIN, or a check from FAIL to PASS, without the underlying wording having
changed, don't — that's rationalizing a pass, not evidence of one. Flag it as still failing.

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
- Scan the full draft for any sentence built as three parallel clauses or items ("There was
  X...; Y...; and Z...", "She did A; she did B; she did C", "It was A. It was B. It was C.").
- A triad stays a triad even when each item carries its own descriptive clause, or when
  connector/ordinal words are inserted between items ("next," "then," "finally," "first...
  second... third"). Judge by the underlying X; Y; and Z skeleton, not the decoration.
- If the draft explicitly names the device it's using ("the sacred triad," "the trilogy
  of," "three truths"), count that as a confirmed triad regardless of how it reads.
- This is a zero-tolerance gate: even a single confirmed triad FAILS it, no partial credit —
  this has been the most recurring failure across drafts, so treat any count above zero as
  disqualifying, not as a minor deduction.
- Evidence: quote every triad found in full, including decorated or connector-disguised
  ones. State the count explicitly — "0 triads found" if none, don't skip this silently.

## Scored checks (only if both gates pass)

Score every check 1 (fully present) / 0.5 (partial) / 0 (absent), with quoted evidence:

- **Sentence-length variation** — weight 20. See the sentence-length patterns below. Quote
  the draft's shortest and longest sentence as evidence.
- **Specificity** — weight 20. See the specificity patterns below. Name one concrete detail
  per paragraph as evidence; if a paragraph has none, that paragraph fails the check.
- **Hedging & directness** — weight 10. See the hedging & smoothness patterns below. Quote
  one plainly-committed line and flag any hedge phrases found.
- **Voice match** — weight 20, omit entirely (and rescale, see Scoring) if no
  `writing/persona.md` exists. Sentence rhythm, transitions, vocabulary, register, and
  punctuation match the persona. Any phrase of 4+ consecutive words also appearing verbatim
  in `writing/samples/` is an automatic 0 on this check regardless of everything else —
  that's copying, not style. Name 2 specific persona traits and confirm they appear.
- **Overused-word clusters** — weight 10. See the secondary word-hint list below. List any
  flagged words found and justify or remove each.
- **Ornament density** — weight 20. Enumerate every sentence in the draft, numbered, tagged
  PLAIN or ORNAMENTED (contains a simile, metaphor, or elevated comparison) — a summary
  ratio alone is not acceptable evidence, show the full numbered list. Compare the resulting
  ratio against the persona's "Ornament baseline" (default to 1-in-3 if the persona has none
  or doesn't exist). Score 1 if within ±15 percentage points of baseline, 0.5 if 15-30 points
  over, 0 if more than 30 points over.

### Scoring

Sum each check's `weight × score`. The weights above total 100 when all six checks apply,
80 when Voice match is omitted for missing `writing/persona.md` — divide the sum by whichever
total actually applies (100 or 80) and multiply by 100 to get a 0-100 score.

- **90-100 READY** — use as final, at most trivial polish needed.
- **75-89 MINOR REVISION** — usable, but fix the specific flagged lines before finalizing.
- **Below 75 NEEDS REVISION** — send back to the `writer` skill with the priority fix list
  before treating this as usable.

Always show the full per-check breakdown (score × weight = result) before stating the total.
Never state a final score without the breakdown that produced it.

## AI-tell sweep

Independent of the persona, scan for the statistical patterns that make text read as
AI-written regardless of whose voice it's imitating — this is mostly about sentence-level
shape, not individual words. Each pattern below is something to recognize and remove, never
to imitate — treat any resemblance in the draft as a defect to fix, not a style to preserve.

**Sentence-length patterns (check first — most important):**

- No run of 3+ consecutive sentences whose lengths are within ~5 words of each other.
- Every paragraph of 3+ sentences needs real range: at least one short sentence (under 8
  words) and at least one long one (over 25 words). A one- or two-word sentence is fine and
  worth using occasionally.
- Fail signal: if every sentence in a paragraph "feels" the same length when read aloud, it
  fails. Fix: collapse some sentences together, cut others down to a fragment.

**Structural repetition patterns:**

- Sentence openers: within a paragraph, don't start more than 2 sentences the same way
  (same first word or same subject-verb-object shape). Fix: vary with a question, a
  fragment, a subordinate clause, a mid-thought start.
- Paragraph openers: consecutive paragraphs shouldn't open with the same template (every
  one "Let's talk about X," or every one "X is essential because...").
- Symmetric list-of-three padding ("not only X, but also Y, and ultimately Z", or two
  three-item lists back to back). Fix: break the list — make one point, expand it with a
  real example, move on.
- Don't give every paragraph the identical internal shape (claim → because → restate). Mix
  it: some argue, some show an example, some just land a single line.

**Specificity patterns:**

- Flag any sentence that could appear unchanged in an article on a totally different
  topic — that's generic filler. Fix: replace it with a concrete number, name, or scenario.
- Empty quantifiers with nothing attached ("many benefits", "a variety of situations",
  "numerous", "several", "a lot of").
- Every paragraph should carry at least one specific, non-interchangeable detail; if it
  carries none, it's probably AI-shaped.

**Hedging & smoothness patterns:**

- Formulaic openers that delay the point ("In today's...", "It's important to note that",
  "When it comes to..."). Fix: delete the opener, start on the actual point.
- Empty transitions ("Furthermore", "Moreover", "That being said") used more than a real
  human would in this register. Fix: cut the word, or use a connector the persona actually
  uses.
- Over-qualification stacked sentence after sentence ("arguably", "in many ways"). Fix:
  delete the hedge, say the thing directly.
- Tidy summary-conclusion paragraphs that restate what was just said, when nothing earlier
  called for one.
- Perfect, unbroken smoothness — no opinion, no friction, no controlled imperfection
  (a fragment, an aside, a blunt line, direct address to the reader). Fix: add a real
  opinion or a specific detail that only this persona would include.
- Hype constructions with inflated payoff ("doesn't just X — it revolutionizes it",
  "not only enhances but also empowers", "unlock your full potential"). Fix: state one
  plain claim about what the thing actually does, with a concrete result.
- Em dash overuse beyond what the persona's punctuation profile documents.
- One even register held for the whole piece — real writing (and this persona) shifts
  tone: a sharp line here, a slower explanation there.

**Secondary check — overused words:** treat this as a hint, not a ban. A word on this list
is fine if it's genuinely the most accurate one; the real tell is a *cluster* of them
appearing together, or the statistical patterns above being present. Watch for: "delve",
"tapestry", "landscape" (figurative), "navigate" (figurative), "embark", "unlock",
"elevate", "empower", "seamless", "leverage" (verb), "robust", "testament".

## Output

This skill grades; it does not rewrite. Produce:

1. A per-check PASS/FAIL/PARTIAL table with the required evidence for each (the two hard
   gates first, then the six scored checks with weight and weighted result).
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
