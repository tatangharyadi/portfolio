---
name: editor
description: Check a draft against writing/persona.md and revise it to match the persona and read as human-written, not AI-generated
---

# Editor

Take a draft (from `writing/drafts/`, pasted text, or wherever the user points) and revise
it so it matches `writing/persona.md` and doesn't read as AI-generated.

## Before editing

Read `writing/persona.md` in full, especially the "AI-tell checklist" section — that section
lists the specific AI-sounding patterns this person's real writing does NOT contain, and is
the primary thing to check the draft against. If `writing/persona.md` is missing, stop and
say the `profile` skill needs to run first.

## Pass 1 — persona conformance

Go section by section against the persona and flag mismatches with a quote from the draft
next to the persona trait it violates:

- Sentence rhythm drifting from the documented pattern (e.g. draft is all long compound
  sentences when the persona is short and punchy).
- Structural habits not followed (wrong kind of opener/closer, headers where the persona
  never uses them, etc.).
- Vocabulary register mismatch (more formal, more jargon, or more casual than the samples).
- Punctuation habits violated (especially anything the persona's "never does" section rules
  out).
- Missing rhetorical moves the persona relies on, or moves used that the persona never uses.

## Pass 2 — AI-tell sweep

Independent of the persona, scan for generic markers that make text read as AI-written
regardless of whose voice it's imitating:

- Formulaic openers ("In today's...", "In the ever-evolving...", "Let's dive in").
- Empty transitions ("Furthermore", "Moreover", "That being said") used more than a real
  human would in this register.
- Symmetric list-of-three padding ("not only X, but also Y, and ultimately Z") where the
  content doesn't need it.
- Over-qualification / hedging on every claim ("it's important to note that", "arguably",
  "in many ways") stacked sentence after sentence.
- Tidy summary-conclusion paragraphs that restate what was just said, when nothing earlier
  called for one.
- Uniform sentence length and rhythm — real writing (and this persona specifically) has
  variance; a wall of same-length sentences is a tell on its own.
- Em dash overuse beyond what the persona's punctuation profile documents.
- Perfectly balanced/parallel phrasing that no one would naturally speak.

## Output

Produce a revised version of the draft. For each substantive change, note briefly what was
changed and why (persona mismatch vs. AI-tell), so the user can see the reasoning rather
than just a diff. Write the revision back to the same file under `writing/drafts/` if that's
where the draft came from.

If, after revision, the draft still doesn't sound right for reasons the persona doesn't
cover, say so explicitly rather than forcing a fix — that's a signal `writing/persona.md`
may need another `profile` pass with more samples.

## Constraints

- Don't rewrite the whole piece from scratch — edit toward the persona, preserve the
  writer's actual content and structure choices from the writer skill.
- Don't introduce new claims or facts while editing.
- Flag, don't silently fix, anything you're unsure whether the persona would actually do —
  ask rather than guess when a change is borderline.
