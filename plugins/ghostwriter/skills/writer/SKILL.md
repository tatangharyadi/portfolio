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
- Give actions a named actor — a specific person, or "you" — instead of letting an
  abstraction do something human ("the decision emerges," "the data tells us"). Default to
  active voice; use passive only when the actor is genuinely unknown or beside the point.
  Skip binary-contrast setups ("Not X, it's Y") and just state the true half.

## Before finalizing (every draft)

Run this as a dedicated last pass, separate from writing itself — do not rely on catching
these while composing. Triad scanning is deliberately not on this list: the `editor` skill's
hard gate does that check exhaustively and with zero tolerance, and this session's evidence
is that a self-scan run by the same pass that generated the prose misses hits the editor
catches. Spend this pass on what only the writer is positioned to judge — persona fidelity —
and let `editor` be the backstop for triads.

- **Fabrication scan**: tag every specific factual claim — name, number, date, stat,
  attributed quote. Confirm each one traces to the brief, to `writing/persona.md`, or is
  clearly fictional detail inside an intentionally fictional piece. Anything else becomes
  `[PLACEHOLDER]`, never a filled-in guess — a flatter true sentence beats a smooth invented
  one.

- **Self-check**: before calling the draft done, ask "What in this draft would make a
  skeptical reader say it's AI-generated?" and answer in one line — if you can name
  something, fix it now rather than leaving it for the `editor` skill to catch. Then
  re-confirm the fabrication scan above is still clean; a fix made since that scan can
  reintroduce an unmarked claim.

Only after both scans are clean, do a general pass for ornament density (against the
`Ornament baseline` line in `writing/persona.md`), hedging, and word clusters.

## Revision mode

If you're handed a draft you wrote plus feedback from the `editor` skill (a per-check
breakdown, specific flagged lines, or a NEEDS REVISION / MINOR REVISION verdict) — whether
the editor ran earlier in this same session or the user pasted the feedback back in — switch
to a surgical fix instead of rewriting:

1. Don't start over. Leave everything the editor didn't flag untouched — rewriting unflagged
   sentences risks breaking parts that already worked.
2. Work through the flagged issues in the order given. For each one: quote the problem
   sentence, rewrite only that sentence or clause to fix the specific issue named, and leave
   the sentences around it alone unless the fix forces a small adjustment to the one right
   before or after for the paragraph to still read.
3. Re-run the fabrication scan above against the whole revised draft. If the editor flagged a
   triad, fix only the quoted line(s) as instructed — don't re-scan the rest of the draft for
   triads yourself; that's `editor`'s job on the re-check.
4. Output the full revised draft, not just the changed lines, and save it back to the same
   `writing/drafts/<slug>.md` file.
5. Below the draft, list each change on one line, naming which flagged issue it addresses.
6. Don't re-grade the revision yourself or claim it now passes — hand it back to the
   `editor` skill for an independent re-check, same as a first draft.

## Output

Save the draft under `writing/drafts/<slug>.md` (create the directory if missing) rather
than only printing it in the response, so the editor skill has a stable file to work from.
Tell the user the draft is ready for the `editor` skill.

## Constraints

- Never pad with generic AI openers ("In today's fast-paced world...", "Let's dive in..."),
  hedge-everything qualifiers, or a summary-conclusion paragraph unless the persona itself
  does that.
- Don't invent facts, numbers, or claims about the person's work — see the fabrication scan
  above.
- One draft, not options A/B/C, unless the user asked for alternatives.
