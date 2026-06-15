# Build Phase

This is an iterative build phase. You may be called multiple times. Each invocation, pick up where you left off by reading the plan.

## ⚠️ Sandbox
**Work ONLY within your current directory.** Do not read, write, or modify any files outside it. All project files, spec, and plan are here.

## 0 — Orientation

0a. Read `IMPLEMENTATION_PLAN.md`. Find the first incomplete task.
0b. Read `spec.md` if you need to reference the requirements.
0c. Check git status (`git status`). A git repository is already initialized with any previous work committed.

## 1 — This Iteration

1a. Pick the **topmost unfinished task** from `IMPLEMENTATION_PLAN.md`. Implement exactly that task — nothing more.
1b. Write code. Make it clean — this is the 2026 version, not a Perl script from 1993.
1c. If the plan calls for tests on this task, write them now. Tests should verify actual behavior.
1d. Make sure code compiles/passes lint before moving on.
1e. Update `IMPLEMENTATION_PLAN.md` — mark the completed task as done (e.g., `[x]` or `DONE`).
1f. Commit with a meaningful message: `git add -A && git commit -m "description of what was implemented"`

## 2 — Integration Testing (First Iteration Only)

If this is the first build iteration (no code exists yet):
2a. Set up the project according to the plan: dependency manifests, build system, directory structure.
2b. Commit the scaffold: `git add -A && git commit -m "Project scaffold"`

## 3 — Completion Check

After completing your task, check if ALL tasks in `IMPLEMENTATION_PLAN.md` are marked done. If so:
3a. Verify the tool works end-to-end:
  - Create a test stow directory with a couple of packages
  - Run the tool to stow a package — verify symlinks are created correctly with relative paths
  - Run unstow — verify symlinks are removed and real files are untouched
  - Test dry-run mode
  - Test conflict detection (real file in the way is reported, not silently clobbered)
3b. Run any automated tests. Fix failures.
3c. If everything passes, create an empty file called `BUILD_DONE` (use `touch BUILD_DONE`).
3d. Final commit: `git add -A && git commit -m "Build complete — stow 2026"`

If tasks remain, just commit your work and exit. The orchestrator will invoke you again for the next task.

## Guardrails

- **One task per invocation.** Don't try to implement the entire plan in one shot. Focus on the next unfinished task.
- **Mark tasks done in the plan file.** This is how the next invocation knows what's left.
- **Relative symlinks are the core correctness property.** Symlinks must be relative, not absolute.
- **Never delete real files.** Only remove symlinks you created.
- **Idempotency matters.** Stowing an already-stowed package should be a clean no-op.
- **If you hit a bug from a previous iteration, fix it before moving on.** Don't let errors compound.
