# Manan Singh's website

Project details live in `content/projects/` and shared site settings live in `content/profile.json`. The published HTML, styles, scripts, images, and PDF are at the repository root for GitHub Pages.

To generate the site, install Python dependencies `reportlab` and `Pillow`, then run `python build.py --web-only`. The generated site is in `dist-public/`; copy the changed generated files to the repository root. Run `python build.py` to also regenerate the portfolio PDF. Keep draft projects out of the `projects` list in `content/profile.json` until they are ready to publish.
