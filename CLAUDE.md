# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Personal portfolio website for Piyush Maiti (computational biomedical imaging researcher, Machine Learning/AI Engineer at Whissle.ai, amateur photographer). Static HTML/CSS/JS — no build tools, no frameworks, no dependencies. Hosted on GitHub Pages with the custom domain `piyushkmaiti.com` (set in `CNAME`).

The site is three standalone pages: `index.html` (home/split landing), `research.html` (publications + research), and `portfolio.html` (photography gallery). Each page is fully self-contained: CSS lives in a `<style>` block and JS in a `<script>` block within the same file. There is no shared stylesheet or JS module — visual consistency (fonts, color tokens, layout patterns) is maintained by hand across files.

## Local development

```bash
python -m http.server 8000   # then open http://localhost:8000
```

Deployment is automatic: pushing to `main` publishes via GitHub Pages. There is no build step. `.nojekyll` is required so GitHub Pages serves files whose names begin with an underscore (e.g. `images/landscape/_DSC4162.jpg`) — do not delete it.

## Photography gallery (portfolio.html)

The gallery is driven by **hardcoded manifests inside `portfolio.html`**, not by directory listing — a static host cannot enumerate a folder. To add or change photos you must edit the JS, not just drop files:

- `IMAGE_FILES` — per-category arrays of filenames that define what appears and in what order.
- `IMAGE_FOLDERS` — maps each category to its `images/<category>/` path.
- `CAPTIONS` — filename → caption text (optional; missing captions fall back to a default).

Categories: `portfolio`, `street`, `landscape`, `cityscape`, `random`, `old`. The gallery preloads adjacent images and shows a loading spinner during fetch. So the full "add a photo" workflow is: drop the file in the right `images/<category>/` folder → add its filename to `IMAGE_FILES[category]` (and a `CAPTIONS` entry) → run `optimize_images.py` → commit.

## Image optimization

`optimize_images.py` (requires `pip install Pillow`) compresses source photos in-place for web delivery. It resizes the longest edge to 2000px and re-saves at JPEG quality 82, but **only for files larger than 1.5 MB** — smaller files are skipped, so it is idempotent and safe to re-run. Run it after adding new photos and before committing.

## Day / night theme

Every page has a day/night pill. A tiny inline script at the top of each `<head>` sets `data-theme="night"|"day"` on `<html>` from `localStorage['pm-theme']` before first paint (default: night); the pill's click handler at the end of each page's `<script>` flips it and saves the choice, so it carries across pages. Each page's `:root` holds the night tokens and `:root[data-theme="day"]` overrides them. When adding CSS, use the tokens — for translucent accents use `rgba(var(--blue-rgb), a)` / `--gold-rgb` (etc.) rather than literal colours, or the colour won't switch. Exceptions on purpose: text/overlays that sit on photos stay dark in both themes, and `portfolio.html` re-applies night tokens on `.viewer` so photos are always shown on black.

## Other files to keep in sync

- `sitemap.xml` lists pages with hand-written `<lastmod>` dates — update them when a page's content changes, and add an entry if you add a new page. `robots.txt` just points at it.
- `document/piyush_maiti_cv.pdf` is linked from `index.html`. Keep this filename when updating the CV (overwrite the file) so the link never breaks.
- Each page carries its own SEO/meta tags (title, description, Open Graph) in `<head>` — edit them per page when role or bio text changes (e.g. the job title appears in `index.html` and `research.html`).
