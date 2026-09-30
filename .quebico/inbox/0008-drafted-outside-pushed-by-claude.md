# 0008 — Changes are drafted outside the repository and pushed by Claude as pull requests

**Decided:** a change starts as a draft in the maintainer's project folder, outside this
repository, where plans and article drafts already live, and is refined there in
conversation with Claude. When the maintainer says the draft is finished, Claude, working
from its own cloud session, cuts a branch from the latest `main`, commits the draft,
pushes, and opens a pull request. The maintainer reviews the diff on GitHub and merges.
The WSL clone stays for running things locally and only pulls. This replaces the
arrangement set during planning, in which development happened in the WSL clone.

**Why:** the old route cost a round of manual steps for every change: copy the draft into
the WSL clone, commit, push, open the pull request. Copying from the Windows drive also
set the executable bit on text files (cleared in #3). Claude's cloud session can push and
open pull requests through the maintainer's GitHub connection, and the `protect-main`
ruleset (0007) rejects anything that would reach `main` without a pull request, so the
shorter route keeps everything 0001 and 0007 protect. Tests and tools run in Claude's
clone on a Linux filesystem, so the reason the working clone was kept off the Windows
drive — tooling too slow there — does not come back.

**Rejected:**

- *Copying drafts into the WSL clone by hand.* The route this replaces.
- *A clone inside the maintainer's project folder, pushed from there.* Claude can reach
  files on the maintainer's machine but not their GitHub credentials; making it work
  would mean leaving a token where an agent can read it.
- *Running Claude Code inside the WSL clone.* It works, but it separates the
  implementation from the conversation where plans and decisions are made.

**Premise:** Claude's cloud session can push and open pull requests through the GitHub
connection (confirmed 2026-09-30 with #3). If that stops holding, the fallback is the WSL
clone.

**Note for the capture measurement:** Claude now opens the pull requests and applies the
capture rule — an inbox file or `Decisions: none` — as it opens them. The Step 3 capture
rate will therefore measure recording with Claude in the loop, not unprompted recording
by a person, and whether a `Decisions: none` is right now rests mostly on Claude's
judgment of what counts as a decision.
