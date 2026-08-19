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

Write only against persona.md, not against `editor`'s checklist — AI-tell detection (hedging,
agency, overused words, formatting tells, ornament density, triads, device density, and
everything else `editor` checks) is entirely `editor`'s job. Don't steer around, self-check
for, or otherwise anticipate that list while composing; a draft that faithfully matches the
persona and still trips an `editor` check comes back through the revision loop below, same as
any other fix.

## Before finalizing (every draft)

Run this as a dedicated last pass, separate from writing itself. Writer's job here is narrow:
fact discipline and persona fidelity — nothing about AI-tell or structural-pattern detection.
That's `editor`'s job alone, entirely, including triads, device density, hedging, agency,
overused words, formatting tells, and ornament density; writer doesn't self-scan, holistically
self-check, or otherwise anticipate any of it here.

- **Fabrication scan**: tag every specific factual claim — name, number, date, stat,
  attributed quote. Confirm each one traces to the brief, to `writing/persona.md`, or is
  clearly fictional detail inside an intentionally fictional piece. Anything else becomes
  `[PLACEHOLDER]`, never a filled-in guess — a flatter true sentence beats a smooth invented
  one. This is a fact-accuracy check, not an AI-tell scan — writer owns it as one of the three
  enforcement points in AGENTS.md's **Fabrication Discipline** section, independent of the
  AI-tell boundary above.

- **Persona-match pass**: re-read the draft directly against `writing/persona.md` — its
  Imitation checklist, sentence rhythm, structure habits, vocabulary, and `Ornament baseline`
  line — and fix anything that drifted from the documented voice while drafting. This checks
  fit to persona, not absence of AI-tells; a draft can pass this fully and still get flagged
  by `editor`, and that's expected, not a sign this pass failed.

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
   before or after for the paragraph to still read. Confirm the rewrite preserves the
   original claim exactly — same scope, same certainty/hedge level, same attribution, same
   named condition or number — a style fix that quietly softens a claim or drops who said it
   is a new problem, not a fix.
3. Re-run the fabrication scan above against the whole revised draft. If the editor flagged a
   gate-level issue (a triad, device density), fix only the quoted line(s) as instructed —
   don't re-scan the rest of the draft for that pattern yourself; that's `editor`'s job on the
   re-check.
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

- Don't invent facts, numbers, or claims about the person's work — see the fabrication scan
  above.
- One draft, not options A/B/C, unless the user asked for alternatives.
