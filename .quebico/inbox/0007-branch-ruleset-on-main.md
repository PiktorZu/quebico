# 0007 — `main` is protected by a ruleset

**Decided:** a GitHub branch ruleset protects `main`. Changes land only through a pull
request, with zero required approvals so a solo maintainer can merge their own; force
pushes and deletion are blocked; and the bypass list is empty, so administrators are
bound too. This reverses the deferral recorded in 0001.

**Why:** 0001 deferred enforcement because a solo repository did not seem to need the
machinery and a written rule would do. The written rule did not hold. On 2026-09-15 it
reached `main` with PR #2 at 23:57, and at 23:59 a commit went straight to `main`
(`14a0c7e`, moving 0001 into the inbox). That was the second direct commit that day;
the first was caught locally before it was pushed. A change that skips the PR is missing
from both the numerator and the denominator of the capture rate, so this rule protects
the measurement itself. The setting takes minutes and can be switched off.

**Rejected:**

- *Relying on the written rule.* It failed twice in one day.
- *Protection that exempts administrators*, the default for classic branch protection
  rules. The only person pushing here is the administrator, so exempting administrators
  would protect nothing.

**Consequence:** every change, one-line fixes included, goes through a PR, which is what
0001 already asked for.
