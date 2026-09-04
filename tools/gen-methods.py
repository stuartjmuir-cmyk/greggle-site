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

def head(title, desc, canon, image="https://greggle.app/board.jpg", current="methods"):
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
      <a class="navlink" href="/methods/"{' aria-current="page"' if current == "methods" else ''}>Ways of thinking</a>
      <a class="navlink" href="/why/"{' aria-current="page"' if current == "why" else ''}>Why</a>
      <a class="navlink" href="/about/"{' aria-current="page"' if current == "about" else ''}>About</a>
      <a class="btn btn-small" href="https://www.greggle.app/">Open Greggle</a>
    </nav>
  </header>
"""

FOOT = """
  <footer>
    <span class="stated">Greggle &middot; free &middot; no account &middot; works offline</span>
    <span class="stated"><a href="/methods/">ways of thinking</a> &middot; <a href="/why/">why</a> &middot; <a href="/about/">about</a> &middot; <a href="mailto:feedback@greggle.app">feedback@greggle.app</a></span>
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
        ("cause-and-effect", "Cause and Effect", "Kaoru Ishikawa, 1960s", "The fishbone. Go wide across every kind of cause before you go deep on one."),
        ("theory-of-constraints", "Theory of Constraints", "Eliyahu Goldratt, 1984", "Find the one place where the whole flow narrows, and serve it."),
    ]),
    ("Break a big question into parts", "For a Challenge, a Project or a Goal too large to see whole.", [
        ("issue-tree", "Issue Tree", "McKinsey, 1960s", "Split a question into parts that do not overlap and leave nothing out."),
        ("first-principles", "First Principles", "Aristotle", "Find the truths nothing else rests on, then build up from them alone."),
        ("strategic-challenge-map", "Strategic Challenge Map", "Greggle&rsquo;s own synthesis", "Categorise the challenges, evidence each one, judge what you can move."),
    ]),
    ("Decide between options", "For a Decision, or an Opportunity you have not yet said yes to.", [
        ("options-and-criteria", "Options and Criteria", "Franklin, 1772", "Write down what a good answer would have to do before you look at the answers."),
        ("force-field-analysis", "Force Field Analysis", "Kurt Lewin, 1940s", "What is pushing for the change, what is holding it back, and which single restraint to remove."),
    ]),
    ("Plan towards something", "For a Project with an end, or a Goal without one.", [
        ("working-backwards", "Working Backwards", "Amazon, 2000s", "Define what done looks like and the evidence that would prove it, then walk back to now."),
        ("objectives-and-key-results", "Objectives and Key Results", "Intel, 1970s", "One objective, and the numbers that would prove you reached it."),
    ]),
    ("See what could go wrong", "For a Risk, or any plan before it starts.", [
        ("pre-mortem", "Pre-mortem", "Gary Klein, 2007", "It is twelve months from now and this failed. Work out why, then prevent it."),
        ("scenario-planning", "Scenario Planning", "Shell, 1970s", "Build four futures, decide what you would do in each, plant signposts."),
    ]),
    ("Bring other people with you", "For anything whose outcome depends on someone else.", [
        ("stakeholder-and-influence-map", "Stakeholder and Influence Map", "Freeman and Mendelow, 1980s", "Who decides, who can block it, and what each of them actually wants."),
        ("answer-first", "Answer First", "Barbara Minto, 1970s", "Give the answer in the first sentence, reasons beneath. The consulting habit."),
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


METHODS.append(dict(
    slug="issue-tree", name="Issue Tree", kind="a Challenge, a Problem or a Decision",
    desc="Where the issue tree came from, what MECE actually means, and how to build one: the consulting method for splitting a question into parts that do not overlap and leave nothing out.",
    lead="State the question, split it into parts that do not overlap and leave nothing out, then test the parts that would actually change the answer.",
    facts=dict(origin="McKinsey, 1960s", best="a Challenge, a Problem, a Decision", takes="An hour for the first split", needs="A question, and your best answer to it today"),
    origin="""
<p>McKinsey, and specifically Barbara Minto, who joined the firm in 1963 as one of its first women consultants and was soon asked to teach the others how to write. What she taught was a way of organising thought: any question can be broken into a small number of parts, and a breakdown is only trustworthy if the parts are mutually exclusive and collectively exhaustive. No overlaps, no gaps. The consulting world still says MECE, pronounced "mee-see", and still means her rule.</p>
<p>Her book The Pyramid Principle came out in 1978 and has never gone out of print. The issue tree is the working end of it: the question at the top, the parts beneath, each part split again until the leaves are things you can check. The other half of her book, how to present the answer once you have it, is the method Greggle calls Answer First.</p>
<p>The habit of writing your best answer before you start comes from the same firm. A tree built without a hypothesis finds whatever it was pointed at, and takes far longer doing it.</p>""",
    works="""
<p>A question split into non-overlapping parts can be worked on in pieces, by different people, in any order. The "nothing left out" test catches the branch you forgot about before it becomes the reason the plan failed. And a branch that says what would have to be true, and how you would test it, can be closed. Most questions stay open for years because nobody ever wrote down what would settle them.</p>
<p>Greggle is built in this shape. Every board is a split, and every step is a branch you can open and split again. The issue tree is the method that says out loud what the app does quietly, and adds the two questions the app can't ask for you: does this branch overlap another, and would it change the answer?</p>""",
    when="""
<p>Reach for it when a question is too big to see whole, when several people disagree about it and you suspect they are answering different parts, or when you want to know what to check first. It suits a Challenge, a Problem that has many possible causes, and a Decision where the options haven't yet been separated from the reasons.</p>
<p>It is the wrong tool when the question is really a chain of causes, which is 5 Whys, or when the answer depends mostly on how the future turns out, which is Scenario Planning. Greggle suggests it on a Challenge, a Problem and a Decision.</p>""",
    steps=[
        "Write one question, singular and answerable. Then write your best answer today, before you start, and who decides what once it is answered. If nobody would do anything differently, swap the question for one where they would.",
        "Split the question into two to six parts. Test the split: could a fact belong to two parts? Is there a fact that belongs to none? Write down what the split leaves out, and why you cut it this way rather than the obvious other way.",
        "For each part, say what would have to be true for it to hold, stated so that it could turn out false, and how you would actually test it. \"More analysis\" is not a test.",
        "Judge each part: if it holds, does it settle the question, narrow it, or barely move it? Most parts are not decisive. If you have marked them all decisive, you have marked none.",
        "Open the parts that would change the answer and split them again. Leave the others whole. Depth on the interesting branch instead of the decisive one is the commonest failure.",
        "Pick the test to run first: the one that moves the answer furthest for the least effort. Give it a date and write down what result would change your mind.",
    ],
    board_intro="Pick Issue Tree on a Challenge, Problem or Decision board and Greggle proposes the question, the first split with three branches, and what to test first. The depth comes from you: open any branch and split it again.",
    board=[
        dict(label="1", name="The question", text="Answerable and singular. Your best answer today, said before you start. The decision this informs."),
        dict(label="2", name="The split", text="What this split leaves out. Why cut it this way. Then the branches: three to start, two to six."),
        dict(label="each branch", name="This part of the question", text="Does it overlap another, and if so which one owns it? What would have to be true? How you would test it? If it holds: settles, narrows, or barely moves the question."),
        dict(label="open a branch", name="Split it again", text="Any branch becomes a board of its own. Go deep on the decisive ones and leave the rest whole."),
        dict(label="3", name="What to test first", text="The test to run first. By when. What result would change your mind.", action=True),
        dict(label="not on the board", name="MECE", text="The app can't judge overlap for you. The two questions on each branch are how you do it yourself."),
    ],
    checks=[
        "Branches have been written and not one says whether it overlaps another. Overlap does the most damage here, because the same thing gets counted twice.",
        "Not one branch says how it would be tested. A tree made of untestable branches organises the question without ever answering it.",
        "None of the branches would settle the question, or all of them carry the same weight, so the tree cannot say what to do first.",
        "One branch has been taken several levels down while another has not been opened at all.",
    ],
    example="""
<div class="card example">
  <span class="stated">a Decision &middot; should we run the market stall again in December?</span>
  <div class="qa">
    <div><b>The question</b><span>Should the three of us rent the stall again for the four Saturdays in December? Best answer today: yes. Decision it informs: whether to pay the December fee, which is due on 20 November.</span></div>
    <div><b>The split</b><span>Did November actually make money, once everything is counted? Would December be different from November? Can the three of us do it in December? Left out: whether we would rather do something else with four Saturdays. Why this cut: it separates facts we can check now from guesses about next month from a conversation the three of us need to have.</span></div>
    <div><b>Branch 1</b><span>Separate. Would have to be true: takings minus ingredients minus the fee was more than we would have earned doing anything else. Test: the takings sheet and the receipts, added up honestly. If it fails, it settles the question.</span></div>
    <div><b>Branch 2</b><span>Separate. Would have to be true: December has more shoppers and no new stall selling the same thing. Test: ask the market manager how many stalls are booked and what last December's footfall was. Narrows it.</span></div>
    <div><b>Branch 3</b><span>Overlaps branch 1 slightly, since the 6am problem cost us stock in November; branch 1 owns that. Would have to be true: nobody has mocks on a December Saturday and the 6am person is still willing. Test: the mocks timetable and one conversation. Settles it if it fails.</span></div>
    <div><b>Test first</b><span>Count November properly, by Tuesday. What would change my mind: if the money after the fee is less than three Saturdays of babysitting, the answer is no, however good December looks.</span></div>
  </div>
  <p class="dim">The best answer was yes. The first test was the one most likely to make it no, which is the right test to run first. Notice that branch 3 turned out to overlap branch 1, and saying which owns the overlap is what stops the 6am problem being counted twice.</p>
</div>""",
    falls="""
<p>Perfect MECE is rarely achievable and chasing it wastes time. Good enough is "I can see no overlap and I can't think of a gap", written down, with what the split leaves out named honestly. A split that claims to leave out nothing without having checked is worse than one that admits what it skipped.</p>
<p>The other failure is depth in the wrong place. The interesting branch gets four levels; the decisive branch gets none. The judgement on each branch, settles, narrows or barely moves, is there to stop that, and it only works if most branches are honestly marked as not decisive.</p>""",
    pairs=[
        ("Answer First", "The other half of Minto's book. The tree is how you work the answer out; Answer First is how you deliver it."),
        ("Cause and Effect", "When the question is \"why did this happen\", the fishbone is an issue tree with the first split already chosen for you."),
        ("First Principles", "When you can't find a split that isn't inherited from how everyone else frames the question, strip the assumptions first."),
    ],
    reading=[
        "Barbara Minto, The Pyramid Principle, 1978; the current edition is The Minto Pyramid Principle, 2009. The logic-tree chapters are the issue tree.",
        "Ethan Rasiel, The McKinsey Way, 1999, on hypothesis-first problem solving, which is where \"your best answer today\" comes from.",
    ],
    try_="Say it is a Challenge, a Problem or a Decision, open a step, choose Apply a framework and pick Issue Tree. Then open any branch and split it again.",
    cta="Split it honestly. Then test the branch that matters.",
))

METHODS.append(dict(
    slug="cause-and-effect", name="Cause and Effect", kind="a Problem",
    desc="Where the fishbone diagram came from, why going wide beats going deep first, and how to run it: Kaoru Ishikawa's method for finding every class of cause before you commit to one.",
    lead="Go wide across the categories before you go deep, so that a whole class of cause is not simply forgotten.",
    facts=dict(origin="Kaoru Ishikawa, 1960s", best="a Problem, a Risk", takes="Forty minutes", needs="Evidence, or the honesty to mark a guess as a guess"),
    origin="""
<p>Kaoru Ishikawa was a professor of engineering at the University of Tokyo and one of the people who built Japan's approach to quality after the war. He is usually credited with drawing the first cause-and-effect diagram for engineers at Kawasaki's shipyards in the 1940s, and he set it out properly in his Guide to Quality Control in 1968, which reached English in 1976. The problem is the fish's head. The ribs are categories of cause. Under each rib, the causes that belong to it.</p>
<p>In a factory the ribs were traditionally the six Ms: manpower, methods, machines, materials, measurement and mother nature, meaning the environment. Ishikawa's insight was less about the picture than about the discipline of working every rib in turn. Left to themselves, people put every cause under the one heading they already suspected, and the diagram made that visible.</p>
<p>Greggle uses six categories that are the same idea in plainer words: people, process, technology, materials and inputs, environment, and measurement.</p>""",
    works="""
<p>Where 5 Whys goes deep on one chain, this goes wide first. The categories force you to consider kinds of cause you would never have thought of on your own, and seeing them all on one page shows which ribs are crowded and which are empty. An empty category is a finding, if you actually looked. A forgotten one is not.</p>
<p>The second half of the discipline is marking each cause as verified, suspected or ruled out, with the evidence beside it. A board of confident guesses is worse than a short board of checked ones, because the guesses harden into facts the third time somebody repeats them.</p>""",
    when="""
<p>Reach for it when a problem feels wide rather than deep: when you can already think of four unrelated reasons, or when 5 Whys keeps producing a different chain each time you run it. It suits a Problem above all, and a Risk that has happened somewhere else and you want to know how it could happen here.</p>
<p>It is the wrong tool for a problem with one obvious chain of causes; go straight to 5 Whys. And it is only useful if it ends with one most likely cause and the test that would settle it. A fishbone that ends with twenty equally plausible causes has organised the problem without advancing it. Greggle suggests it on a Problem and on a Risk.</p>""",
    steps=[
        "Write the effect as something observable: what happened, when it was first seen, and how you know. Not how it felt.",
        "Draw six ribs and name them: people, process, technology, materials and inputs, environment, measurement. Adapt the names if yours are obviously different, but keep six.",
        "Work every rib in turn, and list the causes that could sit under it, one per line, each stated as something that happens or fails to happen. Force at least one weak cause into the ribs you would have skipped.",
        "Beside each cause, write what makes you think so: a log, a message, a thing you saw, a person who saw it. Then mark it verified, suspected or ruled out.",
        "For every cause marked suspected, write the one thing you would look at to check it.",
        "Name the single cause you would bet on, say why in terms of the evidence rather than the conviction, and write the one test that would show you were wrong.",
    ],
    board_intro="Pick Cause and Effect on a Problem board and Greggle proposes the effect, six category steps each holding one cause to start, and the most likely cause at the end. Each category takes up to eight.",
    board=[
        dict(label="1", name="The effect", text="What happened. How you know. When it was first seen."),
        dict(label="2", name="Where the causes might be", text="Six categories, worked one at a time: people, process, technology, materials and inputs, environment, measurement."),
        dict(label="each cause", name="The cause, and what makes you think so", text="Verified, suspected or ruled out. If suspected, how it would be checked."),
        dict(label="2.6", name="Measurement", text="The category people forget: a cause that only exists because the alert was wrong, or nobody was looking."),
        dict(label="3", name="The most likely cause", text="The one you would bet on. Why that one, in terms of the evidence. The test that would settle it.", action=True),
        dict(label="not on the board", name="The fish", text="The app draws it as steps rather than ribs. The order, category by category, is what matters."),
    ],
    checks=[
        "Causes have been written and not one says what makes you think so.",
        "A cause is marked suspected with no way to check it, so it will stay suspected and quietly harden into a fact.",
        "All the causes sit in one category, which usually means thinking stopped where the suspicion started.",
        "A cause just says the effect again in different words.",
    ],
    example="""
<div class="card example">
  <span class="stated">a Problem &middot; the science fair sensor gives nonsense readings</span>
  <div class="qa">
    <div><b>The effect</b><span>The light sensor reads 0 or 1023 and nothing in between, since Tuesday. I know because the laptop log shows only those two values for three days.</span></div>
    <div><b>People</b><span>I wired it from a photo rather than the diagram. Suspected. Check: redo the wiring from the diagram and compare.</span></div>
    <div><b>Process</b><span>There is no calibration step; I just plugged it in. Verified: there is none. Doesn't explain the two-value readings on its own.</span></div>
    <div><b>Technology</b><span>The sensor is the one from the bottom of the physics cupboard and may be broken. Suspected. Check: swap it for the other one.</span></div>
    <div><b>Materials and inputs</b><span>The USB cable is a cheap charging cable that may not carry data. Suspected. Check: use the printer cable. Also: the power comes from the laptop, which throttles USB power on battery. Ruled out, it was plugged in on Tuesday.</span></div>
    <div><b>Environment</b><span>The sensor sits on the windowsill in direct sun, which may saturate it. Verified: it reads 1023 whenever the sun is on it. But it reads 0 at night, not a low number.</span></div>
    <div><b>Measurement</b><span>The code reads the sensor as a digital pin, not an analogue one, so it can only ever give 0 or 1. Suspected. Check: the pin number in the code against the board's diagram.</span></div>
    <div><b>Most likely</b><span>The measurement one. It is the only cause that explains exactly two values and nothing between, and it explains the sun reading too. Test: change the pin from digital to analogue and see whether intermediate values appear.</span></div>
  </div>
  <p class="dim">Left to itself, the investigation would have started with the sensor being broken and stayed there. Working the ribs in order is what reached the measurement rib, and the measurement rib is where the answer was.</p>
</div>""",
    falls="""
<p>The default categories don't suit every problem, and people either force causes into headings that don't fit or skip the headings that feel irrelevant. Adapt the names, keep the number, and force one weak cause into every rib. The weak cause in the rib you nearly skipped is, surprisingly often, the answer.</p>
<p>It also invites a board of confident guesses, all marked as if they were known. The verified, suspected or ruled out marking is the protection, and it only works if suspected is used honestly and carries a check beside it.</p>""",
    pairs=[
        ("5 Whys", "The partner method. Go wide here first, then take the most likely cause into five whys."),
        ("Issue Tree", "A fishbone is an issue tree with the first split chosen for you. When the categories don't fit, build the tree instead."),
        ("Pre-mortem", "For a Risk that hasn't happened yet, the pre-mortem asks the same question in the past tense."),
    ],
    reading=[
        "Kaoru Ishikawa, Guide to Quality Control, 1968; English edition from the Asian Productivity Organization, 1976. The diagram is in the first chapters.",
        "Kaoru Ishikawa, What Is Total Quality Control? The Japanese Way, 1985, for the thinking behind it.",
    ],
    try_="Say it is a Problem or a Risk, open a step, choose Apply a framework and pick Cause and Effect. It lays out the six categories.",
    cta="Look under every heading. Then bet on one.",
))

METHODS.append(dict(
    slug="objectives-and-key-results", name="Objectives and Key Results", kind="a Goal",
    desc="Where OKRs came from, why the discipline lives entirely in the key results, and how to write a set that can be scored honestly: from Andy Grove's Intel to one person's goal.",
    lead="One qualitative objective, a handful of numbers that would prove it, and the bets you are making to move them.",
    facts=dict(origin="Andy Grove, Intel, 1970s", best="a Goal", takes="An hour, then a quarter", needs="A number, and an agreed place to read it"),
    origin="""
<p>Peter Drucker proposed management by objectives in 1954: agree what each person is trying to achieve, then judge them on that rather than on how busy they look. Andy Grove, running Intel in the 1970s, found Drucker's version too slow and too polite, and cut it down to two questions. Where do I want to go? That is the objective. How will I pace myself to see if I am getting there? Those are the key results. He described it in High Output Management in 1983.</p>
<p>John Doerr learned it as a young engineer at Intel, and in 1999 took it to a company of about forty people that had just taken his investment. Google has run on OKRs ever since. Doerr's 2018 book Measure What Matters made the method famous, and made it fashionable enough that most companies now do it badly.</p>
<p>The version Greggle offers is Grove's rather than the fashionable one: a single objective, two to five key results, each with a number and an agreed place to read it, and a review whose terms are set before the period starts.</p>""",
    works="""
<p>It separates the thing you want, which can be ambitious and even vague, from the numbers that would prove you got there, which can't be. Most goals fail because they were only ever the first half. "Get properly good at guitar" is a wish until something says what good looks like in June and where the number will be read.</p>
<p>The discipline is entirely in the key results. Each is scored from outside: if you could claim it by pointing at effort, it is an activity, and it belongs under initiatives instead. Initiatives are bets on the numbers, not promises of work. If one finishes and no number moves, it was the wrong bet, and it gets dropped without ceremony.</p>""",
    when="""
<p>Reach for it when you are aiming at something without a fixed end date and you want to know, in three months, whether you moved. A Goal, above all. It also suits a Project with a long horizon, where the milestones are too far apart to steer by.</p>
<p>It is the wrong tool for a decision or a diagnosis, and it is weak when the thing you want genuinely can't be counted. Even then, try: there is usually a number hiding behind "done or not done". Greggle suggests it on a Goal, last of five, because the four before it help you know what the goal is.</p>""",
    steps=[
        "Write the objective in one sentence with no numbers in it, in words you would want to repeat. Say why this period rather than any other, and how long the period is. A quarter, usually.",
        "Write two to five key results. Each is an outcome in the world, not work performed: someone on holiday all period could still score it.",
        "Give each a number: where it stands today and where it lands. Then name the report, app or person everyone agrees to believe for that number. Settled now, or renegotiated at review time.",
        "Mark each result committed or a stretch. All committed promises nothing bold; all stretch promises nothing at all. If a result is done-or-not-done, say what number it would move and why you can't measure that instead.",
        "List the initiatives, the work you believe will move the numbers. Each names the key result it is aimed at and roughly how far it should move it. Work aimed at everything is aimed at nothing.",
        "Set the review now: the date the numbers get read, what a seventy per cent period looks like, and who may drop an initiative mid-period when it isn't moving its number.",
    ],
    board_intro="Pick Objectives and Key Results on a Goal board and Greggle proposes four steps: the objective, the key results with three to start, the initiatives with three to start, and the review. Apply it again to a sibling step for the next objective rather than stretching one to hold everything.",
    board=[
        dict(label="1", name="The objective", text="One sentence, no numbers. Why this period, of all periods. The period it covers."),
        dict(label="2", name="The key results", text="Two to five. Each: what will be true; how it is scored; the number, from and to; where it is read; committed or a stretch."),
        dict(label="each result", name="Done or not done?", text="Usually an activity in disguise. If it genuinely is binary, say what number it would move and why not measure that."),
        dict(label="3", name="The initiatives", text="Two to ten bets. Each: the work, which key result it moves, how much movement you expect."),
        dict(label="4", name="The review", text="When the numbers get read. What a seventy per cent period looks like. What gets dropped mid-period, and who may drop it.", action=True),
        dict(label="not on the board", name="The second objective", text="Apply the framework again to a sibling step. One objective per board, on purpose."),
    ],
    checks=[
        "Key results have been written and not one has a number anywhere in it, so the period ends in adjectives.",
        "A result is done-or-not-done with no defence of why it can't be a number.",
        "Nothing says where its number is read, so it will be renegotiated at review time by whoever the number embarrasses least.",
        "Initiatives have been listed and the results they are supposed to move have not, which is a to-do list with a slogan on top.",
    ],
    example="""
<div class="card example">
  <span class="stated">a Goal &middot; get properly good at guitar this year</span>
  <div class="qa">
    <div><b>The objective</b><span>Be the guitarist the band relies on. Why now: the band has its first paid gig in July and two of the songs are currently beyond me. Period: April to the end of June.</span></div>
    <div><b>Key result 1</b><span>I can play all eight songs in the set through without stopping. A number moves: 3 of 8 today, 8 of 8 by 30 June. Read from: the phone recording of Thursday practice. Committed.</span></div>
    <div><b>Key result 2</b><span>Chord changes per minute on the hard progression in song six: 40 today, 80 by June. Read from: the metronome app's log. A stretch; 65 would be a good quarter.</span></div>
    <div><b>Key result 3</b><span>The band stops re-learning my parts on Thursdays. Done or not done? Defence: the number behind it is minutes of practice spent on my parts, roughly 25 a week today, under 5 by June. Measured instead from the practice recording. Committed.</span></div>
    <div><b>Initiatives</b><span>Twenty minutes every day before school, aimed at result 2, expected to take it to 70. One new song every fortnight, aimed at result 1, expected to cover five of eight. Record every practice, aimed at result 3, expected to halve the re-learning by May.</span></div>
    <div><b>The review</b><span>30 June, with the band, from the recordings. Seventy per cent looks like six songs clean and 65 changes a minute. If the fortnightly song isn't landing by mid-May, Sam may tell me to drop it and drill the two hard ones instead.</span></div>
  </div>
  <p class="dim">The first draft of result 3 was "the band trusts me", which nobody could score. Finding the number behind it took five minutes and turned a feeling into something the recording can answer.</p>
</div>""",
    falls="""
<p>Companies pile OKRs up until nobody reads them, then score them all green at the end of the period by arguing about what the words meant. One objective at a time is plenty for a person, and the agreed place to read each number is the defence against the argument.</p>
<p>The other failure is confusing initiatives with results. "Practise every day" is work, and doing it proves nothing about whether you got better. It belongs as a bet, aimed at a number, and if the number doesn't move the bet was wrong however faithfully it was kept.</p>""",
    pairs=[
        ("Working Backwards", "When the goal has an end date, walk back from it instead. The evidence list there is a set of key results."),
        ("Pre-mortem", "Greggle suggests it first on a Goal. Imagine the period failed, then set the key results that would have caught it."),
        ("Theory of Constraints", "If the numbers won't move whatever you do, the constraint is somewhere the initiatives aren't."),
    ],
    reading=[
        "Andrew S. Grove, High Output Management, 1983. The OKR chapter is short and better than anything written about it since.",
        "John Doerr, Measure What Matters, 2018, for the Google story and the case studies.",
        "Peter F. Drucker, The Practice of Management, 1954, where management by objectives begins.",
    ],
    try_="Say it is a Goal, open a step, choose Apply a framework and pick Objectives and Key Results. It asks for the objective without numbers, then the numbers.",
    cta="Say what you want. Then say what would prove it.",
))

METHODS.append(dict(
    slug="scenario-planning", name="Scenario Planning", kind="a Challenge or an Opportunity",
    desc="Where scenario planning came from, how Shell saw the 1973 oil shock coming, and how to build four worlds and the signposts that tell you which one is arriving.",
    lead="Pick the two uncertainties that matter most and are genuinely independent, build the four worlds they produce, then plant the signposts that tell you which one you are entering.",
    facts=dict(origin="Herman Kahn, RAND, 1950s; Pierre Wack, Shell, 1970s", best="a Challenge, an Opportunity, a Decision", takes="Two hours, then a date to revisit", needs="A decision, a horizon, and honesty about what is already settled"),
    origin="""
<p>Herman Kahn at the RAND Corporation in the 1950s, thinking through nuclear futures nobody wanted to imagine, gave the method its name and its reputation for saying the unsayable. Pierre Wack, running a small planning team at Shell in the early 1970s, gave it its purpose. Wack's team built scenarios in which the oil-producing countries organised, cut supply and pushed the price up several times over. When the embargo came in October 1973 and did exactly that, Shell's managers had already thought it through, and the company came out of the decade stronger than any rival.</p>
<p>Wack was clear that the point was not to predict. It was to change what the managers could imagine, so that when the world moved they recognised it. He wrote two articles for Harvard Business Review in 1985 that are still the best account. Peter Schwartz, who succeeded him at Shell, turned the method into a book, The Art of the Long View, in 1991.</p>
<p>The two-axes grid, four worlds from the two most decisive uncertainties, is the version Schwartz taught and the version Greggle uses.</p>""",
    works="""
<p>Forecasting picks one future and bets on it. Scenarios pick the two most uncertain and most decisive forces, cross them, and give you four futures to rehearse. You stop asking "what will happen" and start asking "what would I do if", which is a question you can actually answer now.</p>
<p>Two things make it work rather than just interesting. The axes have to be independent: if knowing how one lands tells you how the other does, the four worlds are really two, and the grid is decoration. And the signposts have to be planted: early, observable signs that one world is arriving rather than another. A scenario nobody can check against reality is a story.</p>""",
    when="""
<p>Reach for it when the right answer depends on things outside your control that could genuinely go either way within the time you care about. A Challenge whose outcome depends on how the world turns, an Opportunity whose value does, a Decision with a long horizon.</p>
<p>It is the wrong tool for a decision whose uncertainties are all inside your control; that is Options and Criteria or Force Field Analysis. And it is wasted on a horizon so short that nothing can diverge, or so long that the decision no longer exists. Greggle suggests it on a Challenge and an Opportunity.</p>""",
    steps=[
        "Name the decision the scenarios are for, the horizon, and what is effectively settled between now and then. The settled things hold in every world; they are the walls of the grid, not its axes.",
        "List the uncertainties: things that could genuinely land either way, with both ends named. Weigh each against the others: decisive, shapes the decision, or background.",
        "Promote exactly two to axes: the most decisive pair that are independent of each other. Ask the question out loud: would knowing how one lands tell you how the other does? If yes, keep the more decisive and find another.",
        "Cross the axes. Each corner is a world. Name each one, say which end of each axis it takes, and write the plausible route from today to it. All four get equal effort, including the one you find implausible.",
        "For each world, list what it makes true that isn't true today, and what you would do about it: now, or prepared now and done then.",
        "Plant signposts: early, observable signs that a world is arriving, each tied to a world by name and to a place you actually look. Then write the moves that are right in every world, the bets that back one world, and the date you will read the signposts next.",
    ],
    board_intro="Pick Scenario Planning on a Challenge or Opportunity board and Greggle proposes five steps: the decision and horizon, the uncertainties with three to start, four worlds each with two implications to start, the signposts, and what you would do now.",
    board=[
        dict(label="1", name="The decision and the horizon", text="What will be done differently. How far out. What is effectively settled and holds in every world."),
        dict(label="2", name="The uncertainties", text="Three to eight. Each: both ways it could land; decisive, shapes or background; an axis or not; and whether the other axis would predict it."),
        dict(label="3", name="The four worlds", text="Each corner: a name people will use, which end of each axis, how it comes about from today. Then implications, each with what you would do."),
        dict(label="4", name="The signposts", text="Three to twelve. Each: the sign, which world it points to, where you would see it."),
        dict(label="5", name="What you would do now", text="The moves right in every world. The bets, and which world each backs. When the signposts get read next.", action=True),
        dict(label="not on the board", name="The story", text="Wack's scenarios were narratives. The route-from-today field is where that lives here."),
    ],
    checks=[
        "Three or more uncertainties are each named as an axis. A grid has two.",
        "An axis has never been checked for independence from the other, or admits it is correlated and nothing replaces it.",
        "Worlds have been named and not one has a plausible route from today.",
        "Nothing has been written under the signposts, which is what separates scenario planning from science fiction.",
    ],
    example="""
<div class="card example">
  <span class="stated">a Decision &middot; whether to take the Saturday job at the garden centre for the year</span>
  <div class="qa">
    <div><b>The decision and horizon</b><span>Whether to say yes to eight hours every Saturday from October to next July. Settled: exams are in May whatever happens, the pay is fixed, and the garden centre wants an answer by the end of September.</span></div>
    <div><b>Uncertainties</b><span>Whether I make the first team, which plays Saturday mornings. Decisive. Whether this year's coursework load is as heavy as everyone says. Decisive. Whether the band gets gigs. Shapes it. Whether the garden centre stays open through winter. Background. Axes: first team and coursework. Would one predict the other? No, they can land in any combination.</span></div>
    <div><b>The four worlds</b><span>Full Saturdays: first team, heavy coursework. The job is impossible; I'd be quitting by November. Free and easy: no team, light coursework. The job is the best thing on offer. Pitch and pen: first team, light coursework. Sundays would work, Saturdays won't. Desk-bound: no team, heavy coursework. Saturday work is fine and Sunday is for the coursework.</span></div>
    <div><b>Implications</b><span>In Full Saturdays, what's true is I'd be letting the garden centre down mid-season; what I'd do is not take the job, or take it only with an agreed exit. In Free and easy, the money and the reference are real; I'd take it now.</span></div>
    <div><b>Signposts</b><span>The team sheet for the first October match, on the noticeboard, points to Pitch and pen or Full Saturdays. The coursework timetable published in September, on the school portal, points to Full Saturdays or Desk-bound. The band's first booking, in the group chat, shapes but doesn't decide.</span></div>
    <div><b>What I'd do now</b><span>Right in every world: ask the garden centre whether Sundays are possible, since that survives three worlds out of four. The bet: say yes to Saturdays now with an honest \"I may need to swap in October\", which backs Free and easy and Desk-bound. Read the signposts on 5 October.</span></div>
  </div>
  <p class="dim">The move that survives every world, asking about Sundays, is the cheapest output of the exercise and the one nobody would have thought of without building the corner they didn't expect.</p>
</div>""",
    falls="""
<p>Four futures becomes fourteen becomes none. Two axes, four boxes, that's the method, and the box you find implausible gets the same effort as the rest, because it is the one that teaches you most when it starts arriving anyway.</p>
<p>The other failure is scenarios that are never revisited. Without signposts and a date to read them, the four worlds become the office mural: admired, referred to, never checked. Wack's point was that the scenarios change what you can recognise, and you only recognise what you keep looking for.</p>""",
    pairs=[
        ("Pre-mortem", "When the causes of failure are outside your control, build the worlds instead of trying to prevent them."),
        ("Options and Criteria", "Judge the options in each world, not just one. An option that wins in three of four is a different thing from one that wins in one."),
        ("Stakeholder and Influence Map", "The signposts are often people. Who would know first that a world is arriving?"),
    ],
    reading=[
        "Pierre Wack, \"Scenarios: Uncharted Waters Ahead\" and \"Scenarios: Shooting the Rapids\", Harvard Business Review, September and November 1985.",
        "Peter Schwartz, The Art of the Long View, 1991. The two-axes method, step by step.",
        "Herman Kahn and Anthony Wiener, The Year 2000, 1967, for where the word came from.",
    ],
    try_="Say it is a Challenge or an Opportunity, open a step, choose Apply a framework and pick Scenario Planning. It asks for the decision and the horizon before any future.",
    cta="Build four futures. Then plant the signposts.",
))

METHODS.append(dict(
    slug="stakeholder-and-influence-map", name="Stakeholder and Influence Map", kind="a Project, a Challenge or an Opportunity",
    desc="Where stakeholder mapping came from, why influence and position are different questions, and how to map a room honestly: who decides, who can block it, and what each of them actually wants.",
    lead="Who decides, who can block it, what each of them actually wants, and what it would take to move them.",
    facts=dict(origin="Freeman, 1984; Mendelow, 1981", best="a Project, a Challenge, an Opportunity", takes="Half an hour", needs="Candour, and a name beside every blocker"),
    origin="""
<p>The word came into management through R. Edward Freeman's 1984 book Strategic Management: A Stakeholder Approach, which argued that a company answers to everyone who can affect it or is affected by it, not only to its owners. The picture came from Aubrey Mendelow, who in 1981 proposed placing each person on a grid of power against interest: who can affect this, and how much do they care. Keep the powerful and interested close, keep the powerful and uninterested satisfied, keep the rest informed.</p>
<p>Greggle's version keeps Mendelow's two axes but asks a sharper pair of questions. Not power in general but influence on this decision specifically. Not interest but where they stand today, from champion to opposed, honestly. And it insists on one thing the classic grid leaves out: the name of the person who is going to talk to each of them.</p>""",
    works="""
<p>Most things that fail with people fail because someone who could block it was never asked, or someone who cared was treated as if they didn't. Putting names on a grid makes those gaps visible before they cost you.</p>
<p>Influence and position are different questions, and keeping them separate is the whole point. Someone can be strongly supportive and unable to help you at all. Someone else can be neutral and hold the only yes that counts. And the person people actually listen to is frequently not the person above them, which is why the map asks who has each person's ear.</p>""",
    when="""
<p>Reach for it when the outcome isn't yours to control and depends on other people agreeing, or at least not objecting. A Challenge where someone has to say yes, an Opportunity that needs permission, a Project with more than two people in it.</p>
<p>It is the wrong tool for a decision that is only yours, and it is dangerous when it isn't candid. A map of what people said in the meeting is a map of the room you were hoping for. Greggle suggests it on a Project, a Challenge and an Opportunity.</p>""",
    steps=[
        "Write what has to be decided, precisely. \"Approve the hall for Thursdays after five\", not \"get everyone on board\". Name who formally decides, and by when, and what happens if it slips.",
        "List everyone with a say or a stake, one line each. Include the people who can't help you but can stop you, and the ones with no formal role who are listened to anyway.",
        "For each, say what part they play: decides, advises, implements, affected, or gatekeeper. Then what they actually want, which is often about something else entirely.",
        "Rate each person's influence on this decision specifically: high, medium or low. Then where they stand today, honestly: champion, supportive, neutral, sceptical or opposed. Somebody is opposed. If nobody is, look again.",
        "For each, write what would move them: the evidence, the concession or the reassurance. \"Nothing\" is a real answer and changes the plan. Note who has their ear.",
        "Put a name and a week beside everyone you need to move, opposed and sceptical first. Then decide the order of conversations, the one to have this week, and what you do if the key person says no.",
    ],
    board_intro="Pick Stakeholder and Influence Map on a Project, Challenge or Opportunity board and Greggle proposes the decision, the people with four to start, and the approach. Each person is a step with eight questions.",
    board=[
        dict(label="1", name="The decision", text="What has to be decided. Who formally decides. By when, and what happens if it slips."),
        dict(label="2", name="The people", text="Four to sixteen. Candid rather than diplomatic: this is for you, and it stays on your machine."),
        dict(label="each person", name="Who they are, and what part they play", text="What they actually want. Influence on this decision: high, medium, low. Where they stand today. What would move them. Who has their ear."),
        dict(label="each person", name="Who is going to talk to them", text="A name and a week. Required for anyone opposed or sceptical."),
        dict(label="3", name="The approach", text="The order of conversations. The conversation to have this week. What you do if the key one says no.", action=True),
        dict(label="not on the board", name="The grid", text="Mendelow drew it as four boxes. The influence and position fields are the two axes."),
    ],
    checks=[
        "Nobody on this map is opposed, which usually means it records what people said in the room rather than what they will do outside it.",
        "Someone is opposed, or sceptical, and nobody is going to talk to them.",
        "The person who decides this has a blank where what they want should be. Everything else is a way of getting to their yes.",
        "Everyone carries the same influence rating, so the map cannot say who to see first.",
    ],
    example="""
<div class="card example">
  <span class="stated">a Challenge &middot; get the band the school hall on Thursdays after five</span>
  <div class="qa">
    <div><b>The decision</b><span>Permission to use the hall from 5 to 6.30 on Thursdays this term. Formally decided by the deputy head who owns the room bookings. By the end of next week, or drama keeps the slot for the term.</span></div>
    <div><b>Deputy head</b><span>Decides. Wants: no complaints from site staff and nothing that looks like favouritism. Influence high. Stands: neutral. Would move them: the site manager saying it's fine, and a written plan for locking up. Has their ear: the head of music. Talking to them: me, week after next, once the others are done.</span></div>
    <div><b>Site manager</b><span>Gatekeeper. Wants: to go home at six. Influence high, can stop it outright. Stands: opposed, has said so. Would move them: someone else holding the keys and signing for them, so they can leave. Has their ear: the deputy head. Talking to them: Sam's dad, who knows him, this week.</span></div>
    <div><b>Head of music</b><span>Advises. Wants: a band that plays at the summer concert. Influence medium. Stands: champion. Would move them: nothing needed. Talking to them: me, this week, to ask them to raise it with the deputy.</span></div>
    <div><b>Drama club lead</b><span>Affected. Wants: their Thursday slot, which they use twice a term. Influence medium. Stands: sceptical. Would move them: first refusal on the two Thursdays they actually need. Talking to them: Sam, this week.</span></div>
    <div><b>The approach</b><span>Site manager first, because the deputy head will ask him before deciding anything. Then drama, so they arrive at the deputy as neutral rather than aggrieved. Then the head of music raises it. Then me. If the site manager says no to the keys idea: ask for 4 to 5.30 instead, before he leaves.</span></div>
  </div>
  <p class="dim">The person with the most influence turned out to be the one with no formal role, and what he actually wants has nothing to do with the band. Nobody would have found that by asking who is in charge.</p>
</div>""",
    falls="""
<p>People aren't fixed points. Positions shift after every conversation, and a map made once and never revisited describes a room that no longer exists. Revisit it after each conversation, and be careful what you write down about named people, even on your own machine.</p>
<p>The other failure is diplomacy. A map that records what people said rather than what they want, and that has nobody opposed on it, is comforting and useless. The candour is the method; the grid is just where you put it.</p>""",
    pairs=[
        ("Force Field Analysis", "When the restraints are people, this is how you find out what each of them actually wants."),
        ("Answer First", "Once you know what the decider wants, the case you put to them starts with the answer and the reason they care about."),
        ("Scenario Planning", "The signposts are often people. Who would know first?"),
    ],
    reading=[
        "R. Edward Freeman, Strategic Management: A Stakeholder Approach, 1984.",
        "Aubrey L. Mendelow, \"Environmental Scanning: The Impact of the Stakeholder Concept\", Proceedings of the International Conference on Information Systems, 1981. The power and interest grid.",
    ],
    try_="Say it is a Project, a Challenge or an Opportunity, open a step, choose Apply a framework and pick Stakeholder and Influence Map. It asks for the decision before any names.",
    cta="Map the room you actually have. Then decide who to talk to first.",
))

METHODS.append(dict(
    slug="strategic-challenge-map", name="Strategic Challenge Map", kind="a Challenge or a Project",
    desc="What the Strategic Challenge Map is, why every challenge needs evidence with a date, and how to run it: Greggle's own method for proposing a change into a complex organisation without losing a sceptical reader.",
    lead="Categorise the challenges, evidence each one with a date, judge what you can actually move, then say what would count as proof.",
    facts=dict(origin="Greggle's own synthesis", best="a Challenge, a Project", takes="A day, done properly", needs="Sources you can cite, with dates"),
    origin="""
<p>This one was not taken from a textbook. It was built for a particular situation: proposing a change into a large organisation, where the reader is a sceptic who has heard "this fixes everything" before and stopped believing it the second time. The method borrows the habits that survive that reader. Evidence with a date, because an undated citation ages silently and is worth nothing in a year. Challenges sorted into four categories, because a technical fix can't solve an organisational problem and mixing the categories hides that. And an honest verdict on each challenge: does what you are proposing remove it, reduce it, or not touch it?</p>
<p>"Does not touch it" is the answer that gives the method its credibility. A map on which everything is improved reads as a pitch. A map that says plainly what it leaves alone is believed on the things it claims.</p>
<p>The four categories are technological, regulatory, competitive and commercial, and organisational, which are the four ways organisations fail. The last step, naming the proof a sceptic would demand before they ask for it, is what separates a proposal from a pitch.</p>""",
    works="""
<p>Listing the challenges is easy and useless. Categorising them, attaching dated evidence to each, and then judging honestly which ones your proposal moves turns a worry list into an argument somebody can check. Half the challenges usually evaporate at the evidence step, which is the point of having one.</p>
<p>The ranking is by urgency and hard deadlines, not by how interesting a challenge is, and the proof metrics are volunteered rather than extracted. Stating the standard you will be judged against, before you are asked for it, is the single most persuasive thing a proposal can do.</p>""",
    when="""
<p>Reach for it when you are proposing something into an organisation, a school, a club, a council, a company, and the people who decide are sceptical, busy and have been burned before. A Challenge whose outcome depends on being believed, or a Project that has to be approved before it can start.</p>
<p>It is far too heavy for a personal decision, and it is the wrong tool when the challenge is inside you rather than in the organisation. Of the fourteen, it is the one most obviously built for work rather than for a kitchen table, and the worked example below scales it down deliberately. Greggle suggests it first on a Challenge, and on a Project.</p>""",
    steps=[
        "Write the strategic context in a paragraph: what the organisation has to keep running, what it is trying to change, and the pressure it is under while doing both. Then name what you must not position against: the people, systems and decisions that are off the table.",
        "Work four categories in turn: technological, regulatory, competitive and commercial, organisational. Under each, list the challenges, at least two, stated as things that are the case rather than things you dislike.",
        "For every challenge, cite the evidence that it is real and the date that evidence carries. A challenge with no citation is an opinion.",
        "For every challenge, say whether your proposal removes it, reduces it, or does not touch it, and justify the verdict mechanically: what changes that makes this stop being true. Then name the proof a sceptical expert would insist on.",
        "Rank the challenges by urgency, driven by deadlines and consequences. Everything critical means nothing is. For each, judge how well a lightweight intervention fits versus changing something at the core.",
        "Define the proof: the metrics that would satisfy the sceptic, each stated so two people would collect the same number, sorted by the kind of doubt it answers, with the artefact you would put in front of them.",
    ],
    board_intro="Pick Strategic Challenge Map on a Challenge board and Greggle proposes the context, four category steps with two challenges each to start, a ranking with three to start, and the definition of proof.",
    board=[
        dict(label="1", name="Strategic context", text="The clash between keeping things running and changing them, and the pressure from outside. What you must not position against."),
        dict(label="2", name="Categorised forensic analysis", text="Technological, regulatory, competitive and commercial, organisational. Two challenges each to start, up to eight."),
        dict(label="each challenge", name="The challenge, and the documented evidence", text="The date of that evidence. Remove, reduce, or does not touch it. Justification. Proof demanded."),
        dict(label="3", name="Ranking and prioritisation", text="Each ranked challenge: the strategic driver, urgency from critical to low, and how well a lightweight intervention fits."),
        dict(label="4", name="Definition of proof", text="Three to twelve metrics. Each: what kind of doubt it answers, and how it would be measured and shown.", action=True),
        dict(label="the rule", name="Say what you don't touch", text="A section where everything is improved reads as a pitch. One honest \"does not touch it\" buys belief for the rest."),
    ],
    checks=[
        "Challenges have been written and not one says when its evidence was true.",
        "Every challenge in a category is one you improve. A section without a \"does not touch it\" reads as a pitch rather than an analysis.",
        "A challenge is claimed as removed with no proof named. The strongest claim is the one that will be tested hardest.",
        "All the ranked challenges carry the same urgency, so the ranking cannot say what to do first.",
    ],
    example="""
<div class="card example">
  <span class="stated">a Challenge &middot; persuade the school to let the canteen take card payments</span>
  <div class="qa">
    <div><b>Context</b><span>The canteen has to feed 900 people in 40 minutes every day while the school is being told to go cashless by the council. The queue is the pressure. Not positioning against: the canteen staff, the existing till supplier, the bursar's decision last year to keep the catering contract.</span></div>
    <div><b>Technological</b><span>The tills are ten years old and have no card reader. Evidence: the supplier's end-of-support letter, March this year. The proposal removes this, by replacing the readers only, not the tills. Proof demanded: a trial reader on one till for a week, with the transaction log.</span></div>
    <div><b>Regulatory</b><span>Card data from under-16s falls under the school's data protection obligations. Evidence: the trust's data policy, updated January. The proposal reduces this but does not remove it: the reader handles card data, the school still holds account records. Proof: the reader supplier's compliance certificate and a one-page data flow the bursar can read.</span></div>
    <div><b>Competitive and commercial</b><span>The corner shop across the road takes cards and a third of year 11 go there. Evidence: the head of year's count in the spring term. The proposal reduces this. Proof: the canteen's daily takings for year 11 before and after the trial.</span></div>
    <div><b>Organisational</b><span>Two of the three canteen staff have never used a card reader and one is retiring in July. Evidence: the catering manager, when asked in April. The proposal does not touch this. Training is the caterer's job and saying so is more credible than pretending a reader trains people.</span></div>
    <div><b>Ranking</b><span>The council's cashless deadline next January: critical. The end-of-support letter: high. The corner shop: medium. Staff training: medium, and not ours.</span></div>
    <div><b>Proof</b><span>Queue time at 12.40, timed by a prefect with a stopwatch, before and during the trial (operational). Failed transactions per day from the reader log (data integrity). A signed one-page data flow the bursar has read (governance).</span></div>
  </div>
  <p class="dim">The organisational challenge is the one the proposal honestly doesn't touch, and saying so is what makes the bursar believe the other three. A version that claimed to solve training would have lost her at that line.</p>
</div>""",
    falls="""
<p>Without the evidence step it becomes a list of fears. With the evidence step but without dates, it becomes a list of things that were true once. The dates are the discipline, and they are the part people skip because finding them is tedious.</p>
<p>It is also heavy. Run in full on a small decision, it produces a document nobody asked for. The scaled-down version in the example above kept all four categories and all four verdicts and took an afternoon; the point is the honesty of the verdicts, not the length of the map.</p>""",
    pairs=[
        ("Stakeholder and Influence Map", "The sceptic you are writing for has a name. Find out what they actually want before you decide which proof to volunteer."),
        ("Answer First", "Once the map exists, the proposal itself should open with the answer and hang the categories beneath it."),
        ("First Principles", "When the challenges all rest on how things have always been done here, strip the assumptions before you evidence them."),
    ],
    reading=[
        "This method has no single source. The definition that runs the app is a data file, and it is the reference.",
        "Richard Rumelt, Good Strategy Bad Strategy, 2011. Not a source for this method, but the best book on diagnosing the challenge before proposing anything.",
    ],
    try_="Say it is a Challenge or a Project, open a step, choose Apply a framework and pick Strategic Challenge Map. It asks for the context and what you must not position against before any challenge.",
    cta="Evidence every challenge. Then say which ones you don't touch.",
))

METHODS.append(dict(
    slug="theory-of-constraints", name="Theory of Constraints", kind="a Project or a Problem",
    desc="Where the Theory of Constraints came from, why an hour saved anywhere but the bottleneck is usually nothing, and how to run the five focusing steps: Eliyahu Goldratt's method for a system that produces less than it should.",
    lead="Find the one place the whole flow narrows, squeeze it before you spend on it, make everything else serve it, then follow it to wherever it moves next.",
    facts=dict(origin="Eliyahu Goldratt, 1984", best="a Project, a Problem", takes="An hour to find it, weeks to serve it", needs="A flow, and the queues along it"),
    origin="""
<p>Eliyahu Goldratt was an Israeli physicist who wrote his management theory as a novel. The Goal, published in 1984, follows a plant manager with three months to save his factory, who learns from an old physics teacher that a system's output is limited by its one narrowest point, and that improving anything else is wasted effort. The book sold millions of copies to people who would never have read a textbook, which was the idea.</p>
<p>The method is the five focusing steps. Identify the constraint. Exploit it: get everything out of it with what is already there. Subordinate everything else to it, so it never waits and never drowns. Elevate it: only now, spend money on more capacity. Then go back to step one, because the constraint has moved. Goldratt spent the rest of his life applying the same idea to projects, in Critical Chain in 1997, and to supply chains.</p>
<p>Greggle's description of it points out something the other thirteen methods can't claim: the Theory of Constraints is the only one whose own definition tells you to recurse, and a tool where every step is a board of its own is shaped exactly for that.</p>""",
    works="""
<p>Effort spread evenly across a process improves nothing that matters, because every step except one has slack, whether it admits it or not. Effort at the one narrow point improves everything downstream of it. This is unintuitive, which is why it is worth a whole method: an hour lost at the constraint is lost to the whole system, and an hour saved anywhere else is usually nothing.</p>
<p>Queues are the evidence. Work piling up in front of a step and idle hands after it is what a constraint looks like. A step that merely feels busy is not it. And the constraint is a fact about the flow, not a vote: if two places look equally narrow, trace the flow again until one of them isn't.</p>""",
    when="""
<p>Reach for it when you are busy and nothing gets finished, when work visibly piles up in one place while people further along wait, or when a project is late and adding effort hasn't helped. A Problem of throughput, or a Project whose flow has a narrow point.</p>
<p>It is the wrong tool for a problem with a single cause that isn't about flow; that is 5 Whys. And it needs a system: a set of steps that work passes through. A goal without a flow has no constraint to find. Greggle suggests it on a Project and on a Problem.</p>""",
    steps=[
        "Describe the system: what it exists to get through, the stages the work passes through in order, and the number that goes up when more gets through.",
        "Name the places the flow might narrow. For each, look for the evidence: what piles up in front of it, and who or what sits idle after it. Commit to one. A wrong constraint worked properly teaches you more than a right one never committed to.",
        "Exploit it. List the moves that recover capacity the constraint already has, without spending anything: stop it doing work that isn't its job, stop feeding it broken input, stop letting it sit idle at handovers.",
        "Subordinate everything else. Decide what changes away from the constraint so that it never waits and never drowns, and say whose numbers get worse on purpose. If nobody's do, nothing has been subordinated. Tell them yourself.",
        "Only if squeezing wasn't enough, elevate: spend on more capacity at the constraint specifically. An empty elevate step is a result, not a gap.",
        "Ask where the constraint stands now. If it has moved, name the step it moved to, note which rules from this round must not become policy, and start again from the top on the new one.",
    ],
    board_intro="Pick Theory of Constraints on a Project or Problem board and Greggle proposes six steps: the system, the candidates with two to start, exploit, subordinate, elevate, and whether the constraint has moved. When it has, open the step it moved to and apply the framework again.",
    board=[
        dict(label="1", name="The system and its goal", text="What it exists to get through. How the work flows, start to end. How you would measure what gets through."),
        dict(label="2", name="Find the constraint", text="Two to six candidates. Each: the signs of queueing, and a verdict: the constraint, a contributor, or examined and cleared."),
        dict(label="3", name="Exploit: squeeze it first", text="Two to eight moves, each recovering capacity the constraint already has. Free, or it belongs in step 5."),
        dict(label="4", name="Subordinate everything else", text="What changes away from the constraint. Whose numbers get worse. Agreed with them, not yet raised, or raised and resisted."),
        dict(label="5", name="Elevate, if squeezing was not enough", text="Investment at the constraint specifically. Honestly empty if step 3 was enough.", action=True),
        dict(label="6", name="Has the constraint moved?", text="Moved, still here, or too early to tell. Where it lives now. What from this round must not become policy."),
    ],
    checks=[
        "Several candidates are each named as the constraint. The method insists there is one.",
        "A candidate is named the constraint on no evidence of queueing, and the whole system is about to be bent around a suspicion.",
        "Investment is listed and the squeezing step is empty, which is spending money before using what you already have.",
        "The constraint is being squeezed and nothing elsewhere changes to serve it, or nothing says whose numbers get worse.",
    ],
    example="""
<div class="card example">
  <span class="stated">a Problem &middot; the band's set never gets finished</span>
  <div class="qa">
    <div><b>The system</b><span>It exists to get songs from chosen to performable. Flow: pick a song, each person learns their part at home, rehearse it together on Thursdays, run it clean twice, it's in the set. Measure: songs in the set.</span></div>
    <div><b>Candidates</b><span>Learning parts at home: nothing piles up in front of it and it finishes early. Cleared. Thursday rehearsal: six songs learned by everyone and waiting, and the two songs that reach it get through in a week. Queue in front, nothing waiting after. The constraint. The singer's lyrics: slows two songs, but songs without lyrics still wait for Thursday. A contributor.</span></div>
    <div><b>Exploit</b><span>Start at five, not twenty past, which recovers twenty minutes a week. Free. Only rehearse songs everyone has learned, instead of teaching the drummer his part in the room. Free. Record every run so next week doesn't start from scratch. Free. Stop rehearsing songs already clean. Free.</span></div>
    <div><b>Subordinate</b><span>The guitarists stop learning new songs ahead and drill the queued ones instead, so Thursday never gets a song only half the band knows. Whose numbers get worse: theirs, they like learning new songs. Raised, and resisted, then agreed when the queue was pointed at.</span></div>
    <div><b>Elevate</b><span>Empty, for now. If four free moves don't clear the queue by half term, a second practice on Sundays, which costs everyone's Sunday.</span></div>
    <div><b>Has it moved?</b><span>Too early to tell. Check at half term. If it moves to lyrics, apply this again to the singer's step. Rule not to keep: \"no new songs\" was made to serve Thursday, and if Thursday clears it becomes the next constraint itself.</span></div>
  </div>
  <p class="dim">The instinct was to practise more at home. Home practice was never the constraint, so more of it would have lengthened the queue in front of Thursday and finished nothing.</p>
</div>""",
    falls="""
<p>People find a constraint and then try to fix three things at once, or name three constraints and spread the effort across all of them, which is the same failure. One at a time, or it isn't the method.</p>
<p>Subordination is where it quietly fails in practice. Somebody's local efficiency has to get worse on purpose, and they will resist, reasonably, unless they hear why from you. A constraint exploited while the rest of the system carries on at its own pace is exploited on paper. And the rules made to serve one constraint, left standing after it moves, become the next constraint themselves.</p>""",
    pairs=[
        ("5 Whys", "When the fifth why is \"because there is never enough time\", this is the method that says where the time goes."),
        ("Working Backwards", "A late project is a flow. Find where it narrows before adding milestones."),
        ("Force Field Analysis", "Subordination means asking people to run below their best. The restraints on that are people, and this maps them."),
    ],
    reading=[
        "Eliyahu M. Goldratt and Jeff Cox, The Goal, 1984. A novel, and still the best introduction.",
        "Eliyahu M. Goldratt, Critical Chain, 1997, for the same idea applied to projects.",
    ],
    try_="Say it is a Project or a Problem, open a step, choose Apply a framework and pick Theory of Constraints. When the constraint moves, open the step it moved to and pick it again.",
    cta="Find where it narrows. Serve that, and nothing else.",
))

METHODS.append(dict(
    slug="answer-first", name="Answer First", kind="a Challenge or a Decision",
    desc="Where answer-first writing came from, why the reader decides in the first minute, and how to structure a case: Barbara Minto's pyramid, for anyone who has to persuade someone who may stop reading.",
    lead="Give the answer in the first sentence, then group the reasons beneath it, parallel reasons or a chain, never both at once, with the evidence at the leaves.",
    facts=dict(origin="Barbara Minto, 1970s", best="a Challenge, a Decision, at the end", takes="An hour to get it into one sentence", needs="An answer, and a reader who might stop early"),
    origin="""
<p>Barbara Minto again. The Pyramid Principle's second rule, after MECE, is that the answer goes at the top and the reasons hang beneath it, because a reader who knows the conclusion can judge the reasons, while a reader waiting for the conclusion can't judge anything. She worked it out teaching McKinsey consultants to write in the late 1960s and published it in 1978, and it has been the house style of the consulting trade ever since.</p>
<p>The idea is older. Newspapers have written this way since the telegraph, when a story might be cut off at any line and had to survive it: the inverted pyramid. The military calls the same thing BLUF, bottom line up front. Minto's contribution was the structure beneath the answer: a small number of groups, each asserting one claim, each argued one way, with the evidence at the leaves.</p>
<p>Greggle describes it as the presenting counterpart to the issue tree. One is how you work the answer out; this is how you deliver it.</p>""",
    works="""
<p>Writing the answer first exposes whether you have one. Most rambling explanations are rambling because the writer hasn't decided, and putting the decision in the first sentence makes that impossible to hide. If it needs two sentences, it is two answers, and the work upstream isn't finished.</p>
<p>The rest is built for the reader who may stop at any line. The first sentence alone gives the answer. The three claims alone give the case. The full depth gives the proof. And each group argues one way: parallel reasons survive reordering and the loss of one; a chain survives neither; mixed together, the reader can rely on nothing.</p>""",
    when="""
<p>Reach for it at the end of anything: a Decision made that now has to be explained to someone, a Challenge where someone else has to be persuaded, a Problem diagnosed that someone else has to act on. It is the method for the last step, once the thinking is done.</p>
<p>It is the wrong tool when you don't yet have an answer; that is what the issue tree is for, and Greggle's own rule is to go back to the tree if the answer won't fit in one sentence. Greggle suggests it on a Challenge and on a Decision, last in both lists.</p>""",
    steps=[
        "Write who this is for, what they already believe, and what they will do with the answer. Then write the question they are asking, in their words. Answering a better question than the one asked reads as evasion.",
        "Write the answer in one sentence. The whole recommendation, as the first thing they read. If it won't go in one sentence, go back to the thinking.",
        "Write three groups beneath it, each asserting one claim in a sentence that directly holds the answer up. Order them by strength. Two groups is usually a debate; four is usually a list.",
        "Fill each group with two to five supports that argue alike: all parallel reasons, or all steps in a chain. Never both in one group. Put the evidence, the fact or figure or source, behind each support.",
        "Test each support: if this fell, would the claim still stand? If yes, it is colour, not support, and it moves to an appendix or goes.",
        "Read it as the reader will. Write the thirty-second version: the answer, the three claims, nothing else. Then write the strongest objection and say which group answers it. If none does, you are missing a group.",
    ],
    board_intro="Pick Answer First on a Challenge or Decision board and Greggle proposes the answer, three groups each with two supports to start, and the read-through. Each group takes up to five supports.",
    board=[
        dict(label="1", name="The answer, first", text="Who this is for. The question they are asking. The answer, in one sentence."),
        dict(label="2", name="The groups that hold it up", text="Three. Each asserts one claim in a sentence, argued one way, ordered by strength."),
        dict(label="each support", name="The point, and how it argues", text="A parallel reason, or a step in a chain. The evidence behind it. If this fell, would the claim still stand?"),
        dict(label="3", name="The read-through", text="The thirty-second version: the answer, the three claims, nothing else. The strongest objection, and which group answers it.", action=True),
        dict(label="the rule", name="Every level survives being the last one read", text="The first sentence alone, the answer. The claims alone, the case. The full depth, the proof."),
        dict(label="not on the board", name="The prose", text="The board is the skeleton. The document, the email or the two minutes at the kitchen table is written from it afterwards."),
    ],
    checks=[
        "A group mixes parallel reasons with steps in a chain, so the reader cannot tell what it survives and trusts none of it.",
        "A group's supports are all assertion, with no evidence behind any of them.",
        "By your own account, the claim would survive losing every member of a group, which means the group is standing near it, not holding it up.",
    ],
    example="""
<div class="card example">
  <span class="stated">a Decision, explained &middot; telling my parents I want History instead of Chemistry</span>
  <div class="qa">
    <div><b>Who it's for</b><span>My parents, who think Chemistry is the serious choice and will be paying for whatever comes after. The question they're asking: will this close doors?</span></div>
    <div><b>The answer</b><span>Taking History instead of Chemistry keeps both the courses I'm considering open and gives me a subject I'll actually work at for two years.</span></div>
    <div><b>Group 1</b><span>It closes no doors. Parallel reasons: course A's entry requirements ask for Physics and Maths, not Chemistry (their website, printed). Course B asks for Maths and any science (same). The head of sixth form confirmed both on Tuesday (her email). Each stands alone; losing one, the claim holds.</span></div>
    <div><b>Group 2</b><span>I'll get better grades. A chain: I do the History homework first, unasked (this year's planner); so my History marks are two grades above my Chemistry marks (the spring report); the sixth form predicts grades from year 12 work (the options booklet); and predicted grades are what the applications see. Each step rests on the one before.</span></div>
    <div><b>Group 3</b><span>Chemistry costs more than it gives. Parallel: it's the class I've been asked to see the teacher about twice (their emails). It's the only subject I'd be taking because it looks serious rather than because I want it (me, honestly). Test: if this group fell, the answer would still stand on groups 1 and 2, so it goes last.</span></div>
    <div><b>Thirty seconds</b><span>History instead of Chemistry keeps both courses open. It closes no doors. I'll get better grades in it. And Chemistry is costing me more than it gives.</span></div>
    <div><b>Strongest objection</b><span>\"What if you change your mind about the course?\" Group 1 answers it: Physics keeps the science doors open on its own. If it didn't, I'd need a fourth group.</span></div>
  </div>
  <p class="dim">The first draft opened with the reasons and got to the answer in paragraph three, which is how these conversations usually go and why they usually go badly. The parents can stop after the first sentence and still know what is being asked.</p>
</div>""",
    falls="""
<p>Answer first with nothing beneath it is an assertion, and a confident one is worse than a hesitant one. The pyramid has to have a base, and the base has to be evidence a sceptical reader could check, not more assertions in smaller type.</p>
<p>The other failure is the group that isn't load-bearing: true, relevant-sounding, and unnecessary. If the claim would survive losing every support in the group, the group is decoration, and the reader will notice before you do. Three groups is the discipline because it forces you to choose.</p>""",
    pairs=[
        ("Issue Tree", "The same method from the other end. Build the tree to find the answer, then turn it upside down to deliver it."),
        ("Options and Criteria", "Once chosen, the comparison is the evidence at the leaves. The answer goes at the top."),
        ("Stakeholder and Influence Map", "Who this is for is the first field. Find out what they actually want before you write the sentence."),
    ],
    reading=[
        "Barbara Minto, The Pyramid Principle, 1978; current edition The Minto Pyramid Principle, 2009. The first half is this method.",
        "Any newspaper style guide on the inverted pyramid, which is the same idea a century earlier.",
    ],
    try_="Say it is a Challenge or a Decision, open a step, choose Apply a framework and pick Answer First. It asks who the reader is before it asks for the answer.",
    cta="Say the answer in one sentence. Then hold it up.",
))

for m in METHODS:
    m["try"] = m.pop("try_")

write_index()
for m in METHODS:
    write_method(m)

# ---------------------------------------------------------------------------
def write_page(slug, title, desc, current, body):
    out = head(title, desc, f"https://greggle.app/{slug}/", current=current) + body + FOOT
    d = os.path.join(ROOT, slug); os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w") as f:
        f.write(out)

ESSAY = """
  <article class="essay">
    <header class="method-head">
      <p class="crumbs"><a href="/">Greggle</a> &middot; Why</p>
      <span class="eyebrow">The idea behind it</span>
      <h1>Why methods, and not answers.</h1>
      <p class="dim lead">Every one of the fourteen ways of thinking is a set of questions, and only the person asking can answer them. That is the whole design, and it is the opposite of where most software is going.</p>
    </header>
    <div class="prose">
      <section id="questions">
        <h2>The answer is already in the room</h2>
        <p>Nobody else knows why your band misses practice. No search engine knows what a good answer to your subject choice would have to do. Toyota's fifth why has to come out of the head of the person who was standing at the machine, and Shell's scenarios were only useful because the people who had to act on them had built them. Every method on this site works the same way. It doesn't supply content. It supplies the shape that gets the content out of you.</p>
        <p>That is why the methods are old, and why none of them were invented here. A method that has been used on factory floors and in boardrooms for fifty years has had every shortcut tried and every lazy version found out. What survives is a short list of questions in a particular order, and the order is usually the whole thing. Write the criteria before the options. State the failure as a fact before you list the causes. Ask why of the answer, not of the problem. Get the order wrong and the method quietly becomes a way of justifying what you already thought.</p>
        <p class="pull">A method is a set of questions in an order that stops you lying to yourself. The answers were always yours.</p>
      </section>
      <section id="opposite">
        <h2>The opposite direction</h2>
        <p>The default now is to ask a machine for the answer. That works well when the answer exists outside you: a date, a formula, how to fix a fence post. It works badly, and sometimes harmfully, when it doesn't. A plan for your own life written by something that has never met you is a plausible-sounding plan for someone else. It will be fluent, tidy, and wrong in ways you can't see, because the wrongness is in the assumptions it made about you, and you never got to look at those.</p>
        <p>Greggle takes a side here, and the side shows in how it's built. Pick a method and it proposes a cut of your board, and then it adds nothing until you have looked at every step and ticked or unticked it. It shows the counts, three of eleven, rather than a percentage, because a percentage flatters a plan and a count doesn't. And it holds nothing on a server, because there isn't one. Those aren't privacy features bolted on afterwards. They are what a tool looks like when it believes the knowledge is in the user.</p>
      </section>
      <section id="assistant">
        <h2>What about an assistant?</h2>
        <p>Honest answer: the app is built so that one could be added later, and there isn't one in this version. There is no network code in it at all, and no place to put a key. But the boundary an assistant would sit behind already exists, and it says a lot about what an assistant would be for. It would be asked the same two questions the method library is asked today: propose a cut of this step, and read this branch back and say what is missing. Its suggestions would arrive on the same review screen a method's do, one at a time, to accept, edit or reject. And the settings screen already shows, word for word, what it would be told about a step, so you could read that before every call instead of trusting a promise.</p>
        <p>That is a different job from writing your answer. It's the job of a good colleague who asks "what would have to be true?" and then shuts up. If an assistant is ever switched on, that's the job it gets.</p>
      </section>
      <section id="next">
        <h2>Where this goes</h2>
        <p>If the belief is that the knowledge is in the person, the app is one expression of it and not the only one. The wider thing is a set of tools, methods and systems for people who want to solve problems, finish things and plan what they're going to do, using what they already know. Some of the directions, roughly in the order they're likely to happen.</p>
        <p><b>The library.</b> This site is the first extension. A page that lets someone run a pre-mortem on paper, with no app at all, is already a tool. <a href="/methods/">The fourteen are here.</a></p>
        <p><b>Cards.</b> Each method as a single printable page: the steps, the questions, a blank grid where one is needed. Pen and paper is the most offline the work can get, and a card on a kitchen table is how a method gets used by a family rather than by whoever owns the laptop.</p>
        <p><b>More kinds of thing.</b> Seven kinds is a good start and the gaps are obvious: a habit to build or break, a skill to learn, a conversation you're dreading, a piece of writing. Each brings its own questions and its own natural methods, and none of those were invented here either. Gabriele Oettingen's WOOP for a habit. Chris Argyris's ladder of inference for a conversation.</p>
        <p><b>The knowledge audit.</b> Every method assumes you know things, and most people have never been asked to write down what they know about their own situation. A method for that, run before any other: what do I know for certain, what do I believe, what am I assuming, what would I need to find out and from whom. Donna Ogle's KWL chart from 1986 is the classroom version. This is the method that would feed all the others, and it's the one that most sharply separates a tool built on the user's knowledge from one built on retrieval.</p>
        <p><b>The review loop.</b> Greggle can already read a board back and say what's missing. The next thing to read back is the past. A decision journal records what you decided, what you expected and how sure you were, and then, months later, what actually happened. Over a year it teaches a person where their own judgement is reliable and where it isn't, which is knowledge nobody else can give them. Finished boards are the raw material. It stays on the device like everything else.</p>
        <p><b>Fading.</b> The most interesting version of the tool is one that plans its own obsolescence. The first time someone runs a pre-mortem, the app walks them through every question. The fifth time, it offers the board and stays quiet. By the tenth, they run it in their head in a meeting and don't open anything. Teachers call this cognitive apprenticeship: model, coach, then fade the scaffolding. A tool that measured its success by how little people needed it would be unusual. It's also exactly what a tool built on the user's own knowledge ought to want.</p>
      </section>
      <section id="rules">
        <h2>The rule</h2>
        <p>The thread through all of these is the rule the app already follows. If a proposed feature breaks one of these, it belongs to a different product.</p>
        <div class="rules">
          <div class="tile"><b>Elicit, don't generate</b><span>Ask the question. The person answers it.</span></div>
          <div class="tile"><b>Show the count, not the score</b><span>Three of eleven. A percentage flatters.</span></div>
          <div class="tile"><b>Add nothing unreviewed</b><span>Every proposal is looked at, step by step, before it lands.</span></div>
          <div class="tile"><b>Keep the work where the person is</b><span>On the device, in a file they own.</span></div>
        </div>
      </section>
    </div>
    <section class="method-cta">
      <div class="card">
        <h2>Pick a method. The answers are yours.</h2>
        <p class="dim">Fourteen ways of thinking, each with where it came from and how to run it on paper.</p>
        <a class="btn" href="/methods/">See the fourteen</a>
      </div>
    </section>
  </article>
"""

ABOUT = """
  <article class="essay">
    <header class="method-head">
      <p class="crumbs"><a href="/">Greggle</a> &middot; About</p>
      <span class="eyebrow">About</span>
      <h1>What Greggle is, who made it, and what it promises.</h1>
      <p class="dim lead">A free tool for breaking a big thing into pieces small enough to just do, built by one person, with nothing to sign up for.</p>
    </header>
    <div class="prose">
      <section id="what">
        <h2>What it is</h2>
        <p>Greggle is a web app. You name something you are working on, say what kind of thing it is, and it gives you a board of interlocking steps. Open any step and it becomes a board of its own. Keep going until every piece is something you can actually go and do, mark those as actions, and they collect in one flat list. Along the way it offers <a href="/methods/">fourteen ways of thinking</a>, each of which proposes a cut of your board that you review before anything is added, and a check that reads a branch back and says what is missing.</p>
        <p>It runs in the browser and can be installed like any other app on a phone or a computer. Once installed it works with no internet connection at all. The ideas behind it are on <a href="/why/">the why page</a>.</p>
      </section>
      <section id="who">
        <h2>Who made it</h2>
        <p>Stuart Muir. Greggle is a one-person project, and the person is reachable: <a href="mailto:feedback@greggle.app">feedback@greggle.app</a> goes to him. If a method is wrong on this site, if a page is unclear, or if the app does something it shouldn't, that is the address. The app has a feedback section in its settings as well.</p>
      </section>
      <section id="promise">
        <h2>The promise, and what enforces it</h2>
        <p>Nothing you write leaves your device. That claim is made by a lot of software and usually means "we intend not to send it anywhere". Greggle's version is enforced by your browser rather than intended by the author. The app's security policy forbids outbound connections outright, so the page cannot fetch, post or send a beacon anywhere, including back to its own server. It loads no fonts, scripts, images or trackers from anywhere. An automated test asserts that the app makes no request to any other origin, and another asserts that the policy is present every time it is built.</p>
        <p>There is no account because there is no server to hold one, and no analytics because nothing could send them. Your work lives in your browser and, if you choose, in a file you own. Putting that file in a cloud folder is how the same work reaches your other devices; choosing and writing a file is a conversation between the page and your own computer, not a connection to anywhere. It also means nothing is backed up for you, which the app says plainly rather than hiding.</p>
        <div class="card facts">
          <div><span class="stated">Account</span><p>None. Nothing to sign up for.</p></div>
          <div><span class="stated">Network</span><p>Blocked by policy, and tested.</p></div>
          <div><span class="stated">Your work</span><p>In your browser, and a file you own.</p></div>
          <div><span class="stated">Price</span><p>Free.</p></div>
        </div>
      </section>
      <section id="not">
        <h2>What it is not</h2>
        <p>It is not open source. The app's source is private and the product is commercial, even though the app is free to use. The methods it offers are not Greggle's to own, and this site says where each one came from. One of them is described in the app under a plain name rather than the one it is famous by, because that name is a registered trademark for software; the method underneath is the same and belongs to nobody.</p>
        <p>There is no assistant in this version. The app is built so that one could be added later, behind a boundary that would show you exactly what it was told before every call, and the settings screen already lets you read that. Today the honest description is: no network code, and no place to put a key.</p>
      </section>
      <section id="site">
        <h2>About this website</h2>
        <p>The site is plain static pages with no scripts and no analytics. The one thing it fetches from elsewhere is the typeface, from Google Fonts, and it falls back to a system font if that fails. The board on the front page is a real board from the app. The method pages were checked against the definitions that actually run in the app, and the further reading on each page is the primary source where one exists.</p>
        <p>Copyright Stuart Muir. The site is published so that people can read it, not so that it can be reused: please don't redistribute its text or host a copy without asking. Asking is easy; the address is above.</p>
      </section>
    </div>
    <section class="method-cta">
      <div class="card">
        <h2>Start with the thing you have been putting off.</h2>
        <p class="dim">Free, no account, works offline. Your work stays on your device.</p>
        <a class="btn" href="https://www.greggle.app/">Open Greggle</a>
      </div>
    </section>
  </article>
"""

write_page("why", "Why methods, and not answers", "The idea behind Greggle: every method is a set of questions only the person asking can answer, and where a tool built on that belief could go next.", "why", curly(ESSAY))
write_page("about", "About Greggle", "What Greggle is, who made it, what it promises about your work and how that promise is enforced.", "about", curly(ABOUT))

print("wrote", len(METHODS) + 3, "pages")
