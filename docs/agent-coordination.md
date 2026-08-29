# Agent coordination

This document defines the shared work process for Room 3. It applies to people
and agents that change this repository.

## Sources of truth

Use one GitHub Issue for each work item. The Issue records the intended result,
the owner, the affected paths, and the acceptance criteria.

Use these sources in this order:

1. Tests, examples, and executable checks.
2. Repository requirements and the content canon.
3. The assigned Issue and accepted decisions in that Issue.
4. Meeting notes and chat messages.

If two sources conflict, mark the Issue as `blocked`. Quote both sources and
ask the room leader for a decision. Do not select a source without that decision.

## Work item lifecycle

Use these Issue states:

| State | Meaning | Required action |
| --- | --- | --- |
| `ready` | The scope and owner are clear. | The owner can start work. |
| `in progress` | The owner is changing the assigned paths. | Other contributors do not change these paths. |
| `blocked` | A decision, dependency, or access right is missing. | Describe the blocker and the requested decision. |
| `in review` | A pull request contains the proposed change. | Review the acceptance evidence. |
| `done` | The change is merged and the evidence is recorded. | Close the Issue. |

The room leader maintains the Issue states. The contributor updates the Issue
at start, on block, before review, and after an owner change.

## Issue contract

Create an Issue before you change files. Every Issue must contain:

- **Outcome:** A short description of the user-visible or acceptance result.
- **Owner:** One accountable person or agent.
- **Paths:** The files or directories that the owner can change.
- **Acceptance criteria:** Observable conditions for completion.
- **Dependencies:** Related Issues, decisions, or interfaces.
- **Verification:** The command or example that gives evidence.

Use this template:

```md
## Outcome

## Owner

## Paths

## Acceptance criteria

## Dependencies

## Verification
```

An Issue can have multiple helpers. It has only one owner. If two owners must
change the same file group independently, split the work.

## Path ownership

Claim the smallest path group that completes the work. Record it in the Issue.
For shared files, such as `README.md`, `AGENTS.md`, and integration code, ask
the room leader to assign the change.

Before you edit a file:

1. Read open Issues and pull requests that name the file.
2. If another active Issue owns the file, contact its owner in that Issue.
3. If the work overlaps, agree on one owner or split the file boundaries.
4. Record the decision in the affected Issue before you edit the file.

## Branch and pull request rules

Create one branch for one Issue. Use the branch name format
`<participant-code>/<short-topic>`.

A pull request must link its Issue and include:

- The result that the change provides.
- The changed paths.
- The verification command and its result.
- Known limits or follow-up work.

Do not push directly to `main`. The room leader or assigned integrator merges
approved pull requests.

## Handoffs and blockers

Use the Issue to hand work to another contributor. State:

- What is complete.
- Which branch and pull request contain the work.
- Which files the next owner can change.
- What remains to do.
- Which verification result already exists.

If a required decision or dependency is missing, set the Issue state to
`blocked`. State the question in one sentence and name the person who can
decide it.

## Integration order

Merge shared interfaces before modules that depend on them. Then merge format
modules. Run all examples after each integration.

If an integration changes an agreed interface, update the affected Issues before
you ask their owners to rebase or change their work.

## Current acceptance boundary

The Room 3 acceptance set is in `examples/`. It covers proofread content, a
reels script, and a weekly digest. The content canon is in
`examples/canon.md`.

The evaluator records each example as pass or fail. The final demo reports the
number of passed examples and the customer verdict.
