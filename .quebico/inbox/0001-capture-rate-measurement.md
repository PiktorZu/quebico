# 0001 — How the capture rate gets measured

**Decided:** the denominator of Quebico's own capture rate is **every merged pull
request**. Each PR must either add at least one file under `.quebico/inbox/` or state
the exact line `Decisions: none` in its description; the numerator is the PRs that did
one of the two. Missed records are never backfilled. Nothing reaches `main` outside a
PR.

**Why:** the capture problem — records stop being written, so the tool starves — is what
killed thirty years of design-rationale research, and it is the risk this project is
least able to argue its way out of. It has to be measured on real behaviour, which means
the denominator must be observable *after the fact, from evidence nobody had to remember
to produce*. Merged PRs are exactly that: git history records them whether or not anyone
was paying attention. Backfilling is banned for the same reason — a record written later,
once the gap is noticed, measures the noticing, not the capturing. The misses are the
data, not a mess to tidy.

The `main`-only-through-PR clause was added on 2026-09-15 after a real miss: the Step 0
bootstrap was committed straight to `main`. That commit would have been invisible to the
measurement — neither numerator nor denominator — which showed that the PR rule is not
enforceable without it. Fittingly, the incident is itself the first piece of evidence
that this convention is needed.

**Rejected:**

- *A manual capture log* (one line per work unit in a file). Rejected because its
  denominator depends on remembering to append to it — the instrument would be subject
  to the very failure it is meant to detect.
- *Sessions as the unit of work.* Rejected because session boundaries leave no trace in
  the repository, so the count could never be re-verified by anyone, including future me.
- *No fixed denominator; judge capture by feel at review time.* Rejected under the
  project's meta-rule: a check that cannot be settled yes or no is not a check.
- *Branch protection on GitHub instead of a written rule.* Deferred rather than rejected
  — the rule belongs in `CLAUDE.md` either way, because the agent doing the work needs to
  read it, and a solo repository does not yet need the enforcement machinery.

**Consequence:** capture rate is not judged at all until the denominator reaches 10
merged PRs.
