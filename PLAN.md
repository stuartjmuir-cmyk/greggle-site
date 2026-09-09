# Greggle website plan

The front page does one job: get someone to open the app. This plan adds the
second job, which is to make greggle.app the place people come to understand
the fourteen ways of thinking the app offers, where each one came from, why it
works, and how to run it well. The last section looks past the site at where
the whole model could go next.

Everything here stays inside the constraints the README sets: plain static
files, no build step, the app is a separate site and nothing here touches it.

## 1. What the site should become

Today the site is a landing page. It should become a landing page plus a
reference library, with the library doing three things the front page can't:

- Give each method its own page with enough depth that a reader could run the
  method on paper without ever opening the app.
- Earn search traffic. People search for "5 whys template", "how to run a
  pre-mortem", "force field analysis example" in large numbers. Each method
  page is a real answer to one of those searches, and the app is the obvious
  next step at the bottom of each.
- Make the case for the whole approach. The front page says "none of them were
  invented here, that is the point". The library is the proof.

Audience. The front page's examples are a science fair, a debating final, a band
that keeps missing practice, choosing subjects for next year, a market stall.
That reads as students and their parents first, working adults second. The
method pages should keep that register: plain words, no consulting jargon,
examples a sixteen-year-old and a forty-year-old would both recognise. Where a
method's origin is a factory or a boardroom, say so, then bring it home.

## 2. Site structure

```
/                          front page (exists, small edits)
/methods/                  index of the fourteen, grouped by what they are for
/methods/five-whys/        one page per method, fourteen in total
/methods/working-backwards/
  ... etc
/kinds/                    the seven kinds of thing, one page, later
/why/                      the essay: methods over answers (section 5 below)
/about/                    who made it, how to send feedback, the privacy claim
```

Folders with an index.html rather than flat files, so URLs are clean and can
never break if a page later needs assets of its own. Slugs are lower-case,
hyphenated, and never change once published.

Front page edits are small. The "See the ways of thinking" button and each of
the fourteen method cards link into /methods/. The footer gains links to
/methods/, /why/ and /about/. Nothing else on the front page moves.

### Grouping the fourteen

The front page splits them into six featured and eight more, which is a layout
decision, not a meaningful one. The index page should group by what the reader
is trying to do, because that is the question they arrive with:

| You want to | Methods |
| --- | --- |
| Work out what is actually wrong | 5 Whys, Cause and Effect, Theory of Constraints |
| Break a big question into parts | Issue Tree, First Principles, Strategic Challenge Map |
| Decide between options | Options and Criteria, Force Field Analysis |
| Plan towards something | Working Backwards, Objectives and Key Results |
| See what could go wrong | Pre-mortem, Scenario Planning |
| Bring other people with you | Stakeholder and Influence Map, Answer First |

Each group maps loosely onto the seven kinds of thing (a Problem wants the first
row, a Decision the third, a Risk the fifth). The index should show that mapping
so the two vocabularies reinforce each other rather than compete.

## 3. The method page template

Every method page follows the same shape, in the same order, so a reader who has
read one knows how to read the rest. Sections are short. The whole page should
read in under five minutes.

1. Name and one line. What it is in a sentence a child could repeat.
2. Where it came from. A named person, a place, a decade, and the story of the
   problem it was invented to solve. This is the compelling part and deserves
   real writing. Cite the primary source at the bottom.
3. Why it works. The mechanism, in plain terms. Where real evidence exists, say
   what it is. Where the only evidence is decades of practitioner use, say that
   too. The brand promise is honesty, so the pages have to be honest about
   this.
4. When to reach for it, and when not to. Which of the seven kinds it suits.
   Which situations it handles badly.
5. How to run it. Numbered steps that work with a pen and paper. Five to eight
   steps, no more.
6. How it looks on a Greggle board. What the app proposes as the first cut,
   what each step contains, where the actions end up. One screenshot of a real
   board running this method.
7. A worked example in the site's own register. One of the front page examples,
   carried through the method start to finish.
8. Where it falls down. The known criticisms and the common mistakes.
9. Pairs well with. Two or three other methods and why.
10. Try it. One button: open Greggle. If the app can accept a deep link that
    pre-selects the method, use it (open question, section 7).

Below is the content brief for each of the fourteen: the facts each page rests
on and the angle worth taking. Copy is written later, from these.

## 4. The fourteen methods

### 5 Whys

Origin. Toyota. The habit is credited to Sakichi Toyoda, founder of the Toyota
group, and was made a formal part of the Toyota Production System by Taiichi
Ohno, whose 1978 book gives the famous example of a machine that stopped: a
blown fuse, because of an overloaded bearing, because of poor lubrication,
because the pump was worn, because there was no strainer on the intake. Five
whys, one fix that stops it happening again.

Why it works. Each answer becomes the next question, so you can't stop at the
first plausible cause. The discipline is in refusing to accept "someone made a
mistake" as an answer, because people will always make mistakes and you can't
fix that. You can fix the strainer.

Best for. A Problem. Also a Risk that has happened before.

How to apply. Write the problem as a single observed fact, not an opinion. Ask
why it happened and write one answer. Ask why of that answer. Keep going until
the answer is something you could change tomorrow. Five is a guide, not a rule;
three is often enough and seven is sometimes needed.

Falls down. It assumes one chain of causes, and real problems often have
several. It is also easy to reason your way to the cause you already believed
in. Use Cause and Effect first when the problem feels wide rather than deep.
Alan Card's 2017 critique in BMJ Quality and Safety is the honest reference
here.

### Working Backwards

Origin. Amazon, early 2000s. Before building anything, a team writes the press
release announcing it as if it already shipped, plus the questions a sceptical
customer or journalist would ask. If the press release isn't compelling, the
product isn't built. The Kindle was developed this way. Colin Bryar and Bill
Carr, who ran it inside Amazon, wrote the method up in their 2021 book of the
same name.

Why it works. Starting from the finished thing forces you to describe what
success is in concrete terms before you are invested in a particular route to
it. Most plans go wrong because "done" was never defined.

Best for. A Project, a Goal, an Opportunity.

How to apply. Write one paragraph describing the thing finished, dated in the
future, as if reporting it. List the evidence that would prove it worked. Then
ask what has to be true the week before that, and the month before that, back
to today. The steps you passed through on the way back are the plan.

Falls down. It is only as good as the honesty of the press release. If you
write the announcement you wish were true rather than one you could actually
earn, the plan inherits the wish.

### Pre-mortem

Origin. Gary Klein, a psychologist who studies how people make decisions under
pressure, published the pre-mortem in Harvard Business Review in 2007. It rests
on a 1989 study by Deborah Mitchell, Jay Russo and Nancy Pennington which
found that imagining an event has already happened, rather than that it might,
increased people's ability to identify reasons for it by about 30 percent.
Daniel Kahneman has called it his favourite technique for countering
overconfidence.

Why it works. Once a plan exists, people on it stop looking for its flaws,
partly out of loyalty and partly because doubt feels disloyal. The pre-mortem
gives everyone permission to be the pessimist, because the failure is a
premise, not an accusation.

Best for. A Project or a Risk, run once the plan exists and before it starts.

How to apply. State the plan. Announce that it is a year from now and the plan
failed badly. Each person writes, alone, every reason they can think of. Read
them out one at a time, one reason per person per round. Pick the two or three
most likely and change the plan to prevent them.

Falls down. Done as a group discussion instead of silent writing first, the
loudest voice sets the list. Done too late, when the plan is already in motion,
it becomes a list of excuses.

### First Principles

Origin. Aristotle, who wrote that we understand a thing when we know its first
causes and principles, the basic truths that don't rest on anything else.
Descartes rebuilt philosophy this way in the 1600s. It came back into everyday
use in the 2010s through engineers who used it to challenge assumptions about
what things had to cost, the standard example being the price of battery
packs versus the price of the metals inside them.

Why it works. Most reasoning is by analogy: this is like that, so do what
worked for that. Analogy is fast but inherits every assumption of the thing
you compared to. Going back to what is actually true removes the inherited
assumptions and often shows that the "impossible" part was never really there.

Best for. A Challenge, an Opportunity, or any Problem where the obvious answers
have all been tried.

How to apply. Write the goal. List everything you believe about it. For each
belief ask "how do I know that?" and strike out anything that is only true
because it has always been done that way. What is left is a short list of
things that are actually true. Build a plan from only those.

Falls down. It is slow, and it is arrogant when applied to things other people
have already worked out properly. Reserve it for where the standard answer
genuinely doesn't fit.

### Force Field Analysis

Origin. Kurt Lewin, the German-born psychologist who founded much of social
psychology, in the 1940s. Lewin saw any situation as a balance between forces
pushing for change and forces holding it back, and argued that the balance is
easier to shift by removing a restraint than by pushing harder, because pushing
harder raises the resistance. His field theory was collected and published in
1951, after his death.

Why it works. It makes you list the things holding you back separately from the
things pushing you forward, and then makes you choose one restraint to remove.
Most people only ever add more push.

Best for. A Decision about whether to change something, a Goal that has stalled.

How to apply. Write the change in one line. Left column, everything pushing for
it. Right column, everything holding it back. Score each force out of five for
strength. Look only at the right column and pick the single restraint you could
weaken most cheaply. That is your first action.

Falls down. The scoring invites false precision. The scores are there to force
a ranking, not to be added up.

### Options and Criteria

Origin. Older than any company. Benjamin Franklin described his "prudential
algebra" in a 1772 letter: two columns, for and against, strike out items of
equal weight, see what remains. Charles Kepner and Benjamin Tregoe turned it
into a formal decision analysis at RAND in the 1950s and published it in 1965.
Stuart Pugh's 1981 concept selection matrix is the engineering version.

Why it works. Writing down what a good answer would have to do, before looking
at the answers, stops the answer you already like from writing its own
criteria. The matrix itself is almost beside the point; the sequence is the
method.

Best for. A Decision. Also an Opportunity, to decide whether to pursue it.

How to apply. Write the decision. List what a good outcome must have (must
haves, which kill options) and what it would be nice to have (wants). Only
then list the options, one of them doing nothing. Strike out any option
failing a must. For each survivor say what it wins on and what it costs, then
make the call and write down what would reverse it. The app deliberately has
no scoring arithmetic: a weighted total hides the judgement, so the page
should not teach one.

Falls down. Weights and scores can be tuned until the favourite wins, which is
why Greggle leaves them out. The protection is writing the criteria first and
not editing them afterwards, and refusing any option with an empty cost line.

### Issue Tree

Origin. McKinsey, and specifically Barbara Minto, who joined the firm in 1963
and codified the rule that the parts of any breakdown should be mutually
exclusive and collectively exhaustive (MECE: no overlaps, no gaps). Her book
The Pyramid Principle came out in 1978 and is still the consulting industry's
standard text.

Why it works. A question split into non-overlapping parts can be worked on in
parallel, and the "nothing left out" test catches the branch you forgot about
before it becomes the reason the plan failed.

Best for. A Challenge, a Project, a big Goal. Anything too large to see whole.

How to apply. Write the question at the top. Split it into two to five
sub-questions that don't overlap and together cover it. Test each split: could
a fact belong to two branches? Is there a fact that belongs to none? Repeat on
each branch until the leaves are things you can answer or do.

Falls down. Perfect MECE is rarely achievable and chasing it wastes time. Good
enough is "I can see no overlap and I can't think of a gap".

### Cause and Effect

Origin. Kaoru Ishikawa, a University of Tokyo professor and one of the founders
of Japanese quality management, drew the first fishbone diagram for engineers
at Kawasaki's shipyards, and set it out in his 1968 Guide to Quality Control.
The problem is the fish's head; the ribs are categories of cause, in
manufacturing traditionally people, methods, machines, materials, measurement
and environment.

Why it works. Where 5 Whys goes deep, this goes wide. The categories force you
to consider kinds of cause you would never have thought of on your own, and
seeing them all on one page shows which ones are crowded.

Best for. A Problem that feels like it has many causes, or where 5 Whys keeps
producing different answers each time.

How to apply. Write the problem as the head. Draw four to six ribs and name a
category on each. On each rib, list every cause you can think of in that
category, without judging. Circle the ones that appear on more than one rib or
that you could actually test. Take those into 5 Whys.

Falls down. The default manufacturing categories don't suit a band that misses
practice. Change them. For most personal problems, four ribs of people, time,
place and habits work better than six factory ones.

### Objectives and Key Results

Origin. Andy Grove at Intel in the 1970s, as a lighter version of the
management by objectives that Peter Drucker had proposed in the 1950s. Grove
described it in High Output Management in 1983. John Doerr, who learned it at
Intel, brought it to Google in 1999 when the company had around forty people,
and wrote it up in Measure What Matters in 2018.

Why it works. It separates the thing you want (the objective, which can be
ambitious and even vague) from the numbers that would prove you got there (the
key results, which can't be). Most goals fail because they were only ever the
first half.

Best for. A Goal, above all. A Project with a long horizon.

How to apply. Write one objective, in words that would make you want to do it.
Write three to five results that would prove it, each with a number. Check
that none of the results is an activity ("practise more") rather than an
outcome ("run the piece through without stopping"). Score them at the end
honestly; hitting seven out of ten on a hard result is the intended outcome.

Falls down. Companies pile them up until nobody reads them. One objective at a
time is plenty for a person.

### Scenario Planning

Origin. Herman Kahn at RAND in the 1950s, thinking through nuclear futures
nobody wanted to imagine, then Pierre Wack at Shell in the early 1970s. Wack's
team built scenarios in which oil producers cut supply and prices jumped, so
when the 1973 embargo came Shell's managers had already thought it through and
responded faster than any rival. Peter Schwartz, who succeeded Wack, wrote The
Art of the Long View in 1991.

Why it works. Forecasting picks one future and bets on it. Scenarios pick the
two most uncertain forces, cross them, and give you four futures to rehearse.
You stop asking "what will happen" and start asking "what would I do if".

Best for. A Risk, a Decision with a long horizon, an Opportunity whose value
depends on how the world turns out.

How to apply. Name the decision. List the forces outside your control that
would change the right answer. Pick the two most uncertain and most important.
Cross them to make four futures and give each a name. For each one, write
what you would do. Then plant signposts: the early signs that would tell you
which future is arriving.

Falls down. Four futures becomes fourteen becomes none. Two axes, four boxes,
that's the method.

### Stakeholder and Influence Map

Origin. R. Edward Freeman's 1984 book Strategic Management: A Stakeholder
Approach put the word into management. Aubrey Mendelow's 1981 power and
interest grid gave it a picture: who has the power to affect this, and how much
do they care.

Why it works. Most things that fail with people fail because someone who could
block it was never asked, or someone who cared was treated as if they didn't.
Putting names on a grid makes those gaps visible before they cost you.

Best for. A Challenge where the outcome isn't yours to control, an Opportunity
that needs permission, a Project with more than two people in it.

How to apply. List everyone affected or with a say. For each, note what they
actually want (not what they say). Place them on a grid: power on one side,
interest on the other. High power and high interest, keep close. High power
and low interest, keep satisfied. The rest, keep informed. Decide one thing to
do about each person in the top right corner.

Falls down. People aren't fixed points. Revisit the grid when anything changes,
and be careful what you write down about named people.

### Strategic Challenge Map

Origin. This one is Greggle's own synthesis rather than a single named method,
drawing mainly on Richard Rumelt's work: the idea in Good Strategy Bad
Strategy (2011) that strategy starts with an honest diagnosis of the challenge,
and the argument in The Crux (2022) that among many gnarly challenges you should
find the one you can actually move and attack that. The page should say this
plainly. (Confirm the exact lineage with whoever wrote the app's prompt for it,
see section 7.)

Why it works. Listing the challenges is easy and useless. Categorising them,
attaching evidence to each and then judging which ones you can move turns a
worry list into one decision about where to push.

Best for. A Challenge. A Goal that keeps failing for reasons nobody has named.

How to apply. Write every challenge standing between you and the goal. Sort
them into categories (things about you, things about others, things about
resources, things about timing). For each, write the evidence it is real, not
just felt. Judge each for how much you could move it. Choose the one that is
both movable and matters, and plan around that.

Falls down. Without the evidence step it becomes a list of fears. With it,
half the challenges usually evaporate.

### Theory of Constraints

Origin. Eliyahu Goldratt, an Israeli physicist, published it as a novel, The
Goal, in 1984. A plant manager has three months to save his factory and learns
that a system's output is limited by its one narrowest point, so improving
anything else is wasted effort. The five focusing steps: identify the
constraint, exploit it, subordinate everything else to it, elevate it, repeat.

Why it works. Effort spread evenly across a process improves nothing that
matters. Effort on the one narrow point improves everything downstream of it.
This is unintuitive, which is why it is worth a whole method.

Best for. A Problem where you are busy and nothing gets finished. A Project
that is late.

How to apply. Draw the steps of the thing as a flow. Find where work piles up
waiting. That is the constraint. Make sure it is never idle and never doing
anything it doesn't have to. Make every other step serve it, even if they
slow down. Only then spend anything on making it bigger. Then look again,
because the constraint has moved.

Falls down. People find a constraint and then try to fix three things at once.
One at a time, or it isn't the method.

### Answer First

Origin. Barbara Minto again. The Pyramid Principle's second rule, after MECE,
is that the answer goes at the top and the reasons hang beneath it, because a
reader who knows the conclusion can judge the reasons, while a reader waiting
for the conclusion can't judge anything. The military calls the same idea
BLUF, bottom line up front. Newspapers have written this way since the
telegraph.

Why it works. Writing the answer first exposes whether you have one. Most
rambling explanations are rambling because the writer hasn't decided.

Best for. The last step of anything: a Decision made, a Problem diagnosed, a
Project proposed to someone else.

How to apply. Write the answer in one sentence. Beneath it, write the two to
four reasons. Beneath each reason, the evidence. Read the top sentence alone
and ask whether someone could act on it. If not, it isn't the answer yet.

Falls down. Answer first with no reasons beneath is just an assertion. The
pyramid has to have a base.

## 5. The essay page, and where the model could go

The site needs one page that argues the case, because the fourteen method pages
each argue only for themselves. Working title: Why methods and not answers.
This is also the right place to think out loud about what Greggle could become,
which the rest of this section does.

### The argument

Every one of the fourteen methods is a set of questions, and only the person
asking can answer them. Nobody else knows why your band misses practice. No
search engine knows what a good answer to your subject choice would have to do.
Toyota's fifth why has to come out of the head of the person who was standing
at the machine. The methods are valuable precisely because they don't supply
content. They supply the shape that gets the content out of you.

That is the opposite of where most software is heading. The default now is to
ask a machine for the answer, which works well when the answer exists outside
you, and works badly, sometimes harmfully, when it doesn't. A plan for your
own life written by something that has never met you is a plausible-sounding
plan for someone else. Greggle's design already takes a side here: it proposes
a cut and adds nothing until you have looked at it, it counts rather than
scores, it holds nothing on a server. Those aren't privacy features. They are
what a tool looks like when it believes the knowledge is in the user.

### The natural extension

If that is the belief, the app is one expression of it and not the only one.
The wider thing is a set of tools, methods and systems for people who want to
solve problems, finish tasks and plan endeavours using what they already know.
Some directions, roughly in order of how close they are to what exists:

The library is the first extension and this plan builds it. A method page that
lets someone run a pre-mortem on paper is already a tool that needs no app.

Cards. Each method as a single printable page: the steps, the questions, a
blank grid where one is needed. Pen and paper is the most offline the work can
get, and a card on a kitchen table is how a method gets used by a family rather
than by whoever owns the laptop. Cheap to make from the method pages, and a
natural thing to give away.

More kinds of thing. The seven kinds are a good start and there are obvious
gaps: a Habit to build or break, a Skill to learn, a Conversation you are
dreading, a Piece of writing. Each new kind brings its own questions and its
own natural methods. A Habit wants Gabriele Oettingen's WOOP (wish, outcome,
obstacle, plan) and Peter Gollwitzer's implementation intentions. A Skill
wants deliberate practice and the Feynman technique. A Conversation wants Chris
Argyris's ladder of inference. None of these were invented here either.

More methods, chosen by the same rule: named origin, decades of use, runnable
by one person with a pen. Candidates worth a page even before they are in the
app: inversion (work out how to guarantee failure, then avoid it), the after
action review (the US Army's four questions), Fermi estimation, the
Eisenhower grid, Kepner-Tregoe's is/is-not problem analysis, Dave Snowden's
Cynefin for working out what kind of situation you are even in, and the
decision journal.

The knowledge audit. Every method assumes you know things, and most people
have never been asked to write down what they know about their own situation.
A method for that, before any other method: what do I know for certain, what do
I believe, what am I assuming, what would I need to find out and from whom.
Donna Ogle's KWL chart from 1986 (know, want to know, learned) is the
classroom version. This would be the method that feeds all the others, and it
is the one that most sharply separates a tool built on the user's knowledge
from one built on retrieval.

The review loop. Greggle can already read a board back and say what is
missing. The next thing to read back is the past. A decision journal records
what you decided, what you expected to happen and how sure you were, and
then, months later, what actually happened. Over a year it teaches a person
where their own judgment is reliable and where it isn't, which is knowledge
nobody else can give them. Finished boards are the raw material for this. It
stays on the device like everything else.

Fading. The most interesting version of the tool is one that plans its own
obsolescence. The first time someone runs a pre-mortem, the app walks them
through every question. The fifth time, it offers the board and stays quiet.
By the tenth, they run it in their head in a meeting and don't open anything.
This is cognitive apprenticeship (Collins, Brown and Newman, 1989): model,
coach, then fade the scaffolding. A tool that measured its success by how
little people needed it would be unusual, and it is exactly what a tool built
on the user's own knowledge should want.

The thread through all of these is the same rule the app already follows.
Elicit, don't generate. Show the count, not the score. Add nothing the person
hasn't looked at. Keep the work where the person is. If a proposed feature
breaks one of those, it belongs to a different product.

## 6. Build order

Phase one, done. The methods index and the six featured method pages (5 Whys,
Working Backwards, Pre-mortem, First Principles, Force Field Analysis, Options
and Criteria). Front page links updated. A shared stylesheet pulled out of
index.html so fourteen pages don't carry fourteen copies of it.

Phase two, done. The remaining eight method pages, written from the app's
framework files, and a real board screenshot on every method page, taken by
driving the app with the page's own worked example (tools/make-boards.js).

Phase three, done. The essay page at /why/ and the about page at /about/,
both linked from every page's navigation and footer.

Phase four, done. Cards: each method has a one-page A4 card at
/methods/<slug>/card/, made to print from the browser, and a PDF beside it
rendered by tools/make-cards.js. The kinds page at /kinds/.

After phase four. The first extension from section 5 is built: four more kinds
of thing (a Habit, a Skill, a Conversation, a Piece of writing), each with two
paper-only methods as cards under /cards/, introduced at the foot of the kinds
page. They are the first methods in the library that exist without the app.
The knowledge audit from section 5 is built as a card too, at /cards/knowledge-audit/,
introduced at the top of the kinds page as the thing to do before any method.

Each phase ships on its own. A half-finished phase two, with nine of fourteen
pages live, is fine; the index simply links the pages that exist.

## 7. Open questions

Two of the original questions were settled by reading the app's source, which
lives in the private `stuartjmuir-cmyk/Jigsaw` repository. Every method is a
data file under `src/frameworks/data/`, with its opening question, its steps,
the fields inside each step, and the checks the read-back runs. The six built
pages were corrected against those files, and the eight remaining pages should
be written from them rather than from memory. The kinds and the order in which
methods are suggested for each kind are in `src/domain/vocabulary.ts`.

- Deep links: the app reads nothing from the URL, so there is no way to open it
  with a method or kind pre-selected. Every try-it button opens the app's front
  door. Adding a query parameter to the app would be a small change and would
  make the method pages measurably more useful; worth raising there.
- Strategic Challenge Map: the app's own description is "a forensic breakdown
  for a complex organisation or market" and names no source. The page should
  say it is Greggle's own synthesis and leave Rumelt out unless Stuart says
  the lineage is real.
- Trademarks. The app deliberately ships Answer First without the name the
  method is famous by, or its owner's name, because that name is registered
  for software (see the app's decision note 04). The site's Answer First and
  Issue Tree pages cite the book and its author as sources, which is
  ordinary editorial citation rather than naming a product, but it is a
  judgement call and worth a look before the site is promoted.
- Voice on origin stories: how much history is too much? The brief above gives
  each about a paragraph. The pages could go longer for the good stories (Shell
  in 1973, Goldratt writing a novel) and shorter for the rest.
- Whether to add structured data (JSON-LD for HowTo) to the method pages for
  search. Cheap, harmless, probably worth it once the pages exist.

## 8. Conventions for the pages

Keep the front page's CSS variables and type: Instrument Sans, the same greys,
the same blue, the same card radius. Move the shared rules to /site.css and
have every page link it; the front page keeps working during the move because
it can link the stylesheet and keep its inline styles until they are pruned.

Every page carries a canonical URL, a description, og:title and og:description,
and the favicon. Method pages set og:image to their board screenshot.

No script anywhere unless a page genuinely needs it. No analytics. The site
should make the same promise the app does, and be able to prove it the same
way.

Headings in sentence case, no colons. Numbers as words below ten in prose.
Straight quotes. British spelling, matching the front page.
