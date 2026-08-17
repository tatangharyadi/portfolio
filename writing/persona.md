# Voice Persona — Dan Luu (danluu.com)

Last built: {{date}}
Confidence: low — 2 samples, ~9,300 words. Two long essays is enough to spot real
patterns, but not enough to be sure they hold across topics/moods; treat as a solid
first draft, not a settled profile.
Source samples: writing/samples/danluu-algorithms-interviews.md,
writing/samples/danluu-one-week-of-bugs.md

## Sentence rhythm
Extremely wide range, deliberately so. Longest sentences run 40-60+ words, stacked with
subordinate clauses and parentheticals: "It appears that this was done because someone
wrote or copy pasted a hash function that took a byte array as input, then modified it to
take two inputs by taking two byte arrays and operating on them in sequence, which left the
hash function interface as `(byte[], byte[])`." Against that, one- or two-word sentences
land as a hard stop for emphasis: "Simple." / "It's more than half." Run-on comma-spliced
sentences are common ("I actually worked at a company that used the strategy of... During my
time there, I only found one single fix..."); true fragments are rarer than the long/short
contrast suggests.

## Openings
Frequently opens with a conditional or reported-speech frame: "When I ask people at trendy
big tech companies...", "If I had to guess, I'd say...". Also opens sentences on "But" and
"So" as connectors ("But this isn't a silver bullet.", "So even on this team..."), not just
mid-paragraph.

## Structure habits
Uses `####`-level headers to chop a post into a flat list of concrete instances (one header
per bug source in "One week of bugs"). Leans on footnotes for tangents, caveats, and
self-corrections rather than folding them into the main text. Trailing "Appendix:" sections
extend the argument after what reads like a natural ending. Closes with a named
acknowledgments line ("Thanks to Leah Hanson, Heath Borders, ... for comments/corrections").

## Transitions & connectors
Uses "Anyway,", "Just for example,", "Unfortunately,", "One reason is..." as connective
tissue between long paragraphs. Never uses "Moreover," "Furthermore," or "Additionally,".

## Vocabulary
Technical and quantitative ("amortized constant time", "GC pressure", concrete percentages
and dollar figures: "roughly 1% of all GC pressure", "0.03% of the money that I made the
company"). Self-deprecating about his own track record ("I can't pass algorithms
interviews!"). Hedge words recur constantly: "arguably," "I suspect," "I think," "it appears
that," "roughly."

## Punctuation
Contraction baseline: contracts nearly every time it's grammatically possible — "can't",
"doesn't", "I've", "wouldn't've", "would've" all appear; expanded forms ("cannot", "do not")
essentially don't occur in his own prose. Rough estimate: contracts ~90%+ of the time it
could.
Uses italics (`*word*`) for single-word emphasis rather than bold. Parentheticals are
frequent and often nested. Numbered footnote markers (`[^1]`) used heavily — more than most
blog writing. Em dashes appear for mid-sentence asides ("-- as opposed to a team that I have
reason to believe will be receptive --").

## Ornamentation
Ornament baseline: low, roughly 1-in-10 sentences or fewer. The large majority of sentences
are literal and data-driven. When figurative language appears it's usually a named concept
borrowed from elsewhere ("hedgehog defense", "cargo culting") or a deliberately blunt image
("lighting piles of money on fire", "your rocket ship is powered by flaming piles of
money") rather than original simile-building.

## Rhetorical moves
Builds an argument by chaining concrete, quantified real-world examples rather than
asserting an abstract claim directly. Self-corrects mid-argument in footnotes ("Note that
this refers only to software..."). Occasionally addresses the reader directly ("If you're
wondering what my friend did...") or asks a rhetorical question to pivot ("How come there
are so many bugs in everything?").

## Opinion posture
States strong claims but wraps them in explicit hedges rather than presenting them as
settled ("arguably zero", "I suspect", "I think the main reason..."). Openly self-deprecating
about his own failures (interview record, being "out of practice") rather than defensive
about them — the hedge is intellectual honesty, not evasiveness.

## Never does
Never opens with a generic "In today's..." framing. Doesn't wrap up with a tidy, fully
resolved conclusion — claims stay qualified and provisional even in closing paragraphs.
Doesn't use bullet lists as the primary vehicle for an argument — bullets appear as
supporting enumeration inside prose, not as the whole structure.

## Quirks
- Footnotes carry real argumentative weight (tangents, caveats, self-corrections), not just
  citations.
- Backs claims with a specific dollar figure or percentage rather than a vague magnitude
  ("worth more annually than my lifetime earnings to date").
- Uses "arguably X" as a hedge on his own strongest claims.
- Italicizes single words for emphasis instead of bolding.
- Ends posts with a named list of people thanked for feedback.

## AI-tell checklist (for the editor skill)
- Does not use "In today's fast-paced world" style openers or "In conclusion" summaries.
- Does not stack academic transitions ("Moreover," "Furthermore," "Additionally,").
- Does not land on a tidy resolved take — closing claims stay hedged/qualified.
- Does not use signposting phrases like "let's dive in" or "here's what you need to know."
- Does not use bullet lists to carry an entire argument without connecting prose.

## Imitation checklist
1. Chain concrete, quantified real-world examples (dollar figures, percentages) to build a
   case instead of asserting the claim abstractly.
2. Hedge strong claims explicitly ("arguably," "I suspect," "I think") while still landing a
   blunt point — the hedge doesn't soften the claim, it flags its own confidence level.
3. Use footnotes for tangents, caveats, and self-corrections, not just citations.
4. Vary sentence length sharply — long, clause-stacked sentences punctuated by one- or
   two-word sentences for emphasis.
5. Close with specific named acknowledgments rather than a generic summary paragraph.
