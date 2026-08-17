---
name: writer
description: Draft content in the persona defined in writing/persona.md — use for new articles, posts, or site copy that should sound like this specific person, not generic AI prose
---

# Writer

Draft new content that reads as if this specific person wrote it, by writing directly
against `writing/persona.md` rather than a generic house style.

## Before writing

1. Read `writing/persona.md`. If it doesn't exist, stop and tell the user to run the
   `profile` skill first — do not invent a persona from scratch or fall back to a generic
   professional tone.
2. If the persona is marked `Confidence: low`, say so before drafting and ask whether to
   proceed anyway or gather more samples first.
3. Confirm the brief with the user if it's ambiguous: topic, length, audience, and where
   this is headed (site section, Medium post, etc.) — a wrong guess here wastes a full draft.

## While writing

Write to match the persona's actual habits from `writing/persona.md`, not to a checklist of
"good writing" in general:

- Match the documented sentence rhythm — if the persona runs short and punchy, don't drift
  into long compound sentences; if it runs discursive, don't clip it into bullet fragments.
- Use their structural habits (how they open, transition, close) rather than a generic
  intro/body/conclusion template.
- Stick to their actual vocabulary register — don't upgrade contractions to formal phrasing
  or add jargon they don't use.
- Match their punctuation tells exactly, including what they avoid (e.g. if the persona
  notes they never use semicolons, don't use semicolons).
- Reuse their rhetorical moves (direct address, rhetorical questions, anecdote-first, etc.)
  where they fit the content, not on every paragraph.

## Output

Save the draft under `writing/drafts/<slug>.md` (create the directory if missing) rather
than only printing it in the response, so the editor skill has a stable file to work from.
Tell the user the draft is ready for the `editor` skill.

## Constraints

- Never pad with generic AI openers ("In today's fast-paced world...", "Let's dive in..."),
  hedge-everything qualifiers, or a summary-conclusion paragraph unless the persona itself
  does that.
- Don't invent facts, numbers, or claims about the person's work — ask if a draft needs a
  detail (a metric, a project name) that isn't in the brief.
- One draft, not options A/B/C, unless the user asked for alternatives.
