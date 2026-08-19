# AGENTS.md — Ghostwriter

Agent behavioral guidelines for the `ghostwriter` plugin (`plugins/ghostwriter/`) and the
`writing/` workspace it operates on.

## Setup

Add the repo-local marketplace once (`.claude-plugin/marketplace.json` already declares it)
and enable `ghostwriter`. The three skills — `profile`, `writer`, `editor` — read and write
only under `writing/`. `profile` and `editor` also shell out to
`plugins/ghostwriter/scripts/text_metrics.py`, a dependency-free Python 3 script (standard
library only) that computes sentence/paragraph/contraction/vocabulary-richness metrics
deterministically — no install step for it beyond having `python3` on PATH. Vocabulary
richness is two numbers (MATTR and MTLD), both length-robust and both running in the same
direction — see `profile/SKILL.md`'s Vocabulary fingerprints section for what each measures and
the minimum sample length they need.

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
- Publishing or posting anywhere — these skills only produce local files under `writing/`.

## Skill Workflow

Run in this order; each skill hands off a specific file to the next:

1. **`profile`** — runs `text_metrics.py` against each sample for sentence/paragraph/
   contraction/vocabulary-richness numbers, then reads writing samples qualitatively and writes
   `writing/persona.md`. Saves any raw samples handed to it under `writing/samples/`. Run
   once per person, and re-run (refresh mode) when new samples arrive for the same person.
2. **`writer`** — reads `writing/persona.md`, drafts new content, saves to
   `writing/drafts/<slug>.md`. Its only job is fact discipline (the fabrication scan) and
   matching the documented voice — it runs no AI-tell or structural-pattern check of any
   kind, not even a holistic one; all of that is `editor`'s job, entirely, and writer depends
   on the writer→editor loop to catch it. See **Pattern-checking boundary** below.
3. **`editor`** — also runs `text_metrics.py` against the draft first, then grades a file in
   `writing/drafts/` (or pasted text) against `writing/persona.md`. Checks three hard gates
   first (accuracy/integrity, triad structure,
   device density), then eight weighted checks, for a 0-100 score and a READY / MINOR
   REVISION / NEEDS REVISION verdict. Hands back a prioritized fix list — it does not rewrite
   the draft.
4. If `editor` returns anything short of READY, hand its fix list back to `writer`'s revision
   mode: surgical fixes only to the flagged lines, then back to `editor` for an independent
   re-check. Don't let `writer` self-grade a revision.
5. Once `editor` returns READY, move the file from `writing/drafts/<slug>.md` to
   `writing/published/<slug>.md` — this repo's staging area for pieces headed to Medium or
   dev.to. This is a local move only; see **Not in scope** above — actually posting to either
   platform still happens outside these skills.

**Pattern-checking boundary:** any AI-tell or structural-pattern check — triads, device
density, hedging, agency, overused words, formatting tells, ornament density, or any future
addition of the same kind — is `editor`'s job alone, never `writer`'s, in any form: not an
exhaustive scan, not a holistic self-check, not steering around the list while composing.
`writer`'s job is narrower than that: fact discipline (the fabrication scan) and matching the
documented voice in `writing/persona.md`. It fully depends on the writer→editor loop to catch
everything else — a draft that matches persona perfectly and still trips an `editor` check is
expected, not a sign `writer` should have caught it first.

This started narrower and got tightened twice. First, `writer` used to duplicate the triad
check as an exhaustive scan in its own before-finalizing pass — a self-scan run by the same
pass that generated the prose caught only 1 of 3 real hits in one drafting session, while
`editor` caught all of them; a surgical revision-mode fix to the flagged lines (no self-scan)
didn't introduce a new one on that same draft. That established: never duplicate `editor`'s
exhaustive gate-level scan inside `writer`. Later, `writer` still kept a lighter holistic
self-check ("what would make a skeptical reader call this AI-generated?") and general
AI-tell-list avoidance while composing — both cut on the reasoning that `editor` runs its
checks unconditionally either way, so a writer-side attempt at the same job buys nothing and
risks the same self-grading blindness the triad case demonstrated, just at lower stakes.
Neither cut has its own before/after evidence the way the triad case does; if a future draft's
`editor` score suffers from writer no longer even attempting AI-tell avoidance, that's worth
re-examining before assuming the fully-hands-off split is right.

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
**Agency & construction**, **Overused-word clusters**, and **Formatting & mechanical tells** —
that's the authoritative, maintained list; read it there rather than trusting a copy here that
could drift out of sync.

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
  `Contraction baseline`, `Ornament baseline`, `Vocabulary richness baseline` (MATTR and MTLD
  together, per `profile/SKILL.md`) — not a vague "sometimes" or "often."
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
- `writing/published/<slug>.md` — drafts that cleared `editor` with a READY verdict, staged
  for Medium or dev.to. Moved here from `writing/drafts/`, not copied — a slug lives in one
  place at a time.

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
