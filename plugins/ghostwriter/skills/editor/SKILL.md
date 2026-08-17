---
name: editor
description: Check a draft against writing/persona.md and revise it to match the persona and read as human-written, not AI-generated
---

# Editor

Take a draft (from `writing/drafts/`, pasted text, or wherever the user points) and revise
it so it matches `writing/persona.md` and doesn't read as AI-generated.

## Before editing

Read `writing/persona.md` in full. Check the draft against the "Imitation checklist" section
first — it's the 5 most load-bearing traits, so a draft that fails one of those is worth
flagging before a full section-by-section pass. Then use the "AI-tell checklist" section,
which lists the specific AI-sounding patterns this person's real writing does NOT contain,
as the primary thing to check the draft against. If `writing/persona.md` is missing, stop
and say the `profile` skill needs to run first.

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
