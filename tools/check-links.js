#!/usr/bin/env node
// Checks every link on the site before it is published.
//
// Walks each HTML file under the site root and looks at every href and src. A
// link into the site has to land on a file that exists, and a fragment on it has
// to name an id that page actually has. A link into the app is checked against
// the app itself: the kind and method ids in the query have to be ones the app
// recognises, read from its vocabulary and framework files, because the app
// ignores a stale id rather than reporting it and the try-it button would then
// quietly open the front page. Other addresses are listed and not fetched: the
// site links to almost nothing else, and a check that needs the network fails for
// reasons that have nothing to do with the site.
//
//   node tools/check-links.js            checks the site in the current directory
//   node tools/check-links.js --app ../jigsaw
//                                        says where the app repository is; also
//                                        read from GREGGLE_APP, else ../jigsaw
//
// Exits 1 if anything is broken, so it can gate a deploy.

const fs = require('fs');
const path = require('path');

const root = process.cwd();
const argAt = process.argv.indexOf('--app');
const appRoot = path.resolve(
  argAt > -1 ? process.argv[argAt + 1] : process.env.GREGGLE_APP || path.join(root, '..', 'jigsaw'),
);

const SKIP_DIRS = new Set(['.git', 'node_modules', 'tools']);

function htmlFiles(dir, out = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) {
      if (!SKIP_DIRS.has(entry.name)) htmlFiles(path.join(dir, entry.name), out);
    } else if (entry.name.endsWith('.html')) {
      out.push(path.join(dir, entry.name));
    }
  }
  return out;
}

const decode = (s) => s.replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#39;/g, "'");

/** Every id a page declares, for checking fragments against. */
function idsIn(html) {
  const ids = new Set();
  for (const m of html.matchAll(/\sid="([^"]+)"/g)) ids.add(m[1]);
  return ids;
}

/** Every href and src on a page, with the line it is on. */
function linksIn(html) {
  const out = [];
  const lines = html.split('\n');
  lines.forEach((line, i) => {
    for (const m of line.matchAll(/\b(?:href|src)="([^"]*)"/g)) out.push({ url: decode(m[1]), line: i + 1 });
  });
  return out;
}

/** What the app recognises in a link: its kind ids and framework ids. */
function appIds() {
  const vocab = path.join(appRoot, 'src', 'domain', 'vocabulary.ts');
  const data = path.join(appRoot, 'src', 'frameworks', 'data');
  if (!fs.existsSync(vocab) || !fs.existsSync(data)) return null;
  const kinds = new Set();
  for (const m of fs.readFileSync(vocab, 'utf8').matchAll(/^\s+id: '([a-z]+)',$/gm)) kinds.add(m[1]);
  const methods = new Set();
  for (const f of fs.readdirSync(data)) {
    if (f.endsWith('.json')) methods.add(JSON.parse(fs.readFileSync(path.join(data, f), 'utf8')).id);
  }
  return { kinds, methods };
}

/** The file a site path resolves to, or null. A directory means its index.html. */
function fileFor(sitePath) {
  const clean = decodeURIComponent(sitePath.split('?')[0]);
  const full = path.join(root, clean);
  if (!full.startsWith(root)) return null;
  if (fs.existsSync(full)) {
    if (fs.statSync(full).isDirectory()) {
      const index = path.join(full, 'index.html');
      return fs.existsSync(index) ? index : null;
    }
    return full;
  }
  return null;
}

const app = appIds();
const pages = htmlFiles(root);
const idCache = new Map();
const problems = [];
const external = new Map();
let checked = 0;

function idsOf(file) {
  if (!idCache.has(file)) idCache.set(file, idsIn(fs.readFileSync(file, 'utf8')));
  return idCache.get(file);
}

for (const page of pages) {
  const html = fs.readFileSync(page, 'utf8');
  const rel = path.relative(root, page);
  const here = path.dirname(page);
  const fail = (line, url, why) => problems.push(`${rel}:${line}  ${url}  ${why}`);

  for (const { url, line } of linksIn(html)) {
    checked += 1;
    if (url === '' || url.startsWith('mailto:') || url.startsWith('data:') || url.startsWith('javascript:')) continue;

    // Into the app: the ids in the query are what the app will look up.
    if (/^https:\/\/www\.greggle\.app\/?/.test(url)) {
      const query = new URL(url).searchParams;
      const kind = query.get('kind');
      const method = query.get('method');
      if (!app) {
        if (kind || method) fail(line, url, 'cannot be checked: app repository not found (use --app)');
        continue;
      }
      if (kind && !app.kinds.has(kind)) fail(line, url, `the app has no kind "${kind}"`);
      if (method && !app.methods.has(method)) fail(line, url, `the app has no method "${method}"`);
      continue;
    }

    if (/^[a-z]+:/i.test(url)) {
      if (!url.startsWith('https://greggle.app')) external.set(url, (external.get(url) || 0) + 1);
      else {
        // The site's own address: check it as a site path.
        const u = new URL(url);
        const target = fileFor(u.pathname);
        if (!target) fail(line, url, 'nothing at that path');
        else if (u.hash && !idsOf(target).has(u.hash.slice(1))) fail(line, url, `no id "${u.hash.slice(1)}" on that page`);
      }
      continue;
    }

    // Into the site.
    const [pathPart, hash] = url.split('#');
    let target;
    if (pathPart === '') target = page;
    else if (pathPart.startsWith('/')) target = fileFor(pathPart);
    else {
      const full = path.resolve(here, pathPart.split('?')[0]);
      target = fs.existsSync(full) ? (fs.statSync(full).isDirectory() ? path.join(full, 'index.html') : full) : null;
      if (target && !fs.existsSync(target)) target = null;
    }
    if (!target) {
      fail(line, url, 'nothing at that path');
      continue;
    }
    if (hash && target.endsWith('.html') && !idsOf(target).has(hash)) {
      fail(line, url, `no id "${hash}" on that page`);
    }
  }
}

console.log(`${pages.length} pages, ${checked} links checked${app ? '' : ' (app links not checked: repository not found)'}`);
if (external.size) {
  console.log('Not fetched, listed for the eye:');
  for (const [url, n] of [...external].sort()) console.log(`  ${url}  x${n}`);
}
if (problems.length) {
  console.log(`\n${problems.length} broken:`);
  for (const p of problems) console.log('  ' + p);
  process.exit(1);
}
console.log('All links land.');
