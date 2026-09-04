// Renders each method card to a one-page A4 PDF with the bundled Chromium.
// Usage: serve the site root (python3 -m http.server 8768) and run
//   node tools/make-cards.js [port]
// Needs playwright-core on the path (npm i playwright-core) and a Chromium
// binary, found via PLAYWRIGHT_BROWSERS_PATH or the CHROME env var.
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { chromium } = require('playwright-core');

const port = process.argv[2] || '8768';
const root = path.join(__dirname, '..');
const slugs = fs.readdirSync(path.join(root, 'methods')).filter((s) => fs.existsSync(path.join(root, 'methods', s, 'card', 'index.html')));

(async () => {
  const exe = process.env.CHROME || execSync("find /opt/pw-browsers -name chrome -type f | head -1").toString().trim();
  const browser = await chromium.launch({ executablePath: exe });
  const page = await browser.newPage();
  // Fonts come from Google Fonts; a sandbox without egress would otherwise wait on them.
  await page.route(/fonts\.(googleapis|gstatic)\.com/, (r) => r.abort());
  for (const slug of slugs) {
    await page.goto(`http://localhost:${port}/methods/${slug}/card/`, { waitUntil: 'load' });
    const out = path.join(root, 'methods', slug, 'card.pdf');
    const buf = await page.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true });
    const pages = (buf.toString('latin1').match(/\/Type\s*\/Page[^s]/g) || []).length;
    console.log(slug.padEnd(32), pages, 'page(s)', Math.round(buf.length / 1024), 'KB');
  }
  await browser.close();
})();
