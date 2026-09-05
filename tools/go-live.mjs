#!/usr/bin/env node
// Points greggle.app at Netlify, using the Netlify and Porkbun APIs.
//
// It reads keys from the environment, never from arguments, so they stay out
// of shell history and chat transcripts:
//   NETLIFY_AUTH_TOKEN   a personal access token (Netlify: User settings, Applications)
//   NETLIFY_SITE_ID      the site's API ID (Netlify: Site configuration, General)
//   PORKBUN_API_KEY      and
//   PORKBUN_SECRET_KEY   from Porkbun: Account, API Access. Also switch on
//                        "API access" for the domain itself, in its details.
//
// Dry run by default: it prints what it would change and stops.
//   node tools/go-live.mjs
// Apply the changes:
//   node tools/go-live.mjs --apply
//
// What it does, and nothing more:
//   1. Sets greggle.app as the site's primary custom domain on Netlify.
//   2. On Porkbun, removes the A and AAAA records for the bare domain (the ones
//      that point at GitHub Pages) and adds one ALIAS record to Netlify.
//   3. Leaves every other record alone: the www CNAME that carries the app,
//      the GitHub verification TXT, mail, everything.
//   4. Asks Netlify to provision the certificate.
// Run it again later and it changes nothing that is already right.

const DOMAIN = 'greggle.app';
const NETLIFY_ALIAS = 'apex-loadbalancer.netlify.com';
const apply = process.argv.includes('--apply');

const need = (name) => {
  const v = process.env[name];
  if (!v) { console.error(`Missing ${name} in the environment.`); process.exit(1); }
  return v;
};
const netlifyToken = need('NETLIFY_AUTH_TOKEN');
const siteId = need('NETLIFY_SITE_ID');
const pbKey = need('PORKBUN_API_KEY');
const pbSecret = need('PORKBUN_SECRET_KEY');

async function netlify(method, path, body) {
  const res = await fetch(`https://api.netlify.com/api/v1${path}`, {
    method,
    headers: { Authorization: `Bearer ${netlifyToken}`, 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) throw new Error(`Netlify ${method} ${path}: ${res.status} ${await res.text()}`);
  return res.status === 204 ? null : res.json();
}
async function porkbun(path, body = {}) {
  const res = await fetch(`https://api.porkbun.com/api/json/v3${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ apikey: pbKey, secretapikey: pbSecret, ...body }),
  });
  const json = await res.json();
  if (json.status !== 'SUCCESS') throw new Error(`Porkbun ${path}: ${JSON.stringify(json)}`);
  return json;
}

const say = (s) => console.log(s);
const plan = (s) => console.log(`${apply ? 'DOING ' : 'WOULD  '}${s}`);

// 1. Netlify: the domain.
const site = await netlify('GET', `/sites/${siteId}`);
say(`Netlify site: ${site.name} (${site.url})`);
if (site.custom_domain === DOMAIN) {
  say(`  primary domain is already ${DOMAIN}`);
} else {
  plan(`set primary custom domain to ${DOMAIN} (currently ${site.custom_domain ?? 'none'})`);
  if (apply) await netlify('PATCH', `/sites/${siteId}`, { custom_domain: DOMAIN });
}
const aliases = site.domain_aliases ?? [];
if (aliases.includes(`www.${DOMAIN}`)) {
  plan(`remove www.${DOMAIN} from the site's domain aliases, since www is the app on GitHub Pages`);
  if (apply) await netlify('PATCH', `/sites/${siteId}`, { domain_aliases: aliases.filter((a) => a !== `www.${DOMAIN}`) });
}

// 2. Porkbun: the records.
const { records } = await porkbun(`/dns/retrieve/${DOMAIN}`);
say(`Porkbun has ${records.length} records for ${DOMAIN}:`);
for (const r of records) say(`  ${r.type.padEnd(6)} ${(r.name || DOMAIN).padEnd(48)} ${r.content}`);

const apexOld = records.filter((r) => r.name === DOMAIN && (r.type === 'A' || r.type === 'AAAA'));
const apexAlias = records.find((r) => r.name === DOMAIN && r.type === 'ALIAS' && r.content === NETLIFY_ALIAS);
const www = records.find((r) => r.name === `www.${DOMAIN}`);

if (www) say(`  keeping www -> ${www.content} (the app)`);
else say(`  note: there is no www record; the app at www.${DOMAIN} needs one pointing at GitHub Pages`);

for (const r of apexOld) {
  plan(`delete ${r.type} ${DOMAIN} -> ${r.content} (id ${r.id})`);
  if (apply) await porkbun(`/dns/delete/${DOMAIN}/${r.id}`);
}
if (apexAlias) say(`  ALIAS ${DOMAIN} -> ${NETLIFY_ALIAS} is already there`);
else {
  plan(`create ALIAS ${DOMAIN} -> ${NETLIFY_ALIAS}`);
  if (apply) await porkbun(`/dns/create/${DOMAIN}`, { name: '', type: 'ALIAS', content: NETLIFY_ALIAS, ttl: '600' });
}

// 3. Netlify: the certificate. Netlify checks DNS itself, so this may need a
// second run once the ALIAS has propagated.
if (apply) {
  try {
    await netlify('POST', `/sites/${siteId}/ssl`);
    say('Asked Netlify to provision the certificate. It appears once DNS has propagated.');
  } catch (e) {
    say(`Certificate not provisioned yet: ${e.message.split('\n')[0]}`);
    say('Run this again in a little while, or press "Verify DNS configuration" in Netlify.');
  }
} else {
  say('\nDry run. Nothing was changed. Add --apply to make these changes.');
}
