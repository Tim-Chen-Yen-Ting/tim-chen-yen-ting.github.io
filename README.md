# If you see this, you're probably on the wrong page.

You probably meant **https://tim-chen-yen-ting.github.io/** instead. That's the actual website. This is just the code behind it.

---

## What this repo is

The source for my personal site: a tabbed portfolio (Home, Projects, Personal, Contact) in English and Traditional Chinese, with a popup story for every project.

It's plain HTML, CSS and JavaScript, hosted on GitHub Pages. There's no framework and no bundler. Python is only used to generate the page.

## How it's put together

| Path | What it is |
|---|---|
| `index.html` | **Generated.** Don't edit it by hand, because the next build overwrites it. |
| `_src/build.py` | The generator. Every visible string is written once as (English, 中文) so the two languages can't drift apart. |
| `style.css` | All styling (dark theme, responsive down to phone width). |
| `script.js` | Tabs, language toggle, project popups, live clocks. |
| `assets/img/` | Screenshots, charts and diagrams. |
| `assets/resumes/` | Downloadable résumés and CV (PDF). |

## Editing it

1. Change the text or structure in `_src/build.py` (or the look in `style.css`).
2. Rebuild:

   ```bash
   python _src/build.py
   ```

3. Commit and push. GitHub Pages redeploys in a minute or two.

The build also stamps a content hash on the CSS and JS links, so browsers always fetch the latest version instead of showing a stale cached copy.

## A note on how it was made

I wrote the content and made the decisions. I built the site together with Claude Code, which wrote much of the HTML, CSS and JavaScript and the generator. I check the facts against my own project repos and work reports, and the Chinese version is a translation I reviewed.

## Elsewhere

- GitHub: [Tim-Chen-Yen-Ting](https://github.com/Tim-Chen-Yen-Ting)
- LinkedIn: [Yen-Ting (Tim) Chen](https://www.linkedin.com/in/tim-chen-yen-ting)
