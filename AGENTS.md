# AGENTS.md — Ghostwriter

Agent behavioral guidelines for the `ghostwriter` plugin (`plugins/ghostwriter/`) and the
`writing/` workspace it operates on.

## Setup

No install step beyond the plugin itself. Add the repo-local marketplace once
(`.claude-plugin/marketplace.json` already declares it) and enable `ghostwriter`. The three
skills — `profile`, `writer`, `editor` — read and write only under `writing/`; nothing here
touches the portfolio site content (`index.html`, `style.css`).

## Scope

This plugin exists to draft content that sounds like one specific person, not generic AI
prose, and to catch it when it doesn't. It covers:

- **Voice extraction** — turning real writing samples into a falsifiable persona description.
- **Drafting** — new posts/articles/copy written against that persona.
- **Grading** — an independent, adversarial check of a draft against the persona before it
  ships.

**Not in scope:**
- House styles blended from multiple authors — `profile` describes one person's voice; see
  **Single-author rule** below.
- Editing the portfolio site itself (`index.html`, `style.css`) — unrelated to this plugin.
- Publishing or posting anywhere — these skills only produce local files under `writing/`.

## Skill Workflow

Run in this order; each skill hands off a specific file to the next:

1. **`profile`** — reads writing samples, writes `writing/persona.md`. Saves any raw samples
   handed to it under `writing/samples/`. Run once per person, and re-run (refresh mode) when
   new samples arrive for the same person.
2. **`writer`** — reads `writing/persona.md`, drafts new content, saves to
   `writing/drafts/<slug>.md`. Runs its own fabrication scan and a persona-fidelity self-check
   before calling a draft done — but does **not** scan for triads; see below.
3. **`editor`** — grades a file in `writing/drafts/` (or pasted text) against
   `writing/persona.md`. Checks two hard gates first (accuracy/integrity, triad structure),
   then eight weighted checks, for a 0-100 score and a READY / MINOR REVISION / NEEDS REVISION
   verdict. Hands back a prioritized fix list — it does not rewrite the draft.
4. If `editor` returns anything short of READY, hand its fix list back to `writer`'s revision
   mode: surgical fixes only to the flagged lines, then back to `editor` for an independent
   re-check. Don't let `writer` self-grade a revision.

**Triad-scanning boundary:** `editor`'s hard gate is the sole authority on rule-of-three
sentence structures — zero tolerance, checked exhaustively. `writer` used to duplicate this
check in its own before-finalizing pass; it was dropped because a self-scan run by the same
pass that generated the prose caught only 1 of 3 real hits in one drafting session, while
`editor` caught all of them, and a surgical revision-mode fix to the flagged lines (no
self-scan) didn't introduce a new one on that same draft. That's still a small sample —
if a future draft ships with a triad `editor` should have caught, that's worth re-examining
before assuming the split is wrong.

## Fabrication Discipline

One rule, enforced three separate ways — state it once here instead of re-deriving it from
each skill:

- **`profile`** — every trait it claims must trace to a quoted snippet from a real sample; no
  invented traits.
- **`writer`** — tags every specific factual claim (name, number, date, stat, attributed
  quote) and confirms it traces to the brief, to `writing/persona.md`, or is clearly fictional
  detail inside an intentionally fictional piece. Anything else becomes `[PLACEHOLDER]`, never
  a filled-in guess.
- **`editor`** — gates on this first, before any scored check: any unmarked invented fact,
  statistic, name, or quote presented as factual is an automatic NEEDS REVISION.

Never invent a fact, number, name, or quote to make a draft or persona read more smoothly. A
flatter true sentence, or a visible `[PLACEHOLDER]`, beats a smooth invented one.

## AI-Tell Patterns

Avoiding AI-sounding prose is the reason this plugin exists (see `plugin.json`'s description),
not just one check among many. The canonical pattern list lives in
`plugins/ghostwriter/skills/editor/SKILL.md` under **Hedging & directness**,
**Overused-word clusters**, and **Formatting & mechanical tells** — that's the authoritative,
maintained list; read it there rather than trusting a copy here that could drift out of sync.

`profile`'s persona-specific **AI-tell checklist** section can override a hit on this general
list — e.g. a persona that documents heavy em-dash use isn't penalized for em dashes just
because the general list is wary of them. Persona-documented exceptions always win over the
generic pattern.

## Single-author rule

`profile` builds a persona around one person's writing, not a blended "house style." Before
running `profile`, confirm all writing samples share one author — mixing authors produces a
persona that's true of neither one, and any `writer`/`editor` output built from it inherits
that fiction. If samples turn out to be multi-author mid-run, flag it to the user rather than
merging silently, and prefer rebuilding from the single largest-author subset over shipping a
blended profile.

## persona.md Quality Standard

A usable `writing/persona.md` should have, for every trait it claims:

- **A quoted example** from a real sample — no trait without supporting text.
- **A concrete number where the section calls for one** — sentence-length range,
  `Contraction baseline`, `Ornament baseline` — not a vague "sometimes" or "often."
- **An explicit confidence level** (`low`/`medium`/`high`) tied to sample count/word count,
  not an assumed default.
- **A "Never does" section** — absence patterns are as identifying as presence ones, and are
  what `editor`'s AI-tell checklist checks against.

Keep the file under ~150 lines (per `profile/SKILL.md`) — it's a working reference for
`writer`/`editor`, not an essay about the person.

## Directory Conventions

- `writing/samples/` — raw source material `profile` was given, kept so future refresh runs
  don't need the user to re-supply them.
- `writing/persona.md` — the single active persona. `profile` overwrites this on every run
  (refresh mode merges in new evidence rather than discarding prior analysis).
- `writing/drafts/<slug>.md` — one file per draft; `writer` creates, `editor` grades in place,
  `writer`'s revision mode overwrites the same file rather than creating a new one.

## Autonomous vs. Ask-First

**Autonomous (no confirmation needed):**
- Running `profile`, `writer`, or `editor` when the request clearly names a skill or task.
- `writer`'s revision mode applying a fix list `editor` already returned.
- Saving samples/drafts/persona files under `writing/`.

**Ask first:**
- Running `profile` against samples from more than one author (see **Single-author rule**).
- Proceeding with `writer` when `writing/persona.md` is marked `Confidence: low` — confirm
  whether to draft anyway or gather more samples first (per `writer/SKILL.md`).
- Publishing, posting, or sending a draft anywhere outside this repo.
- Anything that would name real internal tools, employers, or people in a draft meant for
  external/public use — flag before the user publishes, even if the facts are accurate.

## Session End

- If a draft was graded this session and came back MINOR REVISION or NEEDS REVISION, note the
  outstanding fix list before ending — don't let a graded-but-unfixed draft look finished.
- Commits/pushes for `writing/` changes follow the same repo-wide rule as everything else
  here: only when asked, via a branch + PR, never a direct commit to `main`.
