# piyush-maiti.github.io

Personal portfolio website for Piyush Maiti — Neuroimaging Data Analyst at UCSF and amateur photographer.

**Live site:** [piyushkmaiti.com](https://piyushkmaiti.com)

## Pages

- **Home** (`index.html`) — Landing page with a split layout showcasing research experience and photography
- **Research** (`research.html`) — Publications, research areas, conference abstracts, and tools/software
- **Photography** (`portfolio.html`) — Image gallery with category-based navigation (landscape, cityscape, street, etc.)

## Tech Stack

- Static HTML/CSS/JS (no build tools or frameworks)
- Google Fonts (Playfair Display, DM Sans, JetBrains Mono)
- Hosted via GitHub Pages with a custom domain (CNAME)

## Structure

```
.
├── index.html          # Home page
├── research.html       # Research & publications
├── portfolio.html      # Photography portfolio
├── CNAME               # Custom domain config
├── document/           # CV and other documents
└── images/             # Photography organized by category
    ├── portfolio/
    ├── street/
    ├── landscape/
    ├── cityscape/
    ├── random/
    └── old/
```

## Local Development

Open `index.html` in a browser, or serve locally:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000`.