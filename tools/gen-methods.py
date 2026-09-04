# Stamps out /methods/ and one page per built method from the content below.
# The HTML it writes is committed and can be edited by hand; running this again
# overwrites those files, so put copy changes here, not in the HTML, if you
# intend to run it again. Usage: python3 tools/gen-methods.py

import re, os, html

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
MARK = open(os.path.join(ROOT, "index.html")).read().split('<svg class="mark"', 1)[1].split("</svg>", 1)[0]
MARK = '<svg class="mark"' + MARK + "</svg>"

def curly(s):
    return re.sub(r"(\w)'(\w)", r"\1&rsquo;\2", s)

def head(title, desc, canon, image="https://greggle.app/board.jpg"):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canon}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#eceef1">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{image}">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400..700&display=swap">
<link rel="stylesheet" href="/site.css">
</head>
<body>
<div class="shell">

  <header class="topbar bar">
    <a class="brand" href="/">{MARK} <span>Greggle</span></a>
    <nav class="topnav">
      <a class="navlink" href="/methods/" aria-current="page">Ways of thinking</a>
      <a class="btn btn-small" href="https://www.greggle.app/">Open Greggle</a>
    </nav>
  </header>
"""

FOOT = """
  <footer>
    <span class="stated">Greggle &middot; free &middot; no account &middot; works offline</span>
    <span class="stated"><a href="/methods/">ways of thinking</a> &middot; <a href="mailto:feedback@greggle.app">feedback@greggle.app</a> &middot; your work stays on your device</span>
  </footer>
</div>
</body>
</html>
"""

# ---------------------------------------------------------------------------
# The fourteen, in index order. slug None = page not built yet (phase two).
GROUPS = [
    ("Work out what is actually wrong", "For a Problem. Something has gone wrong and you need the cause, not the symptom.", [
        ("five-whys", "5 Whys", "Toyota, 1950s", "Ask why of the answer, five times, until you reach a cause you can actually act on."),
        (None, "Cause and Effect", "Kaoru Ishikawa, 1960s", "The fishbone. Go wide across every kind of cause before you go deep on one."),
        (None, "Theory of Constraints", "Eliyahu Goldratt, 1984", "Find the one place where the whole flow narrows, and serve it."),
    ]),
    ("Break a big question into parts", "For a Challenge, a Project or a Goal too large to see whole.", [
        (None, "Issue Tree", "McKinsey, 1960s", "Split a question into parts that do not overlap and leave nothing out."),
        ("first-principles", "First Principles", "Aristotle", "Find the truths nothing else rests on, then build up from them alone."),
        (None, "Strategic Challenge Map", "Greggle&rsquo;s own synthesis", "Categorise the challenges, evidence each one, judge what you can move."),
    ]),
    ("Decide between options", "For a Decision, or an Opportunity you have not yet said yes to.", [
        ("options-and-criteria", "Options and Criteria", "Franklin, 1772", "Write down what a good answer would have to do before you look at the answers."),
        ("force-field-analysis", "Force Field Analysis", "Kurt Lewin, 1940s", "What is pushing for the change, what is holding it back, and which single restraint to remove."),
    ]),
    ("Plan towards something", "For a Project with an end, or a Goal without one.", [
        ("working-backwards", "Working Backwards", "Amazon, 2000s", "Define what done looks like and the evidence that would prove it, then walk back to now."),
        (None, "Objectives and Key Results", "Intel, 1970s", "One objective, and the numbers that would prove you reached it."),
    ]),
    ("See what could go wrong", "For a Risk, or any plan before it starts.", [
        ("pre-mortem", "Pre-mortem", "Gary Klein, 2007", "It is twelve months from now and this failed. Work out why, then prevent it."),
        (None, "Scenario Planning", "Shell, 1970s", "Build four futures, decide what you would do in each, plant signposts."),
    ]),
    ("Bring other people with you", "For anything whose outcome depends on someone else.", [
        (None, "Stakeholder and Influence Map", "Freeman and Mendelow, 1980s", "Who decides, who can block it, and what each of them actually wants."),
        (None, "Answer First", "Barbara Minto, 1970s", "Give the answer in the first sentence, reasons beneath. The consulting habit."),
    ]),
]

def slug_of(name):
    return name.lower().replace(" and ", "-and-").replace(" ", "-")

ALL = [(s or slug_of(n), n, o, d, s is not None) for _, _, items in GROUPS for (s, n, o, d) in items]
BUILT = [a for a in ALL if a[4]]

def link_to(name):
    for slug, n, o, d, built in ALL:
        if n == name:
            return f'<a href="/methods/{slug}/">{n}</a>' if built else f'<a href="/methods/#{slug}">{n}</a>'
    raise KeyError(name)

# ---------------------------------------------------------------------------
def write_index():
    out = head("Fourteen ways of thinking", "The methods Greggle walks you through: where each came from, what it is for, and how to run it on paper or on a board.", "https://greggle.app/methods/")
    out = out.replace('aria-current="page"', 'aria-current="page"')
    out += """
  <section>
    <div class="page-head">
      <p class="crumbs"><a href="/">Greggle</a> &middot; Ways of thinking</p>
      <span class="eyebrow">Fourteen ways of thinking</span>
      <h1>None of them were invented here. That is the point.</h1>
      <p class="dim lead">These are the methods factories, consultancies and labs have used for decades, the ones normally locked inside textbooks and training courses. Each page says where the method came from, why it works, when to reach for it, and how to run it with a pen. Greggle lays the same method out on your board and walks you through it.</p>
      <p class="dim lead">Start with what you are trying to do.</p>
    </div>
  </section>
"""
    for title, blurb, items in GROUPS:
        out += f"""
  <section class="group">
    <div class="group-head">
      <h2>{title}</h2>
      <p class="dim">{blurb}</p>
    </div>
    <div class="grid grid-methods">
"""
        for slug, name, origin, desc in items:
            sid = slug or slug_of(name)
            if slug:
                out += f'      <div class="card" id="{sid}"><h3><a href="/methods/{slug}/">{name}</a></h3><p class="stated origin">{curly(origin)}</p><p class="dim">{curly(desc)}</p></div>\n'
            else:
                out += f'      <div class="card" id="{sid}"><h3>{name}</h3><p class="stated origin">{curly(origin)}</p><p class="dim">{curly(desc)}</p><p class="stated soon">full page coming</p></div>\n'
        out += "    </div>\n  </section>\n"

    out += """
  <section>
    <div class="card kinds-map">
      <span class="stated">What Greggle suggests first, by the kind of thing you are working on</span>
      <div class="kinds-row"><b>a Goal</b><span>Pre-mortem, Working Backwards, Force Field Analysis, First Principles, Objectives and Key Results</span></div>
      <div class="kinds-row"><b>a Project</b><span>Pre-mortem, Working Backwards, Theory of Constraints, Stakeholder and Influence Map, Strategic Challenge Map</span></div>
      <div class="kinds-row"><b>a Challenge</b><span>Strategic Challenge Map, Issue Tree, Stakeholder and Influence Map, Scenario Planning, First Principles, Answer First</span></div>
      <div class="kinds-row"><b>a Problem</b><span>5 Whys, Cause and Effect, Issue Tree, Theory of Constraints, First Principles</span></div>
      <div class="kinds-row"><b>a Decision</b><span>Issue Tree, Options and Criteria, First Principles, Force Field Analysis, Pre-mortem, Answer First</span></div>
      <div class="kinds-row"><b>an Opportunity</b><span>Force Field Analysis, Options and Criteria, Scenario Planning, Stakeholder and Influence Map, Pre-mortem</span></div>
      <div class="kinds-row"><b>a Risk</b><span>Pre-mortem, Cause and Effect, Force Field Analysis</span></div>
      <p class="dim" style="font-size: 14px; padding-top: 12px">All fourteen are always there. These are the ones the app puts at the top of the list for each kind, most apt first.</p>
    </div>
  </section>

  <section class="cta">
    <div class="card">
      <h2>Pick one and try it on something real.</h2>
      <p class="dim">Greggle proposes the first cut and adds nothing until you have looked at it. No account, nothing leaves your device.</p>
      <a class="btn" href="https://www.greggle.app/">Open Greggle</a>
    </div>
  </section>
"""
    out += FOOT
    with open(os.path.join(ROOT, "methods", "index.html"), "w") as f:
        f.write(out)

# ---------------------------------------------------------------------------
def write_method(m):
    slug = m["slug"]
    canon = f"https://greggle.app/methods/{slug}/"
    out = head(f"{m['name']} · a way of thinking · Greggle", m["desc"], canon)
    toc = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in [
        ("origin", "Where it came from"), ("works", "Why it works"), ("when", "When to reach for it"),
        ("how", "How to run it"), ("board", "On a Greggle board"), ("example", "A worked example"),
        ("falls", "Where it falls down"), ("pairs", "Pairs well with"), ("reading", "Further reading")])
    pairs = "".join(f"<li>{link_to(n)}. {curly(why)}</li>" for n, why in m["pairs"])
    reading = "".join(f"<li>{curly(r)}</li>" for r in m["reading"])
    tiles = ""
    for t in m["board"]:
        cls = "tile action" if t.get("action") else "tile"
        tiles += f'<div class="{cls}"><span class="stated">{t["label"]}</span><b>{curly(t["name"])}</b><span>{curly(t["text"])}</span></div>\n'
    steps = "".join(f"<li>{curly(s)}</li>" for s in m["steps"])
    checks = "".join(f"<li>{curly(c)}</li>" for c in m["checks"])

    # prev / next among built pages
    idx = [b[0] for b in BUILT].index(slug)
    prev = BUILT[idx - 1] if idx > 0 else None
    nxt = BUILT[idx + 1] if idx < len(BUILT) - 1 else None
    nav = '<div class="nextprev">'
    nav += f'<a href="/methods/{prev[0]}/">&larr; {prev[1]}</a>' if prev else '<a href="/methods/">&larr; All fourteen</a>'
    nav += f'<a href="/methods/{nxt[0]}/">{nxt[1]} &rarr;</a>' if nxt else '<a href="/methods/">All fourteen &rarr;</a>'
    nav += "</div>"

    body = f"""
  <article class="method">
    <header class="method-head">
      <p class="crumbs"><a href="/">Greggle</a> &middot; <a href="/methods/">Ways of thinking</a> &middot; {m['name']}</p>
      <span class="eyebrow">A way of thinking &middot; best for {m['kind']}</span>
      <h1>{m['name']}</h1>
      <p class="dim lead">{curly(m['lead'])}</p>
    </header>

    <div class="card facts">
      <div><span class="stated">Origin</span><p>{curly(m['facts']['origin'])}</p></div>
      <div><span class="stated">Best for</span><p>{curly(m['facts']['best'])}</p></div>
      <div><span class="stated">Takes</span><p>{curly(m['facts']['takes'])}</p></div>
      <div><span class="stated">Needs</span><p>{curly(m['facts']['needs'])}</p></div>
    </div>

    <div class="method-body">
      <div class="prose">
        <section id="origin"><h2>Where it came from</h2>{curly(m['origin'])}</section>
        <section id="works"><h2>Why it works</h2>{curly(m['works'])}</section>
        <section id="when"><h2>When to reach for it, and when not to</h2>{curly(m['when'])}</section>
        <section id="how"><h2>How to run it</h2><p class="dim">With a pen, on one sheet of paper.</p><ol>{steps}</ol></section>
        <section id="board"><h2>On a Greggle board</h2>
          <p>{curly(m['board_intro'])}</p>
          <div class="board">
{tiles}          </div>
          <p class="note">Nothing is added until you have looked at it. Open any step and it becomes a board of its own. Steps that cannot sensibly be cut smaller get marked as actions, and every action collects in one flat list.</p>
          <h3>What the check looks for</h3>
          <p class="dim">One button reads the whole branch back. On this method it reports, among other things:</p>
          <ul>{checks}</ul>
        </section>
        <section id="example"><h2>A worked example</h2>{curly(m['example'])}</section>
        <section id="falls"><h2>Where it falls down</h2>{curly(m['falls'])}</section>
        <section id="pairs"><h2>Pairs well with</h2><ul>{pairs}</ul></section>
        <section id="reading" class="reading"><h2>Further reading</h2><ul>{reading}</ul></section>
      </div>
      <aside class="side">
        <div class="card toc"><h3>On this page</h3><ul>{toc}</ul></div>
        <div class="card"><h3>Try it in Greggle</h3><p class="dim" style="font-size:14px">{curly(m['try'])}</p><a class="btn btn-small" href="https://www.greggle.app/">Open Greggle</a></div>
      </aside>
    </div>

    <section class="method-cta">
      <div class="card">
        <h2>{curly(m['cta'])}</h2>
        <p class="dim">Free, no account, works offline. Your work stays on your device.</p>
        <a class="btn" href="https://www.greggle.app/">Open Greggle</a>
      </div>
      {nav}
    </section>
  </article>
"""
    out += body + FOOT
    d = os.path.join(ROOT, "methods", slug)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w") as f:
        f.write(out)

# ---------------------------------------------------------------------------
METHODS = []

METHODS.append(dict(
    slug="five-whys", name="5 Whys", kind="a Problem",
    desc="Where the 5 Whys came from, why it works, when to use it and how to run it: Toyota's method for finding the cause you can actually act on.",
    lead="Ask why of the answer, five times, until you reach a cause you can actually act on.",
    facts=dict(origin="Toyota, 1950s", best="a Problem", takes="Ten minutes", needs="One person who was there"),
    origin="""
<p>Toyota. The habit of asking why until the answer runs out is credited to Sakichi Toyoda, the inventor who founded the Toyota group, and it was Taiichi Ohno who made it a formal part of the Toyota Production System as he built that system through the 1950s and 60s. Ohno's 1978 book gives the example everyone still uses. A machine stopped.</p>
<p>Why did it stop? A fuse blew, because the machine was overloaded. Why was it overloaded? The bearing was not lubricated enough. Why not? The lubrication pump was not pumping properly. Why not? Its shaft was worn and rattling. Why was the shaft worn? There was no strainer on the intake, so metal scrap had got into the pump.</p>
<p>Replace the fuse and the machine stops again next week. Fit a strainer and it doesn't. Ohno's point was that the first four answers are all true and none of them is the cause.</p>""",
    works="""
<p>Each answer becomes the next question, so you can't stop at the first plausible cause. Most people stop there because the first cause is usually a real one, just not the one that matters.</p>
<p>The discipline is in refusing to accept a person's mistake as an answer. Somebody forgot, somebody was late, somebody didn't check. People will always forget and be late and not check, and you can't fix that. You can fix the thing that made the mistake possible, or the thing that made it matter. So when an answer is "someone slipped up", ask why the slip was possible, and keep going.</p>""",
    when="""
<p>Reach for it when something has gone wrong, ideally more than once, and you suspect the obvious explanation is only the surface. It is at its best on a single, specific event: this practice was missed, this deadline slid, this row happened.</p>
<p>Don't use it on something that hasn't happened yet, and don't use it on a problem that feels wide rather than deep. If you can already think of four unrelated reasons, you have several chains, not one, and the fishbone is the better start. In Greggle, 5 Whys is the first method suggested on a Problem.</p>""",
    steps=[
        "Write the problem as one observed fact. Not \"the band is flaky\" but \"we have missed four of the last six practices\". Say how you know.",
        "Ask why it happened. Write one answer, a cause you could check, not the same event in other words.",
        "Ask why of that answer, not of the original problem. Write the next answer beneath it.",
        "Keep going. Whenever the answer is a person's mistake, ask why the mistake was possible, or why it mattered.",
        "Stop when you reach something you could change tomorrow. Five is a guide, not a rule. Three is often enough, and if the fifth still isn't something you can act on, the chain went sideways: start again from the first why.",
        "Write the change as an action. Then check it backwards: if that had been in place, would the chain have broken?",
    ],
    board_intro="Pick 5 Whys on a Problem board and Greggle first asks you to state the problem as an observable fact, then proposes five whys, each one nested inside the one before it, so every why is asked of the answer above and not of the original problem.",
    board=[
        dict(label="the problem", name="What went wrong, and how do you know?", text="Something that happened, not something you feel."),
        dict(label="why 1", name="Why did that happen?", text="Because&hellip; A cause, not the same event in other words."),
        dict(label="why 2", name="And why did that happen?", text="Sits inside why 1. Asked of the answer above."),
        dict(label="why 3 and 4", name="And why did that happen?", text="Each one inside the last. If it could have been written before reading the line above, the chain has gone sideways."),
        dict(label="why 5", name="And why did that happen?", text="Then one more question: can you act on this cause? Yes, this is the root cause. No, the chain needs redoing.", action=True),
        dict(label="then", name="The fix that breaks the chain", text="Cut it small and mark it as an action, so it lands in your list."),
    ],
    checks=[
        "The first why just says the problem again. Restating what went wrong is not a cause of it.",
        "A why gives back the answer above it, which means it was asked of the original problem rather than of the answer it follows.",
        "Five whys in, with nothing you can act on. Either the chain went sideways or it has further to go.",
    ],
    example="""
<div class="card example">
  <span class="stated">a Problem &middot; the band keeps missing practice</span>
  <div class="qa">
    <div><b>The problem</b><span>We have missed four of the last six Thursday practices. I know because I was at all six.</span></div>
    <div><b>Why?</b><span>Two people didn't turn up each time, and you can't practise without a drummer.</span></div>
    <div><b>Why?</b><span>They said they didn't know it was on.</span></div>
    <div><b>Why?</b><span>Practice is arranged in the group chat on the day, and they mute the group chat.</span></div>
    <div><b>Why?</b><span>The group chat has forty messages a day and most of them aren't about the band.</span></div>
    <div><b>Why?</b><span>Because it is also the friends chat. There is no separate place where band things live.</span></div>
    <div><b>Can you act on it?</b><span>Yes. Fix a standing time, Thursdays at 5, and make a chat that only has practice in it. Nobody needs to be reminded of a standing time.</span></div>
  </div>
  <p class="dim">Notice where it would have been easy to stop. "Two people didn't turn up" is true and fixes nothing. "They mute the chat" is true and turns into a row. The strainer is the separate chat.</p>
</div>""",
    falls="""
<p>It assumes one chain of causes. Real problems often have several, and 5 Whys will find whichever chain you happened to start down, then declare it the cause. It is also very easy to reason your way to the cause you already believed in, because each why is answered by the same person who holds the belief. Two people doing it separately and comparing chains is the cheap fix for both.</p>
<p>The technique has been criticised seriously in healthcare, where it was widely adopted for investigating incidents. Alan Card's 2017 paper argued that it oversimplifies, invites blame, and stops at whatever the investigator finds satisfying. Those are fair. They are also arguments for running it honestly rather than for not running it.</p>""",
    pairs=[
        ("Cause and Effect", "Go wide first when the problem has many possible causes, then take the two or three most likely into 5 Whys."),
        ("Theory of Constraints", "When the fifth why is \"because there is never enough time\", the constraint is the real problem."),
        ("Pre-mortem", "Once you have the fix, imagine it failed and ask why. It is 5 Whys pointed forwards."),
    ],
    reading=[
        "Taiichi Ohno, Toyota Production System: Beyond Large-Scale Production. Written in 1978, published in English in 1988. The fuse example is in chapter one.",
        "Alan J. Card, \"The problem with '5 whys'\", BMJ Quality and Safety, 2017. The honest critique.",
    ],
    try_="Say it is a Problem, open a step, choose Apply a framework and pick 5 Whys. You see exactly what it proposes before anything is added.",
    cta="Start with the thing that keeps going wrong.",
))

METHODS.append(dict(
    slug="working-backwards", name="Working Backwards", kind="a Project or a Goal",
    desc="Where Working Backwards came from, why it works, and how to run it: Amazon's way of defining done before you start, then walking back to now.",
    lead="Define what done looks like and the evidence that would prove it, then walk back to now, so every step exists because the one after it needs it.",
    facts=dict(origin="Amazon, early 2000s", best="a Project, a Goal", takes="An hour, then revisits", needs="Honesty about what done is, and who says so"),
    origin="""
<p>Amazon, in the years around 2004. Before a team could build a new product, they had to write the press release announcing it as if it had already shipped, and then the list of questions a sceptical customer or journalist would ask about it. The document was usually six pages. If the press release wasn't something a customer would want to read, the product wasn't built, and if the questions couldn't be answered, the team went away and worked out how.</p>
<p>The Kindle was developed this way, and so were most of the products Amazon launched over the following fifteen years. Colin Bryar and Bill Carr, who ran the process from the inside, wrote it up in a 2021 book of the same name. Inside Amazon the document is still called the PR/FAQ.</p>
<p>The idea is older than Amazon. Any good engineer designs from the requirement back, and any good cook reads the recipe from the plate. What Amazon added was the rule that you write the ending first, in the customer's words, before anyone is allowed to fall in love with a way of getting there.</p>""",
    works="""
<p>Most plans fail before they start, because "done" was never defined. People begin with the first step because it is the one they can see, and by the time they look up they have built a great deal of something that turns out not to be the thing.</p>
<p>Starting from the finished thing forces you to describe success concretely, as a state of the world somebody could observe, and to name who would have to agree it is done. Done is a judgement a particular person makes, not a feeling the team has. Then walking backwards gives you the plan for free, because each step is simply "what has to be true just before this?". A milestone that doesn't say what it stands on is a list item; one that does is part of a walk.</p>""",
    when="""
<p>Reach for it when you are setting out to make something that will finish, or aiming at a goal you can picture. It is especially useful when a lot of people have opinions about how to do the thing and nobody has said what the thing is.</p>
<p>It is less useful for a problem to be diagnosed, where the end state is "the problem has gone" and the work is all in finding out why it is there. Use 5 Whys or the fishbone for that. In Greggle, Working Backwards is suggested second on a Project and on a Goal, after a Pre-mortem.</p>""",
    steps=[
        "Write done as a state of the world, not an activity, dated in the future, as a stranger would report it. Name who would have to agree it is done.",
        "List the evidence that would prove it. Numbers where there are numbers. Something a person outside the work could point at.",
        "Write the questions a sceptic would ask. How much did it cost? What went wrong? Why hasn't someone done this already? Answer each honestly, and notice which you can't.",
        "Now walk back. What has to be true just before that ending? Write it as something that has become true, say how you would see it, and say what must already be true just before it.",
        "Keep walking until the chain touches today. Then say honestly where you actually are, which is rarely where the chain assumed.",
        "Name the first move, the one you could make this week from exactly here, and write down what the chain still assumes.",
    ],
    board_intro="Pick Working Backwards on a Project or Goal board and Greggle proposes three steps: the ending, the walk back, and where it meets today. The walk starts with three milestones and takes up to twelve.",
    board=[
        dict(label="1", name="What done looks like", text="What is true when this is done. The evidence that would prove it. Who says it is done. By when, if it matters."),
        dict(label="2", name="The walk back", text="Milestones, three to start. Each is a state that has become true, walking from done toward today."),
        dict(label="each milestone", name="What is true at this point", text="How you would see it. What must already be true just before this. How firm its date is: fixed, target or undated."),
        dict(label="3", name="Where it meets today", text="Where you actually are. What the chain still assumes."),
        dict(label="action", name="The first move", text="The one you could make this week from exactly here. Marked as an action.", action=True),
        dict(label="not on the board", name="The sceptic's questions", text="Amazon's FAQ isn't a step. Ask its questions of step 1 before you walk."),
    ],
    checks=[
        "Milestones have been written and not one says how you would see it. A milestone nobody can see is passed without anyone noticing.",
        "Not one milestone says what must already be true first, which means this was written forwards and reversed, or is simply a list.",
        "A milestone just says the goal again instead of being a step on the way to it.",
        "A milestone carries a hard deadline with nothing behind it.",
    ],
    example="""
<div class="card example">
  <span class="stated">a Project &middot; the science fair project</span>
  <p><b>Done.</b> It is the evening of 14 March. A working model showing how much energy the school's south roof could collect from the sun stands on the table in the hall. Visitors press a button and see the number for today's weather. The head of science has said it can stay for open evening.</p>
  <p><b>Evidence.</b> The model works when a stranger presses the button. The number it shows matches a real reading to within ten per cent. Three judges' comments, and a placing.</p>
  <p><b>Who says it is done.</b> The head of science, on the night.</p>
  <p><b>The sceptic.</b> How much did it cost? Under forty pounds, because the sensor is borrowed from the physics cupboard. What went wrong? The first sensor reading was nonsense and it took a week to find out why. Why hasn't someone done this? Someone probably has, so the display has to make it interesting rather than the idea.</p>
  <div class="qa">
    <div><b>The week before</b><span>The model has been tested by someone who hasn't seen it before. Seen by: their name on the test sheet. Stands on: the display working. Date: target, 7 March.</span></div>
    <div><b>Two weeks before</b><span>The sensor gives a believable reading and the display shows it. Seen by: the number on screen matching the cupboard's meter. Stands on: having a sensor. Undated.</span></div>
    <div><b>A month before</b><span>The sensor is in hand and gives any reading at all. Seen by: a number, any number, on the laptop. Stands on: the physics department saying yes. Undated.</span></div>
    <div><b>Where it meets today</b><span>I have a laptop and an idea. The chain assumes the physics department will lend the sensor.</span></div>
    <div><b>The first move</b><span>Ask the physics department for the sensor this week. Find one real reading to check against.</span></div>
  </div>
  <p class="dim">The first step turned out to be an email, not a build. That is normal, and it is the point of walking back rather than forward.</p>
</div>""",
    falls="""
<p>It is only as good as the honesty of the ending. If you write the announcement you wish were true rather than one you could earn, the plan inherits the wish, and every backward step is a step towards a fantasy. The sceptic's questions are the protection, and the question people most often skip is "why hasn't someone done this already?".</p>
<p>The other failure is a walk that stops in mid-air. A chain whose earliest milestone is still months away is a plan for the second half of the work. Keep going until a milestone touches something you could do this week, and then say where you really are, which is what the "what the chain still assumes" question is for.</p>""",
    pairs=[
        ("Pre-mortem", "Greggle suggests the pre-mortem first on a Project, then this. Write the ending, walk back, then imagine it failed and see what the walk missed."),
        ("Objectives and Key Results", "The evidence list is a set of key results. If a goal has no end date, OKRs are the better frame."),
        ("Issue Tree", "When a milestone is too big to see, split it into parts that don't overlap."),
    ],
    reading=[
        "Colin Bryar and Bill Carr, Working Backwards: Insights, Stories, and Secrets from Inside Amazon, 2021. Chapter five is the PR/FAQ.",
        "Jeff Bezos's 2004 letter to shareholders, on why Amazon replaced slides with written narratives.",
    ],
    try_="Say it is a Project or a Goal, open a step, choose Apply a framework and pick Working Backwards. It asks for the ending first.",
    cta="Write the ending first. The plan falls out of it.",
))

METHODS.append(dict(
    slug="pre-mortem", name="Pre-mortem", kind="a Project or a Risk",
    desc="Where the pre-mortem came from, the research behind it, and how to run one: Gary Klein's method for finding the flaws in a plan before it starts.",
    lead="It is twelve months from now and this failed. Work out why, then prevent it.",
    facts=dict(origin="Gary Klein, 2007", best="a Project or a Risk, before it starts", takes="Twenty minutes", needs="Everyone who will do the work"),
    origin="""
<p>Gary Klein is a psychologist who spent his career studying how firefighters, nurses and soldiers make decisions under pressure, and he noticed that once a plan existed, the people on it stopped looking for its flaws. He published the pre-mortem in Harvard Business Review in September 2007 as a short, almost trivially simple fix. Tell the team the plan has failed, and ask them why.</p>
<p>It rests on a 1989 experiment by Deborah Mitchell, Jay Russo and Nancy Pennington. They asked people to explain a future event. Some were told it might happen; others were told it had happened, and to explain it in hindsight. The second group came up with about thirty per cent more reasons, and more specific ones. They called it prospective hindsight. Certainty, even pretend certainty, unlocks reasons that possibility doesn't.</p>
<p>Daniel Kahneman gave the pre-mortem a page of Thinking, Fast and Slow and has recommended it as his preferred check on overconfidence. It costs almost nothing, which is why it is worth running on almost everything.</p>""",
    works="""
<p>Doubt feels disloyal. Once a group has agreed a plan, pointing out how it might fail sounds like an accusation against whoever proposed it, so people don't. The pre-mortem makes the failure a premise instead of a prediction. You aren't saying it might fail. You have been told it did, and your job is to be the person who explains why. Everyone gets permission to be the pessimist at once.</p>
<p>The past tense matters. "We ran out of money" comes out of a different part of the head than "we might run out of money". So does the silent writing: if the room talks, the first confident voice sets the list and everyone else adds variations. If everyone writes alone first, you get the quiet person's reason, which is often the one nobody else saw.</p>""",
    when="""
<p>Reach for it when a plan exists and hasn't started. That is the window. Run it too early and there is nothing to break; run it once the work is under way and it turns into a list of excuses for what is already going wrong.</p>
<p>It is also useful on a decision you have nearly made. Tell yourself you chose the thing and it went badly, and see what comes to mind. If nothing does, that is worth knowing too. Greggle suggests it first on a Goal, a Project and a Risk, and on a Decision and an Opportunity as well: five of the seven kinds.</p>""",
    steps=[
        "State what you are about to commit to, in a few lines, and when you would know whether it had worked.",
        "Announce it. \"It is a year from today. This went badly. Not slightly, badly.\" Say it as a fact.",
        "Everyone writes, alone and in silence, every cause they can think of, in the past tense. Two minutes. Nobody talks.",
        "Go round the room. Each person reads one cause. Keep going round until the lists are empty. No discussion yet, and no defending the plan.",
        "Judge each cause against the others: how likely is it really, and how bad would it be? Fatal means the whole thing fails. Serious means a major delay or cost. Annoying means you'd recover.",
        "For each cause worth acting on, write something you could start this month, and say whether you are preventing it, reducing it, or accepting it. An accepted risk gets its reason written beside it.",
    ],
    board_intro="Pick Pre-mortem on a Project board and Greggle asks what you are committing to and when you would know, then proposes two steps: why it failed, with four causes to start, and what to do about it now, with three actions to start. Both take up to twelve.",
    board=[
        dict(label="the plan", name="What you are about to commit to", text="And when you would know whether it had worked."),
        dict(label="1", name="Why it failed", text="It is twelve months from now. This went badly. Looking back, what caused it? Four causes to start."),
        dict(label="each cause", name="What went wrong", text="Past tense. How likely is it really, against the others? How bad: fatal, serious or annoying?"),
        dict(label="2", name="What to do about it now", text="Each cause worth acting on becomes something you can start this month. Three to start."),
        dict(label="each action", name="What to do, and which cause it addresses", text="Prevent it, reduce it, or accept it. If accepting, why.", action=True),
        dict(label="not on the board", name="The silent two minutes", text="The app lays out the pieces. The rule that nobody talks first is yours to keep."),
    ],
    checks=[
        "The failure has been imagined and nothing has been written under what to do about it.",
        "None of the causes would actually sink this. The awkward cause is the one that got left out.",
        "All the causes carry the same likelihood, which is a form filled in rather than a judgement made.",
        "A cause is accepted and does not say why. A month from now it will look identical to one nobody noticed.",
    ],
    example="""
<div class="card example">
  <span class="stated">a Project &middot; a stall at the Saturday market</span>
  <p><b>The plan.</b> Rent a stall for four Saturdays in November selling the baked things that sell well at school. Split the profit three ways. We would know by the end of November: did it cover the stall fees, and are we still friends.</p>
  <p><b>The news.</b> It is next spring. The stall lost money and two of the three of you aren't speaking.</p>
  <div class="qa">
    <div><b>Causes</b><span>It rained on two of the four Saturdays and nobody came. We baked too much on the first day and threw half away. Only one of us could actually get there at 6am with the trays. We never agreed what to do if someone couldn't make it. The council wanted a food hygiene certificate we didn't have. The person whose kitchen we used got fed up with the mess. The pricing was guessed and we sold out of the cheap thing and nothing else.</span></div>
    <div><b>Judged</b><span>The 6am problem: very likely, serious. The hygiene certificate: possible, fatal, because no certificate means no stall. Baking blind on day one: very likely, annoying. The unspoken sharing rule: possible, fatal to the friendship. The rain: possible, serious.</span></div>
    <div><b>Actions</b><span>Check the council's rules before paying for the stall (prevents the certificate). Do the first Saturday with half the stock and count what sells (reduces the waste). Write down, now, who does what if one of us is ill, and what happens to their share (prevents the row). Ask the one who can do 6am whether they actually want to, and pay them for it (reduces the 6am problem).</span></div>
    <div><b>Accepted</b><span>The rain. Reason: we can't move the market indoors, and two dry Saturdays out of four should still cover the fees. If the first Saturday's takings don't cover the stall fee, stop after the second and talk before the third.</span></div>
  </div>
  <p class="dim">Notice that the reason most likely to end friendships was the one about sharing, and it took a pretend failure to say it out loud. Notice too that accepting the rain, with the reason written down, is a real answer. Never mentioning it is not.</p>
</div>""",
    falls="""
<p>Done as a discussion instead of silent writing first, the loudest voice sets the list. Done by one person alone, it still works, but you only get one person's blind spots. Done too late, it becomes a post-mortem with extra steps.</p>
<p>The other failure is stopping after the list. A pre-mortem that produces twelve causes and no changes to the plan was a nice conversation. The value is entirely in the actions at the end, each one naming the cause it answers, and in the honest decision to accept the causes you can't prevent, with the reason written down.</p>""",
    pairs=[
        ("Working Backwards", "Write the ending first, plan back to now, then run a pre-mortem on the plan. One walk forward and one back."),
        ("Scenario Planning", "When the causes of failure are outside your control, the weather or the council, build the futures instead of trying to prevent them."),
        ("5 Whys", "A cause that surprises you deserves five whys of its own."),
    ],
    reading=[
        "Gary Klein, \"Performing a Project Premortem\", Harvard Business Review, September 2007. Two pages.",
        "Deborah J. Mitchell, J. Edward Russo and Nancy Pennington, \"Back to the future: Temporal perspective in the explanation of events\", Journal of Behavioral Decision Making, 1989.",
        "Daniel Kahneman, Thinking, Fast and Slow, 2011, chapter 24.",
    ],
    try_="Say it is a Project or a Risk, open a step, choose Apply a framework and pick Pre-mortem. It is the first one suggested.",
    cta="Tell yourself it failed. Then find out why.",
))

METHODS.append(dict(
    slug="first-principles", name="First Principles", kind="a Challenge or a Decision",
    desc="Where first principles thinking came from, why it works, when it is the wrong tool, and how to run it: Aristotle's method for reasoning from what is actually true.",
    lead="Find the truths nothing else rests on, then build up from them alone.",
    facts=dict(origin="Aristotle, fourth century BC", best="a Challenge, a Decision, a Problem, a Goal", takes="An hour, done properly", needs="A willingness to look stupid"),
    origin="""
<p>Aristotle opens his Physics by saying that we think we understand a thing when we know its first causes and first principles, the basic truths that don't rest on anything else. Everything we know about a subject is either one of those, or built on them. The Greek word is arche, a beginning.</p>
<p>Descartes rebuilt the whole of philosophy this way in 1637, doubting everything he could doubt until he found something he couldn't, and starting again from there. Engineers and physicists have worked this way ever since, mostly without naming it. The method came back into everyday conversation around 2012, when Elon Musk described using it to argue that battery packs didn't have to cost what they cost. What are batteries made of? Cobalt, nickel, aluminium, carbon, some polymers, a can. What do those cost on the metals exchange? A small fraction of the price of a pack. So the price is a fact about how packs are currently made, not a fact about batteries.</p>
<p>That example has been repeated so often it has become a cliche, which is a shame, because the move underneath it is sound and rare. Greggle calls its version First Principles Analysis, and adds a rebuild step that the bare method leaves out.</p>""",
    works="""
<p>Almost all reasoning is by analogy. This is like that, so do what worked for that. Analogy is fast, and most of the time it is right, which is why we use it. But it carries every assumption of the thing you compared to, and you never see those assumptions because you never chose them.</p>
<p>Going back to what is actually true strips the inherited assumptions out. Quite often the "impossible" part of a challenge was never a fact about the world at all. It was a fact about how everyone has been doing it, dressed up as a law. Naming where each assumption came from, convention, imitation, precedent, fear or nobody ever asking, is what makes it arguable rather than invisible.</p>""",
    when="""
<p>Reach for it when the standard answer doesn't fit and you can feel it, when everyone agrees something can't be done and nobody can say why, or when you have tried the obvious things and they haven't worked. It suits a Challenge, where the outcome isn't in your control and you need an edge nobody else has looked for, and a Decision where the options on the table all feel like someone else's.</p>
<p>Don't use it on things other people have already worked out properly. Reasoning from first principles about how to boil an egg is a way of spending an hour to arrive where a recipe would have taken you in a minute. It is also slow and a bit arrogant, and both are fine as long as you reserve it for where they pay. Greggle suggests it on a Goal, a Challenge, a Problem and a Decision.</p>""",
    steps=[
        "Describe the situation with enough detail to tell your actual constraints from your assumptions. Say what you know is true and what you believe is true.",
        "Surface the assumptions. One sentence each. For each, say where it comes from: convention, imitation, precedent, fear, or an unexamined default. Then judge how much weight it carries: if it were false, would the problem change shape?",
        "Strip them away. What remains that is true regardless? Test each candidate three ways: still true if everyone else doing this vanished tomorrow; still true if you had never tried anything before; sayable without \"that's how it's done\". Aim for three to seven that pass all three.",
        "Rebuild from those alone, three ways, as if no prior approach existed. One optimised for speed, one for the biggest long-term result, one for simplicity. For each, write the chain from principle to action.",
        "Find the high-leverage move: the one action first principles makes visible that conventional thinking hides. Say why it was hidden, and name the first concrete step.",
        "If no single move dominates, write down the runner-up and the trade-off, and choose anyway.",
    ],
    board_intro="Pick First Principles on a Challenge or Decision board and Greggle proposes four phases: surface the assumptions, establish the principles, rebuild three ways, and the high-leverage move. The assumptions and principles are yours to write.",
    board=[
        dict(label="phase 1", name="Surface the assumptions", text="Three to start, up to twelve. Each in one sentence, with where it came from and how load-bearing it is. Then: is the framing mostly sound?"),
        dict(label="phase 2", name="Establish first principles", text="Three to seven. Each stated so plainly an outsider could check it, and ticked against three tests. All three, or it is a belief in a principle's clothing."),
        dict(label="phase 3", name="Rebuild from the foundation", text="Approach A, optimised for speed. B, for impact. C, for simplicity. Each with its reasoning chain from principle to action."),
        dict(label="phase 4", name="The high-leverage move", text="What to do. Why conventional thinking obscures it. The first concrete step.", action=True),
        dict(label="if it's close", name="The runner-up and the trade-off", text="Recorded, so the choice can be revisited without redoing the analysis."),
        dict(label="not on the board", name="The recipe check", text="Before you start, ask whether someone has already worked this out properly. If so, use theirs."),
    ],
    checks=[
        "None of the assumptions is holding the problem up. The load-bearing one is usually the one that felt too obvious to write.",
        "All the assumptions come from the same place, which usually means only one kind was looked for.",
        "Not one principle survives its competitors vanishing. A statement that stops being true when the others do is a description of them, not a principle.",
        "An approach names no principles it rests on, which makes it an ordinary idea that happens to sit below phase 2.",
    ],
    example="""
<div class="card example">
  <span class="stated">a Challenge &middot; the debating final</span>
  <p><b>The challenge.</b> Win the final against the school that has won it four years running. Known true: there are two speakers each, four minutes each, and three judges. Believed: they are better than us.</p>
  <div class="qa">
    <div><b>Assumptions</b><span>"They are better speakers than us." Precedent, high. "You win debates by being confident." Convention, medium. "The judges like them." Fear, low. "We should prepare more arguments than they have." Unexamined default, high. Framing mostly sound? Mostly, except "beat them" really means "score more on the sheet than them".</span></div>
    <div><b>Principles</b><span>The judges score against a published sheet: true if the other school vanished, true if we'd never debated, sayable without any norm. Passes. The sheet gives more marks for rebuttal than for opening argument. Passes. Each speaker has four minutes and the clock is enforced. Passes. "Their last three finals were won on rebuttal" fails the first test: it is evidence about them, not a principle. Kept as evidence, dropped as a principle.</span></div>
    <div><b>Rebuild</b><span>A, speed: get the sheet, rehearse rebuttal against a timer for two weeks. B, impact: build a bank of rebuttals to every argument on this motion, reusable next year. C, simplicity: two arguments each instead of four, and spend the saved minutes rebutting.</span></div>
    <div><b>The move</b><span>Spend preparation on rebuttal, not on more arguments. Hidden because every team prepares arguments, since that is what preparing looks like. First step: get the judges' scoring sheet from the organisers this week. Runner-up: B, which costs time we don't have before the final.</span></div>
  </div>
  <p class="dim">The plan looks odd, because it involves preparing fewer arguments for a debating final. That oddness is what first principles buys you. Everyone else is preparing more.</p>
</div>""",
    falls="""
<p>It is slow, and it is easy to mistake a strongly held belief for a first principle. That is what the three tests are for, and they have to be applied honestly. If everything you wrote passes all three, you weren't testing.</p>
<p>The other trap is contempt for the people who did it the old way. Sometimes the old way is old because it works and the reasons have been forgotten. First principles should make you check the old way, not sneer at it. If your rebuilt plan is wildly different from what everyone else does, treat that as a reason to look harder, then proceed if it holds.</p>""",
    pairs=[
        ("Options and Criteria", "Greggle calls it the missing half of this method: first principles gives you three approaches and nothing for choosing between them. That is where they get compared."),
        ("Issue Tree", "Once the principles are clear, the tree is how you turn them into parts you can work on."),
        ("Strategic Challenge Map", "When there are many challenges and you need to know which one to attack, map them first, then go to first principles on the crux."),
    ],
    reading=[
        "Aristotle, Physics, book one, chapter one; Metaphysics, book one. Any translation. The opening lines of the Physics are the whole idea.",
        "Rene Descartes, Discourse on the Method, 1637. Short, and still readable.",
    ],
    try_="Say it is a Challenge or a Decision, open a step, choose Apply a framework and pick First Principles Analysis. It asks for your assumptions, then tests them.",
    cta="Find out what is actually true. Build from only that.",
))

METHODS.append(dict(
    slug="force-field-analysis", name="Force Field Analysis", kind="a Decision or a stalled Goal",
    desc="Where force field analysis came from, why removing a restraint beats pushing harder, and how to run it: Kurt Lewin's method for shifting something that has stuck.",
    lead="What is pushing for the change, what is holding it back, and which single restraint you could actually remove.",
    facts=dict(origin="Kurt Lewin, 1940s", best="a Decision, a Goal that has stalled, an Opportunity, a Risk", takes="Twenty minutes", needs="Honesty about what is holding you back, and a name"),
    origin="""
<p>Kurt Lewin was a German psychologist who left Berlin for America in 1933 and, in the fourteen years before his death in 1947, founded most of what is now called social psychology. He thought of any situation, a person, a group, a factory floor, as a field of forces held in balance. Some push towards a change; some hold it back. Nothing moves while they balance. Something moves when they don't.</p>
<p>His observation, which is the whole method, is that there are two ways to unbalance the field, and they are not equal. You can push harder. Or you can remove something that is holding the change back. Pushing harder works briefly and raises resistance, because the restraining forces push back in proportion. Removing a restraint lets the change happen with the push you already have. Lewin's papers were collected as Field Theory in Social Science in 1951, after he died. The analysis, drawn as two columns of arrows pointing at a line, has been used in change management ever since.</p>""",
    works="""
<p>It makes you write the things holding you back in a separate column from the things pushing you forward, and then it makes you choose one restraint to remove. Most people, when something has stalled, only ever add more push: more motivation, more reminders, more pressure. The restraints are still there, so the thing stays stalled and now everyone is tired.</p>
<p>Naming the restraints one by one, weighing them against each other and asking who could move each one shows that they are not all equal and that at least one is usually cheap to remove. That one, with a method and a name against it, is the action.</p>""",
    when="""
<p>Reach for it when you are deciding whether to change something, or when a goal you have been pushing towards has stopped moving. It suits a change that involves other people particularly well, because the restraints are usually other people's, and this makes you write them down as forces rather than as villains.</p>
<p>It is the wrong tool for choosing between several options; that is Options and Criteria. It is also weak on a change you don't yet want, since the whole method assumes the push exists. Greggle suggests it on a Goal, a Decision, an Opportunity and a Risk, and first of all on an Opportunity.</p>""",
    steps=[
        "Write the change as a movement from one state to another, and be honest about what happens if nothing changes at all.",
        "Left column, everything pushing for it. Include the forces you did not create and do not control: a deadline, a rule, someone else's decision. For each, say whose force it is.",
        "Right column, everything holding it back. Be specific enough that somebody could go and do something about each one. Include the ones that are about you.",
        "Weigh every force against the others: strong, moderate or weak. Words, not numbers, and relative, not absolute.",
        "For each restraint, ask: could it be removed entirely, weakened, or neither? For anything removable or weakenable, write who would do it. A name.",
        "Pick one restraint. Not the largest, the one where the effort you can actually spend produces the most movement. Say how it gets removed and what moves once it is gone. One restraint, one method, one name.",
    ],
    board_intro="Pick Force Field Analysis on a Goal or Decision board and Greggle proposes four steps: the change, what is pushing for it, what is holding it back, and the one to remove. Each column starts with three forces and takes up to twelve.",
    board=[
        dict(label="1", name="The change", text="The change being proposed, as a movement from one state to another. What happens if nothing changes."),
        dict(label="2", name="What is pushing for it", text="Each force: strong, moderate or weak against the others, and whose force it is."),
        dict(label="3", name="What is holding it back", text="Each force weighed the same way, plus: could it be removed, weakened, or neither? And who would move it."),
        dict(label="4", name="The one to remove", text="Which restraint. How it gets removed or weakened. What moves once it is gone.", action=True),
        dict(label="the rule", name="One restraint, one method, one name", text="Not the largest restraint. The one where effort you can spend produces the most movement."),
        dict(label="not on the board", name="The arrows", text="The classic diagram draws the forces as arrows of different lengths. The words do the same job."),
    ],
    checks=[
        "The forces for the change have been written out and the forces against it left blank. That is wishful thinking on paper.",
        "Forces have been listed and none is weighed against the others. An unweighted list says everything matters equally.",
        "A restraint you have judged removable has no name beside it, which is the commonest way this method produces a tidy board and no change.",
    ],
    example="""
<div class="card example">
  <span class="stated">a Goal &middot; make the first team this season</span>
  <p><b>The change.</b> From training with the seconds to being picked for the first team for the second half of the season. If nothing changes: another season in the seconds, and next year the year below start overtaking.</p>
  <div class="tablewrap"><table>
    <tr><th>Pushing for it</th><th>How strong</th><th>Whose force</th></tr>
    <tr><td>Fitness is better than last year</td><td>Moderate</td><td>Mine</td></tr>
    <tr><td>The coach has said I am close</td><td>Moderate</td><td>The coach</td></tr>
    <tr><td>Two first-team players leave at Christmas</td><td>Strong</td><td>The calendar</td></tr>
    <tr><td>A friend already on the team who talks me up</td><td>Weak</td><td>Sam</td></tr>
  </table></div>
  <div class="tablewrap"><table>
    <tr><th>Holding it back</th><th>How strong</th><th>Could it be moved</th><th>Who would move it</th></tr>
    <tr><td>Tuesday training clashes with my shift at the shop</td><td>Strong</td><td>Removed</td><td>Me, and the shop manager</td></tr>
    <tr><td>No lift to Saturday away matches</td><td>Moderate</td><td>Weakened</td><td>Me, asking at Tuesday training</td></tr>
    <tr><td>The current player in my position is popular</td><td>Moderate</td><td>Neither</td><td>Plan around it</td></tr>
    <tr><td>I get nervous in trials and play worse than in training</td><td>Strong</td><td>Weakened</td><td>Me, slowly</td></tr>
  </table></div>
  <div class="qa">
    <div><b>The one to remove</b><span>The shift clash. It is strong and it is the only restraint that could be removed outright, in one conversation about swapping Tuesday for Sunday. The nerves are just as strong but slow to weaken. The popular player isn't a restraint to remove at all.</span></div>
    <div><b>How</b><span>Ask the manager this week about moving the Tuesday shift. If yes, be at every Tuesday training until Christmas.</span></div>
    <div><b>What moves once it's gone</b><span>Being at Tuesdays probably solves the lift as well, because someone at Tuesday training drives to Saturday matches. Two restraints for one conversation.</span></div>
  </div>
  <p class="dim">Left to itself, the instinct is to add push: train harder, want it more. The field says the fastest way to move is to stop missing Tuesdays.</p>
</div>""",
    falls="""
<p>The classic version scores each force out of five, and people add the columns up, get 15 against 16, and conclude the change is impossible by one point. The scores were only ever there to rank the restraints. Greggle uses three words instead of numbers for exactly this reason: a ranking is what you need and a total is what misleads you.</p>
<p>It is also easy to fill the right-hand column with other people and leave yourself out. The restraint that is about you, the nerves in the example, is often the one that matters most in the long run even if it isn't the one to remove first. Write it down anyway. And a restraint judged removable with nobody's name beside it is a wish, not a plan.</p>""",
    pairs=[
        ("Stakeholder and Influence Map", "When most of the restraints are people, map them properly: what does each one actually want?"),
        ("5 Whys", "A restraint that is strong deserves to be asked why, five times. It may not be what it looks like."),
        ("Options and Criteria", "If the field shows the change is worth making, and there are several ways to make it, choose between them with criteria written first."),
    ],
    reading=[
        "Kurt Lewin, Field Theory in Social Science, 1951, edited by Dorwin Cartwright. The force field is in the papers on group decision and social change.",
        "Kurt Lewin, \"Frontiers in Group Dynamics\", Human Relations, 1947. Where unfreezing, moving and refreezing first appear.",
    ],
    try_="Say it is a Goal, a Decision, an Opportunity or a Risk, open a step, choose Apply a framework and pick Force Field Analysis. It sets up both columns.",
    cta="Stop pushing harder. Remove one thing that is holding it back.",
))

METHODS.append(dict(
    slug="options-and-criteria", name="Options and Criteria", kind="a Decision",
    desc="Where the decision matrix came from, why the order of the steps is the whole method, and why Greggle leaves out the arithmetic: from Franklin's prudential algebra to a judgement you can defend.",
    lead="Write down what a good answer would have to do before you look at the answers, then say honestly what each one costs.",
    facts=dict(origin="Franklin, 1772; Kepner and Tregoe, 1965", best="a Decision, an Opportunity", takes="Half an hour", needs="Criteria written before the options"),
    origin="""
<p>Older than any company. In September 1772 Benjamin Franklin wrote to his friend Joseph Priestley, who was agonising over a job offer, and described what he called his moral or prudential algebra. Draw a line down a sheet of paper. Write the reasons for on one side, the reasons against on the other, over three or four days as they occur to you. Then strike out pairs of equal weight, a "for" against an "against", two weak ones against one strong one, until one side is empty. What remains is the answer, and it is an answer you can explain.</p>
<p>Charles Kepner and Benjamin Tregoe, two researchers who met at the RAND Corporation in the 1950s, turned the same instinct into a formal method for managers, published in The Rational Manager in 1965. Their decision analysis separates the criteria into musts, which any option has to satisfy or it is out, and wants, which are weighted and scored. Stuart Pugh's concept selection matrix, from 1981, is the engineering version, where options are scored against a reference design rather than against each other.</p>
<p>Everyone has seen the grid. What almost nobody does is fill it in in the right order. Greggle keeps the sequence and the must-or-want split, and drops the arithmetic on purpose: it asks which option wins on which criterion and what each one costs, because a weighted total hides the judgement you are actually making behind numbers nobody checks.</p>""",
    works="""
<p>The matrix is almost beside the point. The sequence is the method. If you list the options first, the one you already like starts writing its own criteria: it is fast, so speed becomes a criterion; it is cheap, so cost becomes one. By the time you compare, the answer was decided before the grid existed, and the grid is just an alibi.</p>
<p>Writing down what a good answer would have to do, before any answer is on the table, stops that. The musts do most of the work: options that fail one are gone, and often that leaves two. Then the honest question is what each survivor costs. An option that loses on nothing was written after the conclusion.</p>""",
    when="""
<p>Reach for it when there is a genuine choice between several things and you can feel your preference pulling you before you have thought. It suits a Decision above all, and an Opportunity where the choice is whether to pursue it at all, with "do nothing" as one of the options.</p>
<p>It is the wrong tool when there is only one option and the question is whether to take it; that is Force Field Analysis. It is also weak on a choice whose outcome depends heavily on things outside your control, where Scenario Planning does better. Greggle suggests it on a Decision and on an Opportunity.</p>""",
    steps=[
        "Write the choice: what is being chosen, by when, and what is not on the table. Name the decision, not the outcome you are hoping for.",
        "Before listing any option, write the criteria. For each, say whether an option must meet it or you would merely like it to, and how you would tell. Check that no two measure the same thing; if they overlap, say which one owns it.",
        "Only now list the options. At least three, and one of them is doing nothing. Deferring counts, if you say what you are waiting for.",
        "Strike out any option that fails a must, whatever else it does.",
        "For each survivor, say what it wins on, naming the criteria rather than qualities, and what it costs. No totals. Every option gives something up.",
        "Make the call: one option, why it over the runner-up, and what would reverse it. Writing down what would change your mind now is what lets you change it later without a fight.",
    ],
    board_intro="Pick Options and Criteria on a Decision board and Greggle proposes the choice, then the criteria, then the options, then the call. The criteria come before the options on the board, and the check complains if you fill them in the other way round.",
    board=[
        dict(label="1", name="The choice", text="What is being chosen. By when. What is not on the table."),
        dict(label="2", name="What a good answer must do", text="Three criteria to start, up to eight. Each: must, or would like? How you would tell. Does it overlap another?"),
        dict(label="3", name="The options", text="Three to six. Each: a change, do nothing, or defer. What it wins on. What it costs and where it loses. Does it fail a must?"),
        dict(label="each option", name="Where it ends up", text="Recommended, runner-up with a reason, or rejected."),
        dict(label="4", name="The call", text="The option chosen. Why it, over the runner-up. What would reverse this.", action=True),
        dict(label="not on the board", name="The weighted total", text="Left out deliberately. Say which option wins on which criterion instead."),
    ],
    checks=[
        "The options have been listed and what a good answer must do has not.",
        "Doing nothing is not among the options, so every option looks better than it is.",
        "Not one option says what it gives up, which is the signature of criteria written after the conclusion.",
        "The recommended option doesn't say what it costs. Say it yourself before somebody else does.",
    ],
    example="""
<div class="card example">
  <span class="stated">a Decision &middot; which subjects to take next year</span>
  <div class="qa">
    <div><b>The choice</b><span>Three subjects alongside maths, by the options deadline in March. Not on the table: dropping maths, which the school won't allow.</span></div>
    <div><b>Musts</b><span>Keeps both university courses I am considering open (tell: their published entry requirements). No timetable clash (tell: the blocks sheet). A B or better in it now, or it is new (tell: last report).</span></div>
    <div><b>Would likes</b><span>I would turn up to it gladly (tell: did I do the homework this year without being asked). Useful whatever I end up doing. A teacher I work well with. "Friends in the class" was struck: it overlaps with turning up gladly, and that one owns it.</span></div>
    <div><b>Options</b><span>A: Physics, Chemistry, History. B: Physics, History, Economics. C: Physics, Chemistry, Economics. D, do nothing: leave the form's default, Physics, Chemistry and Further Maths. Art never appears because it clashes with everything.</span></div>
    <div><b>Musts applied</b><span>D fails: Further Maths needs an A now and I have a B. Out. Physics alone keeps both courses open, so A, B and C all pass.</span></div>
    <div><b>A</b><span>Wins on: both courses open, useful. Costs: Chemistry is the homework I do last, and its teacher is the one I don't work with. Runner-up.</span></div>
    <div><b>B</b><span>Wins on: turn up gladly, both teachers, both courses open. Costs: Economics is new, so it is an unknown, and it is the least obviously useful of the three. Recommended.</span></div>
    <div><b>C</b><span>Wins on: useful. Costs: nothing in it I would turn up gladly for, and two years is a long time. Rejected.</span></div>
    <div><b>The call</b><span>B. Over A because every criterion A loses on is about actually turning up for two years, and A only looks serious. What would reverse it: if the second course's entry requirements turn out to want Chemistry, it is A.</span></div>
  </div>
  <p class="dim">There are no numbers anywhere in that. The decision is in the sentences, where somebody can argue with it. A weighted grid would have put B ahead by six points and hidden the one thing that would reverse it.</p>
</div>""",
    falls="""
<p>The classic weighted grid can be tuned until the favourite wins, and everyone who has used one has done it at least once. Greggle leaves the arithmetic out for that reason, but the same failure survives in words: an option with an empty cost line, criteria quietly rewritten after the options went in, doing nothing left off the list so everything else looks good against nothing.</p>
<p>The protection is the order, kept honestly, and the rule that every option costs something. If the option you recommend has no cost you can name, you haven't examined it, and the first person you show it to will find the cost for you.</p>""",
    pairs=[
        ("First Principles", "Greggle calls this the missing half of that method. First principles generates three approaches; this is where they get compared."),
        ("Scenario Planning", "If the best option changes depending on how the world turns out, judge the options in each future, not just one."),
        ("Answer First", "Once chosen, say it in one sentence with the reasons beneath. The comparison is the evidence, not the answer."),
    ],
    reading=[
        "Benjamin Franklin, letter to Joseph Priestley, 19 September 1772. One page, and worth reading in full.",
        "Charles H. Kepner and Benjamin B. Tregoe, The Rational Manager, 1965. Decision analysis is the middle third.",
        "Stuart Pugh, Total Design, 1991, for concept selection; the method dates from his 1981 conference paper.",
    ],
    try_="Say it is a Decision or an Opportunity, open a step, choose Apply a framework and pick Options and Criteria. It asks for the criteria before the options.",
    cta="Decide what good looks like. Then look at the options.",
))

for m in METHODS:
    m["try"] = m.pop("try_")

write_index()
for m in METHODS:
    write_method(m)
print("wrote", len(METHODS) + 1, "pages")
