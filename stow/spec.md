# GNU Stow — 2026 Edition

## What You're Building

A replacement for **GNU stow**, a symlink farm manager. Stow takes packages from a source directory and "installs" them into a target directory by creating symlinks. It's the tool people use to manage dotfiles, or to install software from source into `/usr/local`.

The original stow was written in Perl in 1993. You're building the 2026 version.

## How Stow Works (Conceptual)

```
Source tree (~/dotfiles):        Target tree ($HOME):
  bash/                            .bashrc  →  ~/dotfiles/bash/.bashrc
    .bashrc                        .bash_profile → ~/dotfiles/bash/.bash_profile
    .bash_profile               
  vim/                             .vim/    →  ~/dotfiles/vim/.vim/
    .vim/                          .vimrc   →  ~/dotfiles/vim/.vimrc
      colors/
        solarized.vim
    .vimrc
```

- `stow bash` creates symlinks in `$HOME` pointing into `~/dotfiles/bash/`
- `stow vim` does the same for vim — merges into the same target tree
- `stow -D bash` removes (unstows) the bash symlinks
- Conflicts: if `.bashrc` already exists as a real file (not a stow symlink), stow reports it

## Required Features

### Core Operations
- **Stow** (install): Create symlinks from a source package into the target directory
- **Unstow** (uninstall): Remove symlinks that were created by a previous stow operation
- **Restow**: Unstow then stow (useful after updating a package)
- **Dry-run**: Show what WOULD happen without actually doing it (`-n` / `--dry-run`)

### Conflict Handling
- Detect when a target path already exists as a real file (not a symlink)
- Detect when a target path is a symlink owned by a DIFFERENT package
- Report conflicts clearly, don't just fail silently
- Option to `--force` (override conflicts) or `--skip` (skip conflicting files)

### Safety & Correctness
- Symlinks must be relative, not absolute (survives moving/renaming parent directories)
- Operations should be idempotent: stowing an already-stowed package is a no-op
- Unstowing should only remove symlinks that point back to the correct package
- Never delete real files — only symlinks the tool created

### UX
- Clear CLI interface with good help text
- Verbose mode (`-v`) showing what's happening
- Reasonable error messages (not just "failed")
- Support for specifying target directory (`-t /path/to/target`)

## Freedom

You choose everything:
- **Language**: Go, Rust, Python, Zig, whatever you think is right for a CLI tool in 2026
- **Architecture**: Monolithic, modular, whatever pattern serves the problem
- **Libraries**: Use the standard library, bring dependencies, your call
- **Testing strategy**: Unit tests, integration tests, both, neither — but be ready to justify it

## Evaluation Criteria

What makes a good submission:
1. **Correctness**: Does it actually work? Symlinks correct? Conflict detection solid?
2. **Robustness**: Edge cases handled? Relative symlinks? Idempotent operations?
3. **UX**: Is the CLI pleasant to use? Good help text? Clear error messages?
4. **Code quality**: Readable? Well-structured? Appropriate abstractions?
5. **Tests**: Do they exist? Do they pass? Do they test meaningful behavior?

## Deliverables

A working CLI tool that can be invoked like:
```bash
./stow [--target /path] [--dry-run] [--verbose] [--force|--skip] <package>
./stow -D [--target /path] [--dry-run] [--verbose] <package>
```

Plus any tests, documentation, or build files needed to run and verify it.
