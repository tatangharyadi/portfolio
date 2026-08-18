# Managing an AI-applied engineering team is mostly token discipline

A team of AI-applied engineers doesn't fail because the model is bad. It fails because
nobody mapped which task should cost how many tokens, and by the time anyone notices, the
bill already explains it.

I've watched a team burn a week's budget on tasks that should have taken an afternoon.
Nobody set a ceiling. Nobody asked what a routine refactor should cost versus what a
genuine multi-file migration should cost. The agent just kept running until someone
glanced at the invoice and asked why a linting pass cost as much as a rewrite.

The first job is mapping tokens to tasks before the work starts, not after the bill
arrives. A quick lookup fix gets a small budget and a low-effort model. A cross-repo
migration gets a bigger one, on purpose, because the task actually needs it. Skip that
mapping and every task defaults to whatever the harness happens to reach for, which is
usually more than it needs.

The harness matters as much as the mapping does. Though I'd rather blame a careless
engineer, the truth is usually the setup. An agent that re-reads the same file five times
because nothing cached the context wastes tokens no ceiling would have caught. A review
step skipped because the pipeline never wired it in does the same, quietly.

Repeatable quality is the harder half of this problem. If the same task run twice produces
two different outcomes, token diligence doesn't mean much, since you're paying twice to
find out which run you can trust. Fixing that means giving the harness an owner and a
version number, then testing it against a known task before trusting it against a new one.

None of this is exciting work. Terrific. It's also the entire job, once a team is running
enough agents that nobody can watch every session by hand.

A team with real token discipline scales its AI usage. A team without it just scales its
bill.
