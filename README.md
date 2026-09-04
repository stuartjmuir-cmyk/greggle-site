# The Greggle website

The public site GitHub Pages serves at <https://greggle.app/>. The app itself is a
separate site at <https://www.greggle.app/>, deployed from the private source
repository — nothing here touches it.

Plain static files, no build step: edit, commit, push, and Pages serves it. The
`CNAME` file is what attaches the domain — do not delete it. New pages are new
files: `frameworks.html` becomes `greggle.app/frameworks.html`, or
`frameworks/index.html` becomes `greggle.app/frameworks/`.

The front page's design source of truth is the "Greggle Website" canvas in Claude
Design; the board screenshot is a real board from the app.

Shared styles live in `site.css`; the front page keeps only its own layout rules
inline. The ways-of-thinking pages are under `methods/`, one folder per method
with an `index.html`, plus `methods/index.html` for the grouped index. They were
stamped out by `tools/gen-methods.py`, which holds the copy for every built
page; running it again overwrites those files, so edit the copy there if the
script is going to be run again, or edit the HTML directly and leave the script
alone. Method pages not yet built are listed on the index as coming.
