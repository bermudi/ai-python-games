# Planning Phase

## ⚠️ Sandbox
**Work ONLY within your current directory.** Do not read, write, or modify any files outside it. The spec and all context files you need are already here.

## 0 — Orientation

Before anything else:
0a. Read `spec.md` carefully. Understand what stow does and what's expected.
0b. Check if `IMPLEMENTATION_PLAN.md` already exists. If it does, you're in a follow-up planning iteration — review it, identify gaps, refine.
0c. Check git status (`git status`). A git repository is already initialized. Understand the current state.

## 1 — Domain Understanding

1a. Make sure you understand the core stow concept: a symlink farm manager that mirrors a source package tree into a target directory via relative symlinks.
1b. If needed, research the original GNU stow to understand its behavior (conflict detection, tree folding, relative symlinks). The goal isn't to clone it — it's to understand the problem space so you can design something better for 2026.

## 2 — Architecture Decisions

Make concrete decisions and document your reasoning:
2a. **Language**: What language fits this task best in 2026? Consider ergonomics, deployment story (single binary?), standard library support for file system operations, error handling patterns.
2b. **Dependencies**: What libraries will you use? Argparse library? Testing framework? Prefer standard library unless there's a strong reason.
2c. **Module structure**: How will you organize the code? What are the key modules/components?
2d. **Testing strategy**: How will you verify correctness? Manual test scenarios? Automated tests? What edge cases matter?

## 3 — Implementation Plan

Create or update `IMPLEMENTATION_PLAN.md`. Structure it as a clear, ordered list of implementation steps. Each step should be concrete and verifiable, for example:
- "Initialize project with build system and dependency manifests"
- "Implement path resolution: compute relative symlink target from package file to target destination"
- "Implement tree scanning: walk source package, map each file to its target path"

Order the steps logically — foundations first, polish last. The plan is what the build phase will follow step by step, so make it actionable.

## 4 — Completion

When you're satisfied the plan is thorough and complete:
4a. Create an empty file called `PLAN_READY` (use `touch PLAN_READY`). This signals the orchestrator to move to the build phase.
4b. Commit your plan: `git add IMPLEMENTATION_PLAN.md PLAN_READY && git commit -m "Implementation plan complete"`

## Guardrails

- **Don't implement anything yet.** This phase is planning only. Write the plan, not code.
- **Don't create project files, source code, or dependency manifests.** That's the build phase.
- **Be specific in the plan.** "Implement stow command" is not a step. "Parse CLI arguments using <library>, map to Stow/Unstow/DryRun operations" is.
- **Think about edge cases.** Relative symlinks, nested directories, existing files, race conditions, symlink chains. The plan should acknowledge these.
- **The plan file IS the deliverable.** Make it detailed enough that another engineer could execute it without asking questions.
