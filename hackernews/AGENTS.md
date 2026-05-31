# AGENTS.md

## What This Is

A side-by-side benchmark of LLM-generated Hacker News frontends. Each subdirectory is a complete implementation produced by a different model, deployed to Netlify under a shared domain.

## Structure

```
.
├── index.html              # Landing page linking to all implementations
├── .netlify/
│   └── netlify.toml        # Deploy config: publish = this dir
├── qwen3.7-max/            # Static HTML
├── kimi-k2.6/              # Vite + React + React Router
│   ├── index.html            # Built output (copied from app/dist/)
│   ├── assets/
│   ├── images/
│   └── app/                  # Source code + build artifacts
├── glm-5.1/                # Next.js (static export)
├── deepseek-v4-pro/        # Static HTML
├── gemini-3.5-flash/       # Static HTML
└── mimo-v2.5-pro/          # Static HTML
```

## Deployment

- **Host:** Netlify (`llm-hn-bench.netlify.app`)
- **Deploy command:** `netlify deploy --prod --dir=/home/daniel/build/llm-benchmarking/hackernews`
- Each implementation lives at a subdirectory path (e.g. `/kimi-k2.6/`)

## Subdirectory Gotchas

When fixing a React/Vite app deployed to a subdirectory:

1. **Routing:** Use `HashRouter`, not `BrowserRouter`. The server does not have SPA fallback rules for subdirectories. `<BrowserRouter basename="/kimi-k2.6">` also works but is fragile.
2. **Asset paths:** Set `base: './'` in `vite.config.ts` so JS/CSS bundles use relative paths.
3. **Runtime image paths:** Any hardcoded `/images/foo.jpg` must become `./images/foo.jpg` or be made relative to the current URL. Otherwise they 404 when served from `/kimi-k2.6/`.

## Build Conventions

- Static HTML implementations: commit the raw files directly.
- Vite/React implementations: keep source in `app/`, build with `bun run build`, then copy `app/dist/*` to the subdirectory root. Do not commit `app/node_modules/`.
- Next.js implementations: export to static HTML, commit the exported files.

## Quality Bar

If an implementation is broken in production, fix the source, rebuild, copy to the subdirectory root, deploy, and commit the updated built files.
