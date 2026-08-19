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
one specific person writes — mixing authors produces a blend that's true of neither. Back a
content read with a quick numeric check: for each sample, count its average sentence length
and contraction rate; a sample whose numbers diverge sharply from the others (e.g. roughly
half the contraction rate, or a sentence-length median off by more than a third) is grounds
to suspect a different author even when the subject matter reads consistently — voice can
survive a topic switch, these numbers don't usually survive an author switch. If samples
turn out to be multi-author, flag it to the user instead of merging silently, and prefer
building from the single largest-author subset over shipping a blended profile.

Save any raw samples handed to you under `writing/samples/` (create the directory if
missing) so future runs can build on them instead of starting over.

## Measure first

Before the qualitative read, run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/text_metrics.py
<sample-file>` against each saved sample (or a temp file holding pasted text). It computes
sentence-length stats, paragraph-length-in-sentences, contraction rate, and hapax legomenon
rate directly from the text — the exact numbers several sections below ask for, without
relying on the model's own counting. Use its output as the source of the numeric fields in
those sections (Sentence rhythm's word counts, Contraction baseline, Vocabulary richness
baseline); the model's job is still reading each sample for everything qualitative (openings,
structure, rhetorical moves, ornamentation, what's absent) that a line-counting script can't
judge. If a sample is short enough that the script's paragraph/sentence split looks wrong on
inspection, say so and fall back to a manual count for that sample rather than trusting a
bad split silently. With multiple samples, run the script per sample and note whether the
numbers agree or diverge — divergence here is also evidence for the single-author check above.

## Analysis

Read every sample fully before writing anything. Analyze only HOW it's written, not what
it's about — ignore topic, plot, and information entirely; a persona built from the subject
matter is useless for drafting on a different topic. Extract, with a short quoted example
for each claim (do not assert a trait without a supporting quote):

- **Sentence rhythm**: shortest, median, and longest sentence length in words (pull these from
  the script's `sentence_length` output — give actual numbers, not a computed average or
  standard deviation), how often very short
  (under 8 words) and very long (over 30 words) sentences appear, whether length varies
  sharply or stays in a narrow band, run-ons vs. fragments, use of one-word or two-word
  sentences for emphasis.
- **Openings**: how sentences and paragraphs tend to begin — same structure every time or
  varied — and any recurring opening moves ("And"/"But"/"So" starters, questions, fragments).
- **Structure habits**: use (or absence) of headers/lists/bold, whether arguments build
  linearly or circle back, how pieces tend to end, and whether paragraphs repeat one shape
  (e.g. claim-then-evidence every time) or vary it — if the sample shows more than one shape,
  quote at least two differently-shaped paragraphs rather than asserting "varies" from one
  example. Report typical paragraph length in sentences (shortest and longest, from the
  script's `paragraph_length_in_sentences` output, not just "varies") — this is a distinct,
  separately countable structural tell from sentence rhythm above, so don't skip it just
  because sentence rhythm is already documented.
- **Transitions & connectors**: the specific transition words/phrases this writer actually
  uses, and ones they clearly avoid (e.g. never "furthermore" or "moreover").
- **Vocabulary fingerprints**: recurring content words/phrases (not conjunctions, pronouns, or
  prepositions — those belong under Function-word tendencies below), contractions vs. formal,
  jargon level, concrete nouns vs. abstractions, swearing/slang if present, regionalisms.
  Also note lexical-repetition tolerance: when the same word applies twice in close proximity
  (a sentence or two apart), does this writer repeat it plainly, or reach for a synonym to
  avoid repeating ("elegant variation")? Quote an instance. This is distinct from what recurs
  across a whole piece above — it's about tolerance for *immediate* repetition, and it's a
  countable, actionable field regardless of the writer's answer. Also report the hapax
  legomenon rate — the percentage of distinct words in the sample used exactly once — as a
  concrete vocabulary-richness number, pulled from the script's `vocabulary.hapax_rate` output
  rather than estimated, the same way Ornament baseline and Contraction baseline give their
  sections a measured rate instead of a qualitative impression like "varied vocabulary."
- **Function-word tendencies**: specific conjunctions, pronouns, or prepositions that recur
  noticeably or are conspicuously avoided (e.g. "but" over "however," dropped relative
  pronouns — "the thing I built" not "the thing that I built") — quote an instance for each,
  don't estimate a frequency; this is unconscious grammatical habit, distinct from the
  deliberate discourse markers covered under Transitions & connectors above.
- **Punctuation tells**: em dash frequency, semicolons, ellipses, parentheticals, Oxford comma
  use, exclamation point frequency.
- **Contraction density**: pull the ratio of contracted forms ("don't", "it's", "they're")
  against expandable forms actually found ("do not", "it is", "they are") from the script's
  `contraction.contraction_rate` output (e.g. "contracts ~90% of the time it could") — measure
  it directly rather than estimating, even when the answer seems obvious from a quick read.
  The script's expandable-phrase list is a fixed set of common patterns, not exhaustive; if a
  sample's rate looks off from a quick read, spot-check a few sentences by hand before trusting
  it.
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
Vocabulary richness baseline: <the measured hapax legomenon rate, e.g. "~42% of distinct
words used exactly once">
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
