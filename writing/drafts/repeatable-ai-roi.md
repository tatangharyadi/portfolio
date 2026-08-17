# Repeatable ROI from an AI-applied engineering team means building tools, not pilots

When people ask how to get repeatable ROI out of an AI-applied engineering team, the answer
they're hoping for is usually a workflow: adopt some tool, write a few good prompts, ship a
demo, count the hours it saved. That's not repeatable ROI. That's a pilot, and pilots decay
the moment the person who built them moves on to the next thing.

I've watched this happen often enough that I think it's worth being blunt about it: an
AI-applied engineering team that doesn't build its own tooling is going to produce a string
of one-off wins that don't compound, and that probably won't survive the person who built
them leaving the team. The wins are real. They just don't repeat, which is the entire point
of the word "repeatable."

Here's what I mean by "tooling," concretely, because "invest in tooling" is vague enough to
be useless as advice on its own.

#### An agent-aware workspace

Somewhere between a terminal and an IDE, there's a missing piece: something that shows you
what an agent is actually doing right now, across every session, without making you tab
through six terminal windows guessing which one is stuck. We built ours as fusion-ws — a
desktop workspace combining a PTY terminal, file tree, git panel, and editor in one window,
with a panel that shows every active agent session (Claude Code, Antigravity, Pi AI,
whatever else happens to be running) alongside its state and what it's blocked on. Token
usage is in there too. Arguably a small thing. It's also the difference between noticing a blocked session in
five seconds and noticing it twenty minutes later because someone finally thought to check.

The instinct, when you first start running agents against real work, is to just keep more
terminal tabs open. That works fine for a demo. It stops working the first week someone's
actually running six sessions at once against six different repos and has no way to tell,
at a glance, which one has been sitting there blocked for the last twenty minutes.

There's a second, smaller thing this kind of workspace buys you, which is a plan step before
the agent touches anything. One model proposes an approach. A second, different model attacks
it, looking for holes. Only then does the actual implementation start. It's a bit of extra
latency up front. It's cheap compared to the alternative, which is discovering the
hole after the agent has already rewritten half a module around a wrong assumption.

#### A shared skills repo, not six copies of the same prompt

The second failure mode is quieter and takes longer to notice: every engineer who wants an
agent to do something non-trivial ends up writing their own version of the instructions for
it. One person writes a decent prompt for "create a PR the way our team actually does it."
Someone else, on a different project, writes almost the same prompt, slightly worse, because
they had no way of knowing the first one existed. Multiply that by however many repeatable
workflows a team actually has — starting a ticket, scaffolding a project, running a security
scan, whatever it is — and you end up with N slightly-different, slightly-wrong versions of
the same handful of workflows, with no way to fix all of them at once when one of them turns
out to be wrong.

The fix we landed on was a shared plugin/skills repo (ours is called fusion) that every
project pulls from — Claude Code plugins for things like starting a Jira issue, creating a
PR against the team's actual conventions, running project scaffolding, generating a code
graph for the agent to reason about. When the "create a PR" skill is wrong, you fix it once,
and every project using it gets the fix the next time an agent runs it. That's the entire
difference between tooling and a folder of someone's old prompts.

I'd guess maybe a third of the actual value here isn't even the skills themselves, it's that
fixing one now touches every team that uses it, so whoever finds a real gap in a skill is at
least mildly incentivized to fix the shared version instead of quietly working around it in
their own repo[^1].

#### A CLI that scaffolds instead of a wiki page that explains

The third piece, and maybe the most boring-sounding one, is a scaffolding CLI. Every team
accumulates a "here's how we set up a new service" wiki page, and the wiki page rots, because
updating docs is the first thing that gets skipped when you're two weeks from a deadline. If
setting up a new web app with the right auth pattern, or a new API with the right structure,
is actually a command — fusion-cli scaffold, in our case — instead of a set of steps someone
has to remember to keep current, then "how we do things" lives in code that runs, not in a
doc nobody's touched since March.

This also happens to be the one place where the ROI is easiest to make legible to someone who
isn't already convinced. "This used to take a day of copy-pasting from whichever old project
got it mostly right" is a sentence a skeptical manager understands instantly. "We improved
developer experience" is not.

The same CLI is also where the quality gate lives, if you're doing this right: static
analysis and a security scan catch roughly what a human reviewer would catch. The more
interesting piece is the code graph, since that's what lets an agent actually reason over
the codebase's structure instead of re-discovering its shape from scratch every session.
None of that is glamorous. It's the difference between an agent that scaffolds something and
an agent that scaffolds something that then passes the same checks a human's PR would have
to pass.

### Why this is the unglamorous option

None of this is exciting to build. A scaffolding CLI does not get you a conference talk. A
skills repo that quietly removes duplicate prompts is, on its face, less impressive than
shipping some flashy agent demo that closes a ticket end-to-end on stage. But the demo
doesn't repeat. It's a single data point, run once, by someone who understood the whole
problem well enough to hand-hold the agent through it. The tooling is what lets the
fortieth person on the team get the same result as the first, without needing to understand
the whole problem themselves.

If I had to guess at why teams reach for the demo instead of the tooling, it's that the
tooling takes longer to show a return and it's boring in a way that doesn't look like "doing
AI" to anyone watching from outside the team. Nobody puts "wrote a CLI flag parser" in a
promo packet. But I'd bet that almost none of the teams chasing flashy one-off agent wins
can point to a second project where the same win repeated without someone rebuilding it from
scratch.

### What "repeatable" actually requires

Repeatable, in practice, seems to require a handful of things that have nothing to do with
which model you're using: a place agent activity is visible enough that a blocked or
wandering session gets noticed in minutes instead of the next stand-up; a shared, versioned
home for the workflows an agent needs to know, so fixing one thing fixes it everywhere at
once; a way to turn "here's how we set this up" into a command instead of a memory; and
some way to check, after the fact, whether any of this actually saved time, so the case for
the next tool isn't just vibes.

None of those four are model-dependent. Swap out every model behind these tools tomorrow and
the ROI argument wouldn't change much, which is probably the actual test of whether you're
doing something repeatable or just riding whatever the current model happens to be good at
this month.

### Appendix: tooling doesn't fix incentives, it just removes one excuse

None of the three things above will save a team where building the shared tooling is worth
zero to whoever would have to build it. If the org rewards the person who ships the flashy
one-off demo and gives no credit to whoever spent a month on a scaffolding CLI that quietly
saves everyone else a day per project, people will keep building the demo. That's not a
failure of judgment, it's just what the incentives are asking for.

I think this is the more honest way to frame "why doesn't every team already do this": it's
not that people haven't thought of it, it's that maintaining a shared skills repo or a
scaffolding CLI is exactly the kind of unglamorous, hard-to-put-in-a-promo-packet work that
individual incentives push people away from, even on a team that's otherwise well aligned
with what's actually good for the org. Someone has to be willing to own the boring version
of the work anyway. Tooling doesn't remove that requirement. At best it removes the excuse
that repeatable ROI wasn't possible.

---

[^1]: This isn't automatic — I've also seen the opposite, where someone hits a gap, works
around it locally because fixing the shared version means touching a repo they don't feel is
"theirs," and the gap just sits there for the next person to rediscover. Ownership of the
shared repo matters almost as much as the repo existing in the first place.
