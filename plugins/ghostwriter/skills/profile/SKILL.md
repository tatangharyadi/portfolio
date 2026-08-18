---
name: profile
description: Analyze writing samples and extract a voice persona into writing/persona.md, for use by the writer and editor skills
---

# Profile

Build (or refresh) `writing/persona.md`: a concrete, falsifiable description of how this
specific person writes, derived from their own text — not a generic "professional tone"
description.

## Inputs

Ask the user for one or more writing samples if none are given: pasted text, a file path,
or a URL/Medium link they've already fetched into a file. Prefer at least 3 samples and
600+ words total; if only one short sample is available, say so in the output and mark the
profile as low-confidence.

Confirm all samples share one author before analyzing. A persona is a description of how
one specific person writes — mixing authors produces a blend that's true of neither. If
samples turn out to be multi-author, flag it to the user instead of merging silently, and
prefer building from the single largest-author subset over shipping a blended profile.

Save any raw samples handed to you under `writing/samples/` (create the directory if
missing) so future runs can build on them instead of starting over.

## Analysis

Read every sample fully before writing anything. Analyze only HOW it's written, not what
it's about — ignore topic, plot, and information entirely; a persona built from the subject
matter is useless for drafting on a different topic. Extract, with a short quoted example
for each claim (do not assert a trait without a supporting quote):

- **Sentence rhythm**: shortest, median, and longest sentence length in words (count them —
  give actual numbers, not a computed average or standard deviation), how often very short
  (under 8 words) and very long (over 30 words) sentences appear, whether length varies
  sharply or stays in a narrow band, run-ons vs. fragments, use of one-word or two-word
  sentences for emphasis.
- **Openings**: how sentences and paragraphs tend to begin — same structure every time or
  varied — and any recurring opening moves ("And"/"But"/"So" starters, questions, fragments).
- **Structure habits**: use (or absence) of headers/lists/bold, whether arguments build
  linearly or circle back, how pieces tend to end, and whether paragraphs repeat one shape
  (e.g. claim-then-evidence every time) or vary it — quote at least two differently-shaped
  paragraphs if the sample repeats a shape, since a rigid template is itself an AI tell.
  Count typical paragraph length in sentences (shortest and longest, not just "varies") —
  this is a distinct, separately countable structural tell from sentence rhythm above, so
  don't skip it just because sentence rhythm is already documented.
- **Transitions & connectors**: the specific transition words/phrases this writer actually
  uses, and ones they clearly avoid (e.g. never "furthermore" or "moreover").
- **Vocabulary fingerprints**: recurring content words/phrases (not conjunctions, pronouns, or
  prepositions — those belong under Function-word tendencies below), contractions vs. formal,
  jargon level, concrete nouns vs. abstractions, swearing/slang if present, regionalisms.
- **Function-word tendencies**: specific conjunctions, pronouns, or prepositions that recur
  noticeably or are conspicuously avoided (e.g. "but" over "however," dropped relative
  pronouns — "the thing I built" not "the thing that I built") — quote an instance for each,
  don't estimate a frequency; this is unconscious grammatical habit, distinct from the
  deliberate discourse markers covered under Transitions & connectors above.
- **Punctuation tells**: em dash frequency, semicolons, ellipses, parentheticals, Oxford comma
  use, exclamation point frequency.
- **Contraction density**: count contracted forms ("don't", "it's", "they're") against places
  where the expanded form ("do not", "it is", "they are") would've fit grammatically, and give
  a rough ratio (e.g. "contracts ~90% of the time it could"). AI-generated text skews toward
  expanded forms even when the persona doesn't, so this is worth measuring even if it feels
  obvious.
- **Ornamentation**: rough percentage of sentences containing a simile, metaphor, or elevated
  comparison vs. plain literal ones (e.g. "approximately 20% of sentences are ornamented").
- **Rhetorical moves**: how they transition between ideas, how they land an ending, use of
  humor/self-deprecation/direct address to the reader, rhetorical questions, specific
  anecdotes vs. general claims.
- **Opinion posture**: hedged vs. blunt, first-person admissions of uncertainty, how they
  handle disagreement or critique.
- **What they never do**: patterns notably absent (e.g. never uses semicolons, never opens
  with a question, never uses bullet lists) — these are as identifying as what they do.
- **Quirks**: 3-5 specific, imitable habits that make this voice recognizable on their own,
  distinct from the categories above.

## Output: writing/persona.md

Write (overwrite) `writing/persona.md` with this structure:

```markdown
# Voice Persona — <name/site>

Last built: <do not fabricate a date — leave a placeholder "{{date}}" for the user to fill in>
Confidence: <low|medium|high> — based on <N samples, ~X words>
Source samples: writing/samples/<files>

## Sentence rhythm
...

## Openings
...

## Structure habits
...

## Transitions & connectors
...

## Vocabulary
...

## Function-word tendencies
...

## Punctuation
Contraction baseline: <the measured ratio, e.g. "contracts ~90% of the time it could">
...

## Ornamentation
Ornament baseline: <the measured fraction, e.g. "~20% of sentences">
...

## Rhetorical moves
...

## Opinion posture
...

## Never does
...

## Quirks
...

## AI-tell checklist (for the editor skill)
List the specific AI-sounding patterns THIS person does not use, so the editor skill has a
concrete diff to check against (e.g. "does not use 'in today's fast-paced world' style
openers", "does not summarize with 'In conclusion'", "does not overuse em dashes the way
generic AI output does — this writer uses at most one per paragraph").

## Imitation checklist
The 5 most important, concrete things to copy to sound like this writer — no generic advice
like "be engaging." This is the quick-reference the writer/editor skills should check first.
```

If `writing/persona.md` already exists, treat this as a refresh: read the existing file,
merge in evidence from new samples, and note what changed rather than silently discarding
prior analysis.

## Constraints

- Every trait must trace to a quoted snippet from a real sample — no invented traits.
- Do not editorialize about writing quality; describe the pattern, not whether it's good.
- Keep the file under ~150 lines — this is a working reference for the writer/editor
  skills, not an essay about the person.
