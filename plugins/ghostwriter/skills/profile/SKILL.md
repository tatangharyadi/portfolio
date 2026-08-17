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

Save any raw samples handed to you under `writing/samples/` (create the directory if
missing) so future runs can build on them instead of starting over.

## Analysis

Read every sample fully before writing anything. Analyze only HOW it's written, not what
it's about — ignore topic, plot, and information entirely; a persona built from the subject
matter is useless for drafting on a different topic. Extract, with a short quoted example
for each claim (do not assert a trait without a supporting quote):

- **Sentence rhythm**: shortest and longest sentence length in words (give actual numbers,
  not just "average"), how often very short (under 8 words) and very long (over 30 words)
  sentences appear, whether length varies sharply or stays in a narrow band, run-ons vs.
  fragments, use of one-word or two-word sentences for emphasis.
- **Openings**: how sentences and paragraphs tend to begin — same structure every time or
  varied — and any recurring opening moves ("And"/"But"/"So" starters, questions, fragments).
- **Structure habits**: use (or absence) of headers/lists/bold, whether arguments build
  linearly or circle back, how pieces tend to end.
- **Transitions & connectors**: the specific transition words/phrases this writer actually
  uses, and ones they clearly avoid (e.g. never "furthermore" or "moreover").
- **Vocabulary fingerprints**: recurring words/phrases, contractions vs. formal, jargon level,
  concrete nouns vs. abstractions, swearing/slang if present, regionalisms.
- **Punctuation tells**: em dash frequency, semicolons, ellipses, parentheticals, Oxford comma
  use, exclamation point frequency.
- **Ornamentation**: rough fraction of sentences containing a simile, metaphor, or elevated
  comparison vs. plain literal ones (e.g. "approximately 1 in 5 sentences are ornamented").
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

## Punctuation
...

## Ornamentation
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
