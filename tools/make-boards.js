// Drives the app in Chromium and screenshots a real board for each method,
// filled with the worked example from that method's page.
// Usage: build the app and serve it (npx vite preview --port 4173), then
//   node tools/make-boards.js [slug ...]
// Needs playwright-core and a Chromium (PLAYWRIGHT_BROWSERS_PATH or CHROME).
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { chromium } = require('playwright-core');

const APP = process.env.APP || 'http://localhost:4173';
const root = path.join(__dirname, '..');

// [kind, board title, framework button name, actions]
// select: click a tile once (panel shows its questions). open: click it again to
// go inside. title: rename the selected tile. fill/choose: answer a question in
// the panel. back: return to the top. shot: take the picture.
const BOARDS = {
  'five-whys': ['Problem', 'The band keeps missing practice', /^5 Whys/, [
    ['select', /^Why did that happen/], ['fill', /^Because/, "Two people didn't turn up each time, and you can't practise without a drummer."],
    ['open', /^Why did that happen/], ['select', /^And why/], ['fill', /^Because/, "They said they didn't know it was on."],
    ['open', /^And why/], ['select', /^And why/], ['fill', /^Because/, 'Practice is arranged in the group chat on the day, and they mute the group chat.'],
    ['open', /^And why/], ['select', /^And why/], ['fill', /^Because/, "The group chat has forty messages a day and most of them aren't about the band."],
    ['open', /^And why/], ['select', /^And why/], ['fill', /^Because/, 'Because it is also the friends chat. There is no separate place where band things live.'],
    ['choose', /Can you act on this cause/, 'yes'], ['shot'],
  ]],
  'working-backwards': ['Project', 'The science fair project', /^Working Backwards/, [
    ['select', /^1 — What done looks like/],
    ['fill', /What is true when this is done/, 'A working model of the south roof stands in the hall on 14 March and a stranger can press the button'],
    ['fill', /The evidence that would prove it/, 'The number it shows matches a real reading to within ten per cent'],
    ['fill', /Who says it is done/, 'The head of science, on the night'], ['fill', /By when, if it matters/, '14 March'],
    ['open', /^2 — The walk back/],
    ['select', /^Milestone 1/], ['title', "Tested by someone who hasn't seen it"],
    ['fill', /What is true at this point/, "The model has been tested by someone who hasn't seen it before"],
    ['fill', /How you would see it/, 'Their name on the test sheet'], ['fill', /What must already be true just before this/, 'The display working'],
    ['choose', /How firm is its date/, 'target'], ['fill', /The date, if it has one/, '7 March'],
    ['select', /^Milestone 2/], ['title', 'The sensor gives a believable reading'],
    ['select', /^Milestone 3/], ['title', 'The sensor is in hand'],
    ['select', /^Tested by someone/], ['shot'],
  ]],
  'pre-mortem': ['Project', 'A stall at the Saturday market', /^Pre-mortem/, [
    ['open', /^1 — Why it failed/],
    ['select', /^Cause of failure 1/], ['title', 'It rained on two of the four Saturdays'],
    ['select', /^Cause of failure 2/], ['title', 'We baked too much on day one and threw half away'],
    ['select', /^Cause of failure 3/], ['title', 'Only one of us could get there at 6am with the trays'],
    ['fill', /What went wrong/, 'Only one of us could actually get there at 6am with the trays, and got fed up by week two'],
    ['choose', /How likely is it really/, 'very-likely'], ['choose', /How bad would it be/, 'serious'],
    ['select', /^Cause of failure 4/], ['title', "The council wanted a hygiene certificate we didn't have"],
    ['select', /^Only one of us/], ['shot'],
  ]],
  'first-principles': ['Challenge', 'The debating final', /^First Principles Analysis/, [
    ['open', /^Phase 1/],
    ['select', /^Assumption 1/], ['title', 'They are better speakers than us'],
    ['fill', /State the assumption in one sentence/, 'They are better speakers than us'],
    ['choose', /Where does it come from/, 'precedent'], ['choose', /How load-bearing is it/, 'high'],
    ['select', /^Assumption 2/], ['title', 'You win debates by being confident'],
    ['select', /^Assumption 3/], ['title', 'We should prepare more arguments than they have'],
    ['back'], ['select', /^Phase 1/], ['shot'],
  ]],
  'force-field-analysis': ['Goal', 'Make the first team this season', /^Force Field Analysis/, [
    ['select', /^1 — The change/],
    ['fill', /The change being proposed/, 'From training with the seconds to being picked for the first team after Christmas'],
    ['fill', /What happens if nothing changes/, 'Another season in the seconds, and next year the year below start overtaking'],
    ['open', /^3 — What is holding it back/],
    ['select', /^Restraining force 1/], ['title', 'Tuesday training clashes with my shift at the shop'],
    ['fill', /^The force/, 'Tuesday training clashes with my shift at the shop'],
    ['choose', /How strong is it/, 'strong'], ['choose', /Could it be moved/, 'can-remove'], ['fill', /Who would move it/, 'Me, and the shop manager'],
    ['select', /^Restraining force 2/], ['title', 'No lift to Saturday away matches'],
    ['select', /^Restraining force 3/], ['title', 'I get nervous in trials and play worse than in training'],
    ['select', /^Tuesday training/], ['shot'],
  ]],
  'options-and-criteria': ['Decision', 'Which subjects to take next year', /^Options and Criteria/, [
    ['open', /^2 — What a good answer must do/],
    ['select', /^Criterion 1/], ['title', 'Keeps both university courses open'],
    ['fill', /^The criterion/, 'Keeps both the university courses I am considering open'],
    ['choose', /Must it, or would you like it to/, 'must-have'], ['fill', /How you would tell/, 'Their published entry requirements'],
    ['select', /^Criterion 2/], ['title', 'No timetable clash'],
    ['select', /^Criterion 3/], ['title', 'I would turn up to it gladly'],
    ['select', /^Keeps both/], ['shot'],
  ]],
  'issue-tree': ['Decision', 'Run the market stall again in December?', /^Issue Tree/, [
    ['select', /^1 — The question/],
    ['fill', /^The question/, 'Should the three of us rent the stall again for the four Saturdays in December?'],
    ['fill', /Your best answer today/, 'Yes'], ['fill', /The decision this informs/, 'Whether to pay the December fee by 20 November'],
    ['open', /^2 — The split/],
    ['select', /^Branch 1/], ['title', 'Did November actually make money?'],
    ['fill', /This part of the question/, 'Did November actually make money, once everything is counted?'],
    ['choose', /Does this overlap another branch/, 'separate'],
    ['fill', /What would have to be true/, 'Takings minus ingredients minus the fee was more than three Saturdays of babysitting'],
    ['fill', /How you would test it/, 'The takings sheet and the receipts, added up honestly'],
    ['choose', /If this branch holds/, 'settles'],
    ['select', /^Branch 2/], ['title', 'Would December be different?'],
    ['select', /^Branch 3/], ['title', 'Can the three of us do it in December?'],
    ['select', /^Did November/], ['shot'],
  ]],
  'cause-and-effect': ['Problem', 'The science fair sensor gives nonsense readings', /^Cause and Effect/, [
    ['select', /^1 — The effect/],
    ['fill', /What happened/, 'The light sensor reads 0 or 1023 and nothing in between'],
    ['fill', /How you know/, 'The laptop log shows only those two values for three days'], ['fill', /When it was first seen/, 'Tuesday'],
    ['open', /^2 — Where the causes might be/],
    ['open', /^2.6 — Measurement/], ['select', /^Cause 1/], ['title', 'The code reads the sensor as a digital pin'],
    ['fill', /^The cause/, 'The code reads the sensor as a digital pin, not an analogue one, so it can only ever give 0 or 1'],
    ['back'], ['open', /^2 — Where the causes might be/], ['select', /^2.6 — Measurement/], ['shot'],
  ]],
  'objectives-and-key-results': ['Goal', 'Get properly good at guitar this year', /^Objectives and Key Results/, [
    ['select', /^1 — The objective/],
    ['fill', /^The objective/, 'Be the guitarist the band relies on'],
    ['fill', /Why this period/, 'The first paid gig is in July and two of the songs are beyond me'], ['fill', /The period it covers/, 'April to the end of June'],
    ['open', /^2 — The key results/],
    ['select', /^Key result 1/], ['title', 'All eight songs through without stopping'],
    ['fill', /What will be true/, 'I can play all eight songs in the set through without stopping'],
    ['choose', /How it is scored/, 'moves'], ['fill', /^The number/, '3 of 8 today, 8 of 8 by 30 June'],
    ['fill', /Where the number is read/, 'The phone recording of Thursday practice'], ['choose', /Committed, or a stretch/, 'committed'],
    ['select', /^Key result 2/], ['title', '80 chord changes a minute on song six'],
    ['select', /^Key result 3/], ['title', 'The band stops re-learning my parts'],
    ['select', /^All eight songs/], ['shot'],
  ]],
  'scenario-planning': ['Decision', 'The Saturday job at the garden centre', /^Scenario Planning/, [
    ['open', /^3 — The four worlds/],
    ['select', /^3.1 — First world/], ['title', 'Full Saturdays'],
    ['fill', /What this world is called/, 'Full Saturdays'], ['fill', /Which end of each axis it takes/, 'First team: picked. Coursework: heavy'],
    ['fill', /How it comes about/, 'Two first-team players leave at Christmas and the coursework timetable lands in September heavier than anyone expected'],
    ['select', /^3.2 — Second world/], ['title', 'Free and easy'],
    ['select', /^3.3 — Third world/], ['title', 'Pitch and pen'],
    ['select', /^3.4 — Fourth world/], ['title', 'Desk-bound'],
    ['select', /^Full Saturdays/], ['shot'],
  ]],
  'stakeholder-and-influence-map': ['Challenge', 'Get the band the school hall on Thursdays', /^Stakeholder and Influence Map/, [
    ['open', /^2 — The people/],
    ['select', /^Stakeholder 1/], ['title', 'Deputy head'],
    ['select', /^Stakeholder 2/], ['title', 'Site manager'],
    ['fill', /Who they are/, 'The site manager, who locks up'], ['choose', /What part they play/, 'gatekeeper'],
    ['fill', /What they actually want/, 'To go home at six'], ['choose', /How much influence they have/, 'high'],
    ['choose', /Where they stand today/, 'opposed'], ['fill', /What would move them/, 'Someone else holding the keys and signing for them'],
    ['fill', /Who has their ear/, 'The deputy head'], ['fill', /Who is going to talk to them/, "Sam's dad, this week"],
    ['select', /^Stakeholder 3/], ['title', 'Head of music'],
    ['select', /^Stakeholder 4/], ['title', 'Drama club lead'],
    ['select', /^Site manager/], ['shot'],
  ]],
  'strategic-challenge-map': ['Challenge', 'Let the canteen take card payments', /^Strategic Challenge Map/, [
    ['select', /^1 — Strategic context/],
    ['fill', /The strategic context/, 'The canteen has to feed 900 people in 40 minutes a day while the school is told to go cashless by the council. The queue is the pressure.'],
    ['fill', /What you must not position against/, 'The canteen staff, the till supplier, and last year’s catering contract'],
    ['open', /^2 — Categorised forensic analysis/], ['select', /^2.4 — Organisational/], ['shot'],
  ]],
  'theory-of-constraints': ['Problem', "The band's set never gets finished", /^Theory of Constraints/, [
    ['select', /^1 — The system and its goal/],
    ['fill', /What the system exists to get through/, 'Songs, from chosen to performable'],
    ['fill', /How the work flows, start to end/, 'Pick a song, each person learns their part at home, rehearse it together on Thursdays, run it clean twice, it is in the set'],
    ['fill', /How you would measure what gets through/, 'Songs in the set'],
    ['open', /^2 — Find the constraint/],
    ['select', /^Candidate 1/], ['title', 'Learning parts at home'], ['choose', /Is this the constraint/, 'cleared'],
    ['select', /^Candidate 2/], ['title', 'Thursday rehearsal'],
    ['fill', /Where the flow might narrow/, 'Thursday rehearsal'],
    ['fill', /The signs of queueing/, 'Six songs learned by everyone and waiting for Thursday. Nothing waiting after it.'],
    ['choose', /Is this the constraint/, 'the-constraint'],
    ['back'], ['select', /^2 — Find the constraint/], ['shot'],
  ]],
  'answer-first': ['Decision', 'History instead of Chemistry, to my parents', /^Answer First/, [
    ['select', /^1 — The answer, first/],
    ['fill', /Who this is for/, 'My parents, who think Chemistry is the serious choice'],
    ['fill', /The question they are asking/, 'Will this close doors?'],
    ['fill', /The answer, in one sentence/, "History instead of Chemistry keeps both courses open and gives me a subject I'll work at for two years"],
    ['open', /^2 — The groups that hold it up/],
    ['select', /^2.1 — First group/], ['title', 'It closes no doors'], ['fill', /What this group asserts/, 'Taking History instead of Chemistry closes no doors'],
    ['select', /^2.2 — Second group/], ['title', "I'll get better grades"],
    ['select', /^2.3 — Third group/], ['title', 'Chemistry costs more than it gives'],
    ['select', /^It closes no doors/], ['shot'],
  ]],
};

const wanted = process.argv.slice(2);
const slugs = wanted.length ? wanted : Object.keys(BOARDS);

function board(page) {
  return page.locator('.board-svg:not(.board-svg--leaving-in):not(.board-svg--leaving-out)').last();
}
async function settle(page) {
  await page.locator('.board-svg--leaving-in, .board-svg--leaving-out').first().waitFor({ state: 'detached', timeout: 3000 }).catch(() => {});
  await page.waitForTimeout(150);
}
async function tile(page, re) {
  const t = board(page).getByRole('button', { name: re }).first();
  await t.waitFor({ state: 'visible' });
  return t;
}

(async () => {
  const exe = process.env.CHROME || execSync("find /opt/pw-browsers -name chrome -type f | head -1").toString().trim();
  const browser = await chromium.launch({ executablePath: exe });
  for (const slug of slugs) {
    const [kind, title, fw, actions] = BOARDS[slug];
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 820 }, deviceScaleFactor: 1 });
    const page = await ctx.newPage();
    const errors = [];
    let step = 'start';
    page.on('pageerror', (e) => errors.push(e.message));
    try {
      await page.goto(APP + '/', { waitUntil: 'load' });
      await page.getByRole('button', { name: new RegExp(`^${kind}\\.`) }).click();
      await page.getByLabel(`Name a ${kind.toLowerCase()}`).fill(title);
      await page.getByRole('button', { name: `Start a ${kind.toLowerCase()}` }).click();
      await page.getByRole('heading', { name: new RegExp(title.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')) }).waitFor();
      await page.getByRole('button', { name: 'Apply a framework' }).first().click();
      await page.getByRole('button', { name: fw }).first().click();
      await page.getByRole('button', { name: /^Add \d+ steps$/ }).click();
      const dismiss = page.getByRole('button', { name: 'Dismiss' });
      if (await dismiss.isVisible().catch(() => false)) await dismiss.click();
      await settle(page);
      // A tile opens on its second click, so remember which one is selected: an
      // already-selected tile needs one click to open, any other needs two.
      let selected = null;
      for (const [op, a, b] of actions) {
        step = `${op} ${a}`;
        if (op === 'select') { await (await tile(page, a)).click(); await page.waitForTimeout(120); selected = String(a); }
        else if (op === 'open') {
          const t = await tile(page, a);
          if (selected !== String(a)) { await t.click(); await page.waitForTimeout(150); }
          await t.click(); await settle(page); selected = null;
        }
        else if (op === 'title') { await page.getByLabel('Title of this step').fill(a); await page.waitForTimeout(120); }
        else if (op === 'fill') { await page.getByLabel(a).first().fill(b); }
        else if (op === 'choose') {
          const sel = page.getByLabel(a).first();
          await sel.selectOption(b);
          await sel.press('Tab');
          const got = await sel.inputValue();
          if (got !== b) console.log('  choose did not stick:', String(a), 'wanted', b, 'got', got);
        }
        else if (op === 'back') { await page.getByRole('button', { name: title }).first().click(); await settle(page); selected = null; }
        else if (op === 'shot') {
          // Show the questions and their answers rather than the bottom of the form.
          // The beta banner stays until a work file is linked; it is not part of the method.
          await page.addStyleTag({ content: '.banner--action { display: none !important; }' });
          const q = page.getByText(/^Questions/).first();
          if (await q.isVisible().catch(() => false)) await q.evaluate((el) => el.scrollIntoView({ block: 'start' }));
          await page.waitForTimeout(400);
          const out = path.join(root, 'methods', slug, 'board.jpg');
          await page.screenshot({ path: out, type: 'jpeg', quality: 82 });
          console.log(slug.padEnd(32), Math.round(fs.statSync(out).size / 1024), 'KB', errors.length ? errors : '');
        }
      }
    } catch (e) {
      console.log(slug.padEnd(32), 'FAILED at', step, ':', e.message.split('\n')[0]);
      await page.screenshot({ path: path.join(root, '..', `fail-${slug}.png`) }).catch(() => {});
    }
    await ctx.close();
  }
  await browser.close();
})();
