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
        (None, "Strategic Challenge Map", "after Richard Rumelt", "Categorise the challenges, evidence each one, judge what you can move."),
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
      <span class="stated">Which to reach for, by the kind of thing you are working on</span>
      <div class="kinds-row"><b>a Goal</b><span>Objectives and Key Results, Working Backwards, Force Field Analysis when it has stalled</span></div>
      <div class="kinds-row"><b>a Project</b><span>Working Backwards, Issue Tree, then a Pre-mortem before you start</span></div>
      <div class="kinds-row"><b>a Challenge</b><span>Strategic Challenge Map, First Principles, Stakeholder and Influence Map</span></div>
      <div class="kinds-row"><b>a Problem</b><span>5 Whys when it feels deep, Cause and Effect when it feels wide, Theory of Constraints when nothing gets finished</span></div>
      <div class="kinds-row"><b>a Decision</b><span>Options and Criteria, Force Field Analysis, Scenario Planning when the answer depends on the future</span></div>
      <div class="kinds-row"><b>an Opportunity</b><span>Working Backwards, Options and Criteria, Scenario Planning</span></div>
      <div class="kinds-row"><b>a Risk</b><span>Pre-mortem, Scenario Planning, 5 Whys if it has happened before</span></div>
      <div class="kinds-row"><b>any of them, at the end</b><span>Answer First, to say what you decided in one sentence</span></div>
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
<p>Don't use it on something that hasn't happened yet, and don't use it on a problem that feels wide rather than deep. If you can already think of four unrelated reasons, you have several chains, not one, and the fishbone is the better start. On a Greggle board, 5 Whys is offered on a Problem.</p>""",
    steps=[
        "Write the problem as one observed fact. Not \"the band is flaky\" but \"we have missed four of the last six practices\".",
        "Ask why it happened. Write one answer, a fact you could check, not a judgement.",
        "Ask why of that answer. Write the next answer beneath it.",
        "Keep going. Whenever the answer is a person's mistake, ask why the mistake was possible, or why it mattered.",
        "Stop when you reach something you could change tomorrow. Five is a guide, not a rule. Three is often enough and seven is sometimes needed.",
        "Write the change as an action. Then check it backwards: if that had been in place, would the chain have broken?",
    ],
    board_intro="Pick 5 Whys on a Problem board and Greggle proposes a chain of steps like this, each one holding the last answer and the next question. You edit every one before it lands.",
    board=[
        dict(label="the problem", name="What happened, as a fact", text="One sentence, one observed event, no blame in it."),
        dict(label="why 1", name="Why did that happen?", text="The first cause. Usually true, usually not the one that matters."),
        dict(label="why 2", name="Why did that happen?", text="Ask why of the answer above, not of the original problem."),
        dict(label="why 3", name="Why did that happen?", text="If the answer is a person's mistake, ask why it was possible."),
        dict(label="why 4 and 5", name="Keep going until it stops", text="Something you could change tomorrow. Stop there."),
        dict(label="action", name="The fix that breaks the chain", text="Marked as an action, so it lands in your list.", action=True),
    ],
    example="""
<div class="card example">
  <span class="stated">a Problem &middot; the band keeps missing practice</span>
  <div class="qa">
    <div><b>The problem</b><span>We have missed four of the last six Thursday practices.</span></div>
    <div><b>Why?</b><span>Two people didn't turn up each time, and you can't practise without a drummer.</span></div>
    <div><b>Why?</b><span>They said they didn't know it was on.</span></div>
    <div><b>Why?</b><span>Practice is arranged in the group chat on the day, and they mute the group chat.</span></div>
    <div><b>Why?</b><span>The group chat has forty messages a day and most of them aren't about the band.</span></div>
    <div><b>Why?</b><span>Because it is also the friends chat. There is no separate place where band things live.</span></div>
    <div><b>The action</b><span>Fix a standing time, Thursdays at 5, and make a chat that only has practice in it. Nobody needs to be reminded of a standing time.</span></div>
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
    try_="Say what kind of thing it is (a Problem), then pick 5 Whys. Greggle proposes the chain and you fill it in.",
    cta="Start with the thing that keeps going wrong.",
))

METHODS.append(dict(
    slug="working-backwards", name="Working Backwards", kind="a Project",
    desc="Where Working Backwards came from, why it works, and how to run it: Amazon's way of defining done before you start, then walking back to now.",
    lead="Define what done looks like and the evidence that would prove it, then walk back to now.",
    facts=dict(origin="Amazon, early 2000s", best="a Project, a Goal, an Opportunity", takes="An hour, then revisits", needs="Honesty about what done is"),
    origin="""
<p>Amazon, in the years around 2004. Before a team could build a new product, they had to write the press release announcing it as if it had already shipped, and then the list of questions a sceptical customer or journalist would ask about it. The document was usually six pages. If the press release wasn't something a customer would want to read, the product wasn't built, and if the questions couldn't be answered, the team went away and worked out how.</p>
<p>The Kindle was developed this way, and so were most of the products Amazon launched over the following fifteen years. Colin Bryar and Bill Carr, who ran the process from the inside, wrote it up in a 2021 book of the same name. Inside Amazon the document is still called the PR/FAQ.</p>
<p>The idea is older than Amazon. Any good engineer designs from the requirement back, and any good cook reads the recipe from the plate. What Amazon added was the rule that you write the ending first, in the customer's words, before anyone is allowed to fall in love with a way of getting there.</p>""",
    works="""
<p>Most plans fail before they start, because "done" was never defined. People begin with the first step because it is the one they can see, and by the time they look up they have built a great deal of something that turns out not to be the thing.</p>
<p>Starting from the finished thing forces you to describe success concretely, and to do it before you are invested in a route. Then walking backwards gives you the plan for free, because each step is simply "what has to be true just before this?". The steps you pass through on the way back are the steps you will take on the way forward, in reverse.</p>""",
    when="""
<p>Reach for it when you are setting out to make something that will finish: a project with an end, a goal you can picture, an opportunity you haven't yet decided to take. It is especially useful when a lot of people have opinions about how to do the thing and nobody has said what the thing is.</p>
<p>It is less useful for a problem to be diagnosed, where the end state is "the problem has gone" and the work is all in finding out why it is there. Use 5 Whys or the fishbone for that. On a Greggle board, Working Backwards is offered on a Project, a Goal and an Opportunity.</p>""",
    steps=[
        "Write one paragraph describing the thing finished, dated in the future, as if a stranger were reporting it. Say who it is for and what it does for them.",
        "List the evidence that would prove it worked. Numbers where there are numbers. Who says so, if it is people.",
        "Write the questions a sceptic would ask. How much did it cost? What went wrong? Why hasn't someone done this already? Answer each one honestly, and notice which you can't.",
        "Now walk back. What has to be true the week before that ending? Write it down. And the month before that?",
        "Keep walking until you reach today. The list you have made, read bottom to top, is the plan.",
        "Look at the first step. If it is something you could do this week, start. If it isn't, cut it smaller.",
    ],
    board_intro="Pick Working Backwards on a Project board and Greggle proposes the ending first, then the steps back to now. You review each one before it lands.",
    board=[
        dict(label="done", name="What it looks like finished", text="A paragraph, dated in the future, as a stranger would report it."),
        dict(label="evidence", name="How we would know it worked", text="The numbers, or the people, that would prove the ending was real."),
        dict(label="the sceptic", name="Questions we would have to answer", text="Cost, risk, why nobody has done this already. Answered or left honestly open."),
        dict(label="the week before", name="What has to be true just before done", text="Open this and it becomes a board of its own."),
        dict(label="the month before", name="And before that", text="Keep going until the step is something you could do this week."),
        dict(label="action", name="The first thing to do", text="Cut small enough to just do. Lands in your list.", action=True),
    ],
    example="""
<div class="card example">
  <span class="stated">a Project &middot; the science fair project</span>
  <p><b>Done.</b> It is the evening of 14 March. A working model showing how much energy the school's south roof could collect from the sun stands on the table in the hall. Visitors press a button and see the number for today's weather. It came second in its year, and the head of science has asked to keep it for open evening.</p>
  <p><b>Evidence.</b> The model works when a stranger presses the button. The number it shows matches a real reading to within ten per cent. Three judges' comments, and a placing.</p>
  <p><b>The sceptic.</b> How much did it cost? Under forty pounds, because the sensor is borrowed from the physics cupboard. What went wrong? The first sensor reading was nonsense and it took a week to find out why. Why hasn't someone done this? Someone probably has, so the display has to make it interesting rather than the idea.</p>
  <div class="qa">
    <div><b>The week before</b><span>The model has been tested by someone who hasn't seen it before, and the poster is printed.</span></div>
    <div><b>Two weeks before</b><span>The sensor gives a believable reading and the display shows it.</span></div>
    <div><b>A month before</b><span>The sensor is in hand and gives any reading at all.</span></div>
    <div><b>This week</b><span>Ask the physics department for the sensor. Find one real reading to check against.</span></div>
  </div>
  <p class="dim">The first step turned out to be an email, not a build. That is normal, and it is the point of walking back rather than forward.</p>
</div>""",
    falls="""
<p>It is only as good as the honesty of the press release. If you write the announcement you wish were true rather than one you could earn, the plan inherits the wish, and every backward step is a step towards a fantasy. The sceptic's questions are the protection, and the question people most often skip is "why hasn't someone done this already?".</p>
<p>It also assumes the ending is knowable. For a goal that is really an exploration, where you don't yet know what good would look like, write the ending anyway and treat it as a draft you expect to replace. A wrong ending you can argue with beats no ending at all.</p>""",
    pairs=[
        ("Pre-mortem", "Once you have the plan, imagine it failed and work out why. The two methods are the same walk in opposite directions."),
        ("Objectives and Key Results", "The evidence list is a set of key results. If a goal has no end date, OKRs are the better frame."),
        ("Issue Tree", "When a backward step is too big to see, split it into parts that don't overlap."),
    ],
    reading=[
        "Colin Bryar and Bill Carr, Working Backwards: Insights, Stories, and Secrets from Inside Amazon, 2021. Chapter five is the PR/FAQ.",
        "Jeff Bezos's 2004 letter to shareholders, on why Amazon replaced slides with written narratives.",
    ],
    try_="Say what kind of thing it is (a Project, a Goal or an Opportunity), then pick Working Backwards. Greggle asks for the ending first.",
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
<p>The silent writing matters as much as the framing. If the room talks, the first confident voice sets the list and everyone else adds variations. If everyone writes alone first, you get the quiet person's reason, which is often the one nobody else saw.</p>""",
    when="""
<p>Reach for it when a plan exists and hasn't started. That is the window. Run it too early and there is nothing to break; run it once the work is under way and it turns into a list of excuses for what is already going wrong. On a Greggle board, it is offered on a Project and on a Risk.</p>
<p>It is also useful on a decision you have nearly made. Tell yourself you chose the thing and it went badly, and see what comes to mind. If nothing does, that is worth knowing too.</p>""",
    steps=[
        "State the plan in a few lines, so everyone is imagining the same thing failing.",
        "Announce it. \"It is a year from today. This went badly. Not slightly, badly.\" Say it as a fact.",
        "Everyone writes, alone and in silence, every reason they can think of. Two minutes. Nobody talks.",
        "Go round the room. Each person reads one reason. Keep going round until the lists are empty. No discussion yet, and no defending the plan.",
        "Now pick. Which two or three reasons are both likely and preventable? Those are the ones that matter.",
        "Change the plan so those can't happen, or so you would see them coming. Write each change as an action.",
    ],
    board_intro="Pick Pre-mortem on a Project board and Greggle proposes the failure as the first step, then the reasons, then the prevention. Nothing is written for you.",
    board=[
        dict(label="the plan", name="What we are about to do", text="A few lines, so everyone imagines the same plan failing."),
        dict(label="the news", name="A year on, it failed badly", text="Stated as a fact, not a worry. This is the step people skip."),
        dict(label="reasons", name="Why it failed", text="Everyone's reasons, one per line. Open this step and each reason can become a board."),
        dict(label="the ones that count", name="Likely and preventable", text="Two or three. The rest are noted and left."),
        dict(label="action", name="Change the plan so this can't happen", text="One action per reason that counts.", action=True),
        dict(label="action", name="Plant a signpost", text="The early sign that would tell you it is happening anyway.", action=True),
    ],
    example="""
<div class="card example">
  <span class="stated">a Project &middot; a stall at the Saturday market</span>
  <p><b>The plan.</b> Rent a stall for four Saturdays in November selling the baked things that sell well at school. Split the profit three ways.</p>
  <p><b>The news.</b> It is next spring. The stall lost money and two of the three of you aren't speaking.</p>
  <div class="qa">
    <div><b>Reasons</b><span>It rained on two of the four Saturdays and nobody came. We baked too much on the first day and threw half away. Only one of us could actually get there at 6am with the trays. We never agreed what to do if someone couldn't make it. The council wanted a food hygiene certificate we didn't have. The person whose kitchen we used got fed up with the mess. The pricing was guessed and we sold out of the cheap thing and nothing else.</span></div>
    <div><b>Likely and preventable</b><span>The 6am problem, the hygiene certificate, and baking blind on day one.</span></div>
    <div><b>Actions</b><span>Check the council's rules before paying for the stall. Do the first Saturday with half the stock and count what sells. Write down, now, who does what if one of us is ill, and what happens to their share.</span></div>
    <div><b>Signpost</b><span>If the first Saturday's takings don't cover the stall fee, stop after the second and talk before the third.</span></div>
  </div>
  <p class="dim">The rain isn't preventable, so it doesn't make the cut. Notice that the reason most likely to end friendships was the one about sharing, and it took a pretend failure to say it out loud.</p>
</div>""",
    falls="""
<p>Done as a discussion instead of silent writing first, the loudest voice sets the list. Done by one person alone, it still works, but you only get one person's blind spots. Done too late, it becomes a post-mortem with extra steps.</p>
<p>The other failure is stopping after the list. A pre-mortem that produces twelve reasons and no changes to the plan was a nice conversation. The value is entirely in the two or three actions at the end, and in the signposts that would tell you the failure is arriving anyway.</p>""",
    pairs=[
        ("Working Backwards", "Write the ending first, plan back to now, then run a pre-mortem on the plan. One walk forward and one back."),
        ("Scenario Planning", "When the reasons for failure are outside your control, the weather or the council, build the futures instead of trying to prevent them."),
        ("5 Whys", "A pre-mortem reason that surprises you deserves five whys of its own."),
    ],
    reading=[
        "Gary Klein, \"Performing a Project Premortem\", Harvard Business Review, September 2007. Two pages.",
        "Deborah J. Mitchell, J. Edward Russo and Nancy Pennington, \"Back to the future: Temporal perspective in the explanation of events\", Journal of Behavioral Decision Making, 1989.",
        "Daniel Kahneman, Thinking, Fast and Slow, 2011, chapter 24.",
    ],
    try_="Say what kind of thing it is (a Project or a Risk), then pick Pre-mortem. Greggle states the failure and asks you why.",
    cta="Tell yourself it failed. Then find out why.",
))

METHODS.append(dict(
    slug="first-principles", name="First Principles", kind="a Challenge",
    desc="Where first principles thinking came from, why it works, when it is the wrong tool, and how to run it: Aristotle's method for reasoning from what is actually true.",
    lead="Find the truths nothing else rests on, then build up from them alone.",
    facts=dict(origin="Aristotle, fourth century BC", best="a Challenge, or a Problem where the obvious answers have failed", takes="An hour, done properly", needs="A willingness to look stupid"),
    origin="""
<p>Aristotle opens his Physics by saying that we think we understand a thing when we know its first causes and first principles, the basic truths that don't rest on anything else. Everything we know about a subject is either one of those, or built on them. The Greek word is arche, a beginning.</p>
<p>Descartes rebuilt the whole of philosophy this way in 1637, doubting everything he could doubt until he found something he couldn't, and starting again from there. Engineers and physicists have worked this way ever since, mostly without naming it. The method came back into everyday conversation around 2012, when Elon Musk described using it to argue that battery packs didn't have to cost what they cost. What are batteries made of? Cobalt, nickel, aluminium, carbon, some polymers, a can. What do those cost on the metals exchange? A small fraction of the price of a pack. So the price is a fact about how packs are currently made, not a fact about batteries.</p>
<p>That example has been repeated so often it has become a cliche, which is a shame, because the move underneath it is sound and rare.</p>""",
    works="""
<p>Almost all reasoning is by analogy. This is like that, so do what worked for that. Analogy is fast, and most of the time it is right, which is why we use it. But it carries every assumption of the thing you compared to, and you never see those assumptions because you never chose them.</p>
<p>Going back to what is actually true strips the inherited assumptions out. Quite often the "impossible" part of a challenge was never a fact about the world at all. It was a fact about how everyone has been doing it, dressed up as a law.</p>""",
    when="""
<p>Reach for it when the standard answer doesn't fit and you can feel it, when everyone agrees something can't be done and nobody can say why, or when you have tried the obvious things and they haven't worked. It suits a Challenge, where the outcome isn't in your control and you need an edge nobody else has looked for.</p>
<p>Don't use it on things other people have already worked out properly. Reasoning from first principles about how to boil an egg is a way of spending an hour to arrive where a recipe would have taken you in a minute. It is also slow and a bit arrogant, and both are fine as long as you reserve it for where they pay.</p>""",
    steps=[
        "Write the challenge in one line, without any of the assumptions about how it is usually approached.",
        "List everything you believe about it. Every \"you have to\", \"you can't\", \"the way it works is\". Don't judge yet, just write.",
        "For each belief, ask \"how do I know that?\". Cross out anything whose only support is that it has always been done that way, or that someone told you.",
        "For what survives, ask again. Keep going until each remaining line is something you would bet on, and could say why.",
        "Look at the short list left. Those are the first principles. Read them together and ask what they permit that the crossed-out beliefs forbade.",
        "Build a plan from the short list only. Where it looks strange, that is the point; check it, but don't reject it for being unusual.",
    ],
    board_intro="Pick First Principles on a Challenge board and Greggle proposes the beliefs as a step to fill, the test for each, and the build from what survives. The beliefs are yours to write.",
    board=[
        dict(label="the challenge", name="What we are trying to do", text="Stated plainly, without the usual way of doing it baked in."),
        dict(label="beliefs", name="Everything we think is true about it", text="Open this and each belief becomes a step of its own."),
        dict(label="the test", name="How do we know?", text="Each belief gets asked. Inherited ones get struck out."),
        dict(label="what survives", name="The truths nothing else rests on", text="A short list. Usually shorter than you expected."),
        dict(label="what that permits", name="Options the old beliefs hid", text="Read the short list together. What does it allow?"),
        dict(label="action", name="The first unusual step", text="Built from the short list only. Marked as an action.", action=True),
    ],
    example="""
<div class="card example">
  <span class="stated">a Challenge &middot; the debating final</span>
  <p><b>The challenge.</b> Win the final against the school that has won it four years running.</p>
  <div class="qa">
    <div><b>Beliefs</b><span>They are better speakers than us. You win debates by being confident. We need to know more about the motion than they do. The judges like them. We should prepare more arguments than they have.</span></div>
    <div><b>How do we know?</b><span>"Better speakers" is a feeling from watching them win. "Confidence wins" is what everyone says. "The judges like them" is a guess. "More arguments" is how we have always prepared. None of these survive the question.</span></div>
    <div><b>What survives</b><span>The judges score against a published sheet. The sheet gives more marks for rebuttal than for opening argument. Each speaker has four minutes and the clock is enforced. Their last three finals were won on rebuttal.</span></div>
    <div><b>What that permits</b><span>We don't need to out-argue them. We need to out-rebut them, in four minutes, on the sheet the judges are actually holding. Preparation should be spent predicting their arguments and writing the rebuttal, not on more arguments of our own.</span></div>
    <div><b>Action</b><span>Get the judges' scoring sheet. Watch their last three finals and list every argument they used. Rehearse rebutting those, timed.</span></div>
  </div>
  <p class="dim">The plan looks odd, because it involves preparing fewer arguments for a debating final. That oddness is what first principles buys you. Everyone else is preparing more.</p>
</div>""",
    falls="""
<p>It is slow, and it is easy to mistake a strongly held belief for a first principle. "How do I know that?" has to be asked honestly, and the honest answer is often "I don't". If everything survives the test, you weren't testing.</p>
<p>The other trap is contempt for the people who did it the old way. Sometimes the old way is old because it works and the reasons have been forgotten. First principles should make you check the old way, not sneer at it. If your rebuilt plan is wildly different from what everyone else does, treat that as a reason to look harder, then proceed if it holds.</p>""",
    pairs=[
        ("Issue Tree", "Once the principles are clear, the tree is how you turn them into parts you can work on."),
        ("Strategic Challenge Map", "When there are many challenges and you need to know which one to attack, map them first, then go to first principles on the crux."),
        ("Options and Criteria", "The surviving truths are the criteria. Now generate the options."),
    ],
    reading=[
        "Aristotle, Physics, book one, chapter one; Metaphysics, book one. Any translation. The opening lines of the Physics are the whole idea.",
        "Rene Descartes, Discourse on the Method, 1637. Short, and still readable.",
    ],
    try_="Say what kind of thing it is (a Challenge), then pick First Principles. Greggle asks for your beliefs, then asks how you know.",
    cta="Find out what is actually true. Build from only that.",
))

METHODS.append(dict(
    slug="force-field-analysis", name="Force Field Analysis", kind="a Decision or a stalled Goal",
    desc="Where force field analysis came from, why removing a restraint beats pushing harder, and how to run it: Kurt Lewin's method for shifting something that has stuck.",
    lead="What is pushing for the change, what is holding it back, and which single restraint you could actually remove.",
    facts=dict(origin="Kurt Lewin, 1940s", best="a Decision about a change, a Goal that has stalled", takes="Twenty minutes", needs="Honesty about what is holding you back"),
    origin="""
<p>Kurt Lewin was a German psychologist who left Berlin for America in 1933 and, in the fourteen years before his death in 1947, founded most of what is now called social psychology. He thought of any situation, a person, a group, a factory floor, as a field of forces held in balance. Some push towards a change; some hold it back. Nothing moves while they balance. Something moves when they don't.</p>
<p>His observation, which is the whole method, is that there are two ways to unbalance the field, and they are not equal. You can push harder. Or you can remove something that is holding the change back. Pushing harder works briefly and raises resistance, because the restraining forces push back in proportion. Removing a restraint lets the change happen with the push you already have. Lewin's papers were collected as Field Theory in Social Science in 1951, after he died. The analysis, drawn as two columns of arrows pointing at a line, has been used in change management ever since.</p>""",
    works="""
<p>It makes you write the things holding you back in a separate column from the things pushing you forward, and then it makes you choose one restraint to remove. Most people, when something has stalled, only ever add more push: more motivation, more reminders, more pressure. The restraints are still there, so the thing stays stalled and now everyone is tired.</p>
<p>Naming the restraints one by one, and scoring them, shows that they are not all equal and that at least one is usually cheap to remove. That one is the action.</p>""",
    when="""
<p>Reach for it when you are deciding whether to change something, or when a goal you have been pushing towards has stopped moving. It suits a change that involves other people particularly well, because the restraints are usually other people's, and this makes you write them down as forces rather than as villains.</p>
<p>It is the wrong tool for choosing between several options; that is Options and Criteria. It is also weak on a change you don't yet want, since the whole method assumes the push exists. On a Greggle board, it is offered on a Decision and on a Goal.</p>""",
    steps=[
        "Write the change in one line at the top. Not the goal, the change: what would be different.",
        "Left column, everything pushing for it. Reasons, people, deadlines, things that have already started to shift.",
        "Right column, everything holding it back. Be honest, and include the ones that are about you.",
        "Score every force out of five for how strong it is. Don't add the columns up; the scores are for ranking, not arithmetic.",
        "Look only at the right column. For each restraint, ask what it would take to weaken it. Find the one you could weaken most for the least.",
        "That is your first action. Do it, then look at the field again, because removing one restraint often changes the others.",
    ],
    board_intro="Pick Force Field Analysis on a Goal or Decision board and Greggle proposes the change, the two columns, and the one restraint to remove. You supply the forces.",
    board=[
        dict(label="the change", name="What would be different", text="One line. The thing itself, not the reason for it."),
        dict(label="pushing for it", name="The driving forces", text="Open this and each force becomes a step, with a score out of five."),
        dict(label="holding it back", name="The restraining forces", text="The honest list, including the ones about you."),
        dict(label="the weakest link", name="The restraint that costs least to remove", text="One. Chosen from the right-hand column only."),
        dict(label="action", name="Remove it", text="Marked as an action. The first thing to actually do.", action=True),
        dict(label="then", name="Look at the field again", text="Restraints move when one is removed. Re-score before the next."),
    ],
    example="""
<div class="card example">
  <span class="stated">a Goal &middot; make the first team this season</span>
  <p><b>The change.</b> I am picked for the first team for the second half of the season.</p>
  <div class="tablewrap"><table>
    <tr><th>Pushing for it</th><th>Score</th><th>Holding it back</th><th>Score</th></tr>
    <tr><td>Fitness is better than last year</td><td>4</td><td>Tuesday training clashes with my shift at the shop</td><td>5</td></tr>
    <tr><td>The coach has said I am close</td><td>4</td><td>No lift to Saturday away matches</td><td>4</td></tr>
    <tr><td>Two first-team players leave at Christmas</td><td>5</td><td>The current player in my position is popular</td><td>3</td></tr>
    <tr><td>A friend already on the team who talks me up</td><td>2</td><td>I get nervous in trials and play worse than in training</td><td>4</td></tr>
  </table></div>
  <div class="qa">
    <div><b>The weakest link</b><span>The shift clash scores highest and is the cheapest to move. It is one conversation with the shop about swapping Tuesday for Sunday. The nerves score high too but are slow to change. The popular player isn't a restraint you should try to remove at all.</span></div>
    <div><b>Action</b><span>Ask the manager this week about moving the Tuesday shift. If yes, be at every Tuesday training until Christmas.</span></div>
    <div><b>Then</b><span>With Tuesdays sorted, the lift problem may solve itself, because someone at Tuesday training drives to Saturday matches.</span></div>
  </div>
  <p class="dim">Left to itself, the instinct is to add push: train harder, want it more. The field says the fastest way to move is to stop missing Tuesdays.</p>
</div>""",
    falls="""
<p>The scores invite false precision. People add up the columns, get 15 against 16, and conclude the change is impossible by one point. The scores exist to rank the restraints and nothing else.</p>
<p>It is also easy to fill the right-hand column with other people and leave yourself out. The restraint that is about you, the nerves in the example, is often the one that matters most in the long run even if it isn't the one to remove first. Write it down anyway.</p>""",
    pairs=[
        ("Stakeholder and Influence Map", "When most of the restraints are people, map them properly: what does each one actually want?"),
        ("5 Whys", "A restraint that scores five deserves to be asked why, five times. It may not be what it looks like."),
        ("Options and Criteria", "If the field shows the change is worth making, and there are several ways to make it, choose between them with criteria written first."),
    ],
    reading=[
        "Kurt Lewin, Field Theory in Social Science, 1951, edited by Dorwin Cartwright. The force field is in the papers on group decision and social change.",
        "Kurt Lewin, \"Frontiers in Group Dynamics\", Human Relations, 1947. Where unfreezing, moving and refreezing first appear.",
    ],
    try_="Say what kind of thing it is (a Goal or a Decision), then pick Force Field Analysis. Greggle sets up the two columns.",
    cta="Stop pushing harder. Remove one thing that is holding it back.",
))

METHODS.append(dict(
    slug="options-and-criteria", name="Options and Criteria", kind="a Decision",
    desc="Where the decision matrix came from, why the order of the steps is the whole method, and how to run it honestly: from Franklin's prudential algebra to Kepner-Tregoe.",
    lead="Write down what a good answer would have to do before you look at the answers.",
    facts=dict(origin="Franklin, 1772; Kepner and Tregoe, 1965", best="a Decision, or an Opportunity", takes="Half an hour", needs="Criteria written before the options"),
    origin="""
<p>Older than any company. In September 1772 Benjamin Franklin wrote to his friend Joseph Priestley, who was agonising over a job offer, and described what he called his moral or prudential algebra. Draw a line down a sheet of paper. Write the reasons for on one side, the reasons against on the other, over three or four days as they occur to you. Then strike out pairs of equal weight, a "for" against an "against", two weak ones against one strong one, until one side is empty. What remains is the answer, and it is an answer you can explain.</p>
<p>Charles Kepner and Benjamin Tregoe, two researchers who met at the RAND Corporation in the 1950s, turned the same instinct into a formal method for managers, published in The Rational Manager in 1965. Their decision analysis separates the criteria into musts, which any option has to satisfy or it is out, and wants, which are weighted and scored. Stuart Pugh's concept selection matrix, from 1981, is the engineering version, where options are scored against a reference design rather than against each other.</p>
<p>Everyone has seen the grid. What almost nobody does is fill it in in the right order.</p>""",
    works="""
<p>The matrix is almost beside the point. The sequence is the method. If you list the options first, the one you already like starts writing its own criteria: it is fast, so speed becomes a criterion; it is cheap, so cost becomes one. By the time you score, the answer was decided before the grid existed, and the grid is just an alibi.</p>
<p>Writing down what a good answer would have to do, before any answer is on the table, stops that. It also gives you the must-haves, which do most of the work. Options that fail a must are gone, and often that leaves two, which a person can choose between honestly without any scoring at all.</p>""",
    when="""
<p>Reach for it when there is a genuine choice between several things and you can feel your preference pulling you before you have thought. It suits a Decision above all, and an Opportunity where the choice is whether to pursue it at all, with "do nothing" as one of the options.</p>
<p>It is the wrong tool when there is only one option and the question is whether to take it; that is Force Field Analysis. It is also weak on a choice whose outcome depends heavily on things outside your control, where Scenario Planning does better. On a Greggle board, Options and Criteria is offered on a Decision and on an Opportunity.</p>""",
    steps=[
        "Write the decision in one line. \"Which subjects next year\", not \"what should I do with my life\".",
        "Before listing any option, write what a good outcome must have. These are the musts. An option that fails one is out, regardless of everything else.",
        "Now write what a good outcome would ideally have. These are the wants. Give each a weight: how much it matters, out of five.",
        "Only now list the options. Include the boring one and the one you are secretly hoping for.",
        "Strike out any option that fails a must. Score what is left against each want, out of five, and multiply by the weight.",
        "Look at the result and ask whether it surprises you. If it does, work out whether the criteria are wrong or your gut is. Don't edit the criteria to fix the answer; if you must change them, say why and start again.",
    ],
    board_intro="Pick Options and Criteria on a Decision board and Greggle proposes the criteria as the first step, before the options, so the order is protected for you.",
    board=[
        dict(label="the decision", name="What is being chosen", text="One line. One choice."),
        dict(label="musts", name="What any answer has to have", text="Fail one of these and the option is out. Written before any option."),
        dict(label="wants", name="What a good answer would have", text="Each with a weight out of five. Open this and each want is a step."),
        dict(label="options", name="Only now, the options", text="Including the boring one and the one you are hoping for."),
        dict(label="the score", name="Strike out, then score what is left", text="Musts first. Then wants times weights."),
        dict(label="action", name="The choice, and why", text="One sentence. Marked as an action.", action=True),
    ],
    example="""
<div class="card example">
  <span class="stated">a Decision &middot; which subjects to take next year</span>
  <div class="qa">
    <div><b>Musts</b><span>Keeps the two university courses I am considering open. Fits the timetable without a clash. I have at least a B in it now, or it is new.</span></div>
    <div><b>Wants</b><span>I would enjoy it (5). A teacher I work well with (3). Friends in the class (1). Useful whatever I end up doing (4).</span></div>
    <div><b>Options</b><span>Physics, Chemistry, History, Economics, Art, Further Maths.</span></div>
    <div><b>Musts applied</b><span>Art clashes with Chemistry. Further Maths needs an A now and I have a B. Both out. History doesn't keep either course open on its own but doesn't close one either, so it stays.</span></div>
  </div>
  <div class="tablewrap"><table>
    <tr><th>Option</th><th>Enjoy (5)</th><th>Teacher (3)</th><th>Friends (1)</th><th>Useful (4)</th><th>Total</th></tr>
    <tr><td>Physics</td><td>3 = 15</td><td>4 = 12</td><td>2 = 2</td><td>5 = 20</td><td>49</td></tr>
    <tr><td>Chemistry</td><td>2 = 10</td><td>2 = 6</td><td>4 = 4</td><td>5 = 20</td><td>40</td></tr>
    <tr><td>History</td><td>5 = 25</td><td>5 = 15</td><td>3 = 3</td><td>3 = 12</td><td>55</td></tr>
    <tr><td>Economics</td><td>4 = 20</td><td>3 = 9</td><td>2 = 2</td><td>4 = 16</td><td>47</td></tr>
  </table></div>
  <div class="qa">
    <div><b>Does it surprise you?</b><span>History winning did. The gut said Physics and Chemistry, because that is what "serious" looks like. But the musts already said the courses stay open with Physics alone, and the wants say History is the one I would actually turn up to. Physics and History, then, with Economics as the third.</span></div>
  </div>
  <p class="dim">If the surprise had felt wrong rather than interesting, the honest move would be to ask which want was missing, write it down, say why, and score again. Not to nudge History's numbers until Chemistry won.</p>
</div>""",
    falls="""
<p>Weights and scores can be tuned until the favourite wins, and everyone who has used a decision matrix has done this at least once. The protection is writing the criteria first and refusing to edit them afterwards without saying out loud what changed and why.</p>
<p>The grid also gives an impression of precision it doesn't have. A total of 55 against 49 is not a six-point margin of truth. It is a ranking, and it tells you History is probably ahead and Physics and Economics are close. Treat the numbers as a way of seeing, not as the answer.</p>""",
    pairs=[
        ("First Principles", "When you can't think of the criteria, go back to what is actually true about the situation. The truths are the criteria."),
        ("Scenario Planning", "If the best option changes depending on how the world turns out, score the options in each future, not just one."),
        ("Answer First", "Once chosen, say it in one sentence with the reasons beneath. The matrix is the evidence, not the answer."),
    ],
    reading=[
        "Benjamin Franklin, letter to Joseph Priestley, 19 September 1772. One page, and worth reading in full.",
        "Charles H. Kepner and Benjamin B. Tregoe, The Rational Manager, 1965. Decision analysis is the middle third.",
        "Stuart Pugh, Total Design, 1991, for concept selection; the method dates from his 1981 conference paper.",
    ],
    try_="Say what kind of thing it is (a Decision or an Opportunity), then pick Options and Criteria. Greggle asks for the criteria before it will take an option.",
    cta="Decide what good looks like. Then look at the options.",
))

for m in METHODS:
    m["try"] = m.pop("try_")

write_index()
for m in METHODS:
    write_method(m)
print("wrote", len(METHODS) + 1, "pages")
