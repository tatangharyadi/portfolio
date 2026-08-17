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

Independent of the persona, scan for generic markers that make text read as AI-written
regardless of whose voice it's imitating. Each pattern below is something to recognize and
remove, never to imitate — treat any resemblance in the draft as a defect to fix, not a
style to preserve:

- Formulaic openers ("In today's...", "In the ever-evolving...", "Let's dive in"). Fix:
  delete the opener and start on the actual point.
- Empty transitions ("Furthermore", "Moreover", "That being said") used more than a real
  human would in this register. Fix: cut the transition word; let sentences sit next to
  each other or use a connector the persona actually uses.
- Symmetric list-of-three padding ("not only X, but also Y, and ultimately Z", or two
  three-item lists back to back) where the content doesn't need it. Fix: break the list —
  make one point, expand it with a real example, move on.
- Over-qualification / hedging on every claim ("it's important to note that", "arguably",
  "in many ways") stacked sentence after sentence. Fix: delete the hedge, say the thing
  directly.
- Tidy summary-conclusion paragraphs that restate what was just said, when nothing earlier
  called for one.
- Uniform sentence length and rhythm — real writing (and this persona specifically) has
  variance; a wall of same-length sentences, or a wall of same-shaped paragraphs (every
  one opening "Let's talk about X" or "X is essential because..."), is a tell on its own.
  Fix: collapse some sentences together, cut others to a fragment, vary paragraph openers.
- Em dash overuse beyond what the persona's punctuation profile documents.
- Perfectly balanced/parallel phrasing that no one would naturally speak, including hype
  constructions ("doesn't just X — it revolutionizes it", "not only enhances but also
  empowers", "unlock your full potential", "elevate to new heights"). Fix: state one plain
  claim about what the thing actually does, with a concrete result.
- Generic claims with no specifics ("many benefits", "many people have found it useful",
  "a variety of situations"). Fix: replace every vague claim with one real number, name,
  example, or scenario.
- Overused AI cliché vocabulary: "delve", "tapestry", "landscape" (as in "ever-evolving
  landscape"), "navigate this journey", "embark on", "crucial", "robust", "seamless".
  Fix: strip the cliché, state the point in plain words a real person would say out loud.
- Motivational-poster over-smoothness — no opinion, no friction, interchangeable with any
  other AI paragraph on the topic. Fix: add a real opinion, a specific detail, an aside, or
  a blunt line that only this persona would say.

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
