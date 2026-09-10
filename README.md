# The Greggle website

The public site at <https://greggle.app/>. The app itself is a separate site at
<https://www.greggle.app/>, deployed from the private source repository — nothing
here touches it.

Plain static files, no build step: edit, commit, push, and the host serves it.
`netlify.toml` configures Netlify (publish the root, no build, security and
caching headers, a few redirects); `404.html` is the not-found page. The site
is served by Netlify; GitHub Pages is switched off for this repository. New pages are new
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
alone.

Each method also has a printable card at `methods/<slug>/card/index.html`, styled
by `card.css` for one A4 page, and a `card.pdf` beside it. Eight more cards for
methods that are not in the app, two for each of four further kinds of thing,
live under `cards/<slug>/` and are introduced on the kinds page. The PDFs are rendered
from the card pages by `tools/make-cards.js` (serve the site root, then
`node tools/make-cards.js <port>`; it needs `playwright-core` and a Chromium).
The typeface is self-hosted in `fonts/` under the SIL Open Font License, so
the PDFs carry it and the site fetches nothing from anywhere else.

Each method page shows a real board, `methods/<slug>/board.jpg`, filled in with
that page's worked example, and the board inside every step that has one,
`board-1.jpg` onwards, all the way down. Beside them `board.json` says where each
step sits in each picture and which picture is inside it, and the generator lays
a clickable area over every such step, so a reader can open the example level by
level without a line of script: a hidden radio button per level and a label per
step, in `site.css` under `.boardstack`. The front page's board, `board.jpg` at
the root, is made the same way and pasted between two markers in `index.html`.
They are taken by `tools/make-boards.js`, which drives the app in Chromium: build
the app repository, serve it with `npx vite preview --port 4173`, then
`node tools/make-boards.js [slug ...]` (`home` is the front page's). The script
hides the beta work-file banner for the pictures, since it is not part of the
method; everything else is the app as it runs.

`tools/go-live.mjs` points the domain at Netlify: it sets the primary domain on
the Netlify site and swaps the bare domain's Porkbun records from GitHub Pages
to a Netlify ALIAS, leaving the `www` record (the app) and everything else
alone. Keys come from the environment; it is a dry run unless given `--apply`.

`node tools/check-links.js` walks every page and checks that each link lands:
a path into the site has to be a file that exists, a fragment has to name an id
that page has, and a link into the app has to use kind and method ids the app
recognises, read from the app repository (`--app <path>`, `GREGGLE_APP`, or
`../jigsaw`). The app ignores a stale id rather than reporting it, so without
this a renamed method would quietly turn a try-it button into the front page.
It exits 1 if anything is broken, so it can gate a publish. Nothing is fetched.
