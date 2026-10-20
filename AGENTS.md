# Room 3 agent rules

Read this file before you change this repository. Then read
[`docs/agent-coordination.md`](docs/agent-coordination.md).

## Goal

Build one content pipeline that passes the examples in `examples/`.
The examples and `examples/canon.md` define the acceptance behavior.

## Work ownership

- Use a GitHub Issue for each work item.
- Claim one Issue before you edit files.
- State the owner, target paths, acceptance criteria, and dependencies in the Issue.
- One active owner can change one path group at a time.
- Do not edit a path that another active Issue owns. Ask the owner or room leader first.

## Change flow

1. Read the Issue, this file, and the applicable example.
2. Create a branch from the current integration branch.
3. Make only the changes that the Issue describes.
4. Run the applicable examples and record the result in the pull request.
5. Open a pull request that links the Issue.
6. Wait for review and integration. Do not push directly to `main`.

## Source priority

Use these sources in this order:

1. Tests, examples, and executable checks.
2. `README.md`, `examples/README.md`, and `examples/canon.md`.
3. The assigned GitHub Issue and its accepted comments.
4. Meeting notes and chat messages.

If two sources conflict, stop work. Describe the conflict in the Issue and ask
the room leader for a decision.

## Safety and scope

- Do not add secrets, API keys, private customer material, or unredacted recordings.
- Do not change `examples/` or `examples/canon.md` unless the Issue explicitly assigns that work.
- Do not rewrite unrelated files while resolving a conflict.
- Keep commits small and state what changed.

## Communication

Use the GitHub Issue for decisions, blockers, ownership changes, and handoffs.
Use the pull request for implementation evidence and review discussion.
The detailed templates and status rules are in
[`docs/agent-coordination.md`](docs/agent-coordination.md).
