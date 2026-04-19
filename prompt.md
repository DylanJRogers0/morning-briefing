Daily briefing for XXXX (Researcher on AI and geopolitics, writes Features and Targets Substack). Search the web and Gmail (last 24 hours) for material. Fetch today's Google Calendar events.

IMPORTANT — WORKING METHOD: Complete and write each section to briefing.md using the Write/Edit tools before moving to the next. Do not compose everything in memory at the end. After all sections are written to briefing.md, read the file and create the Gmail draft from it.

STRUCTURE — follow exactly:

# Morning Briefing — [Date]

## Today's Calendar
All events with times in Eastern Time. IMPORTANT: First call list_calendars to get every calendar ID, then call list_events for each calendar ID for today's date. Combine results from all calendars.

## 1. LEADING STORIES (6 stories)
Top stories at the intersection of AI, technology, and geopolitics. For each: one-sentence overview, then a "Why it matters" line for a senior policy or investment decision-maker. Geographic and sector diversity required.

## 2. GEOPOLITICS (5 stories)
Analytical coverage — not merely descriptive — of each:
- AI & Technology Power Competition: US-China AI race, compute access, export controls, frontier model developments, semiconductor supply chains
- US Foreign Policy & the Middle East: Iran, regional dynamics, US posture
- China: Domestic politics, Taiwan, Belt and Road, tech policy, PLA developments
- United Kingdom: AI strategy, defence spending, foreign policy
- European Union: AI Act implementation, strategic autonomy, trade policy
- Latin America: Tech investment, US relations, political developments
- Africa: AI adoption, great power competition, political economy
- Elections Horizon Calendar: Table of elections and referenda globally in the next 60 days

## 3. POLITICS (5 stories)
What is driving the political day in Washington DC and London. Draw primarily from Politico (US and EU editions) and Westminster-focused sources. Cover: key legislative activity, White House and No. 10 priorities, significant political appointments or departures, and anything with direct bearing on AI or technology policy.

## 4. BUSINESS (5 stories)
Framed for a senior decision-maker: what does each mean for capital allocation, supply chains, regulatory exposure, or competitive positioning? Geographic and sector diversity. Include capital-markets and political-economy logic where geopolitics intersects markets.

## 5. SUBSTACK ROUNDUP
Search Gmail for new posts in the last 24 hours from these Substacks. For each: title, 2-3 sentence summary of the key argument, and a link. Skip any with no new posts.

ChinaTalk, Defence Affairs Magazine, Pekingnology, Britain's World, OpenAI Global Affairs/The Prompt, Epoch AI, Interconnects (Nathan Lambert), Don't Worry About the Vase (Zvi Mowshowitz), AINews (swyx), Chipstrat, AI Policy Perspectives, Asterisk Magazine, The Generalist, The State of the Future, The Algorithmic Bridge (Alberto Romero), Anton Leicht, Dan Davies - Back of Mind, Chamath Palihapitiya, Latent.Space, AI Tidbits, Future State, Transformer, Air Street Press, Astral Codex Ten, ChinAI Newsletter, Import AI (Jack Clark), Sentinel Global Risks Watch, AI Policy Bulletin, AGI Strategy, Silicon Continent, UK 2.0, Simon Willison, Joe Carlsmith, Notes on Growth.

---

SOURCING RULES
- Strict 24-hour window for all sections except Research Annex (7-day window).
- Primary news sources: The Economist, Financial Times, Bloomberg, Reuters, Associated Press, Wall Street Journal, Foreign Affairs, Foreign Policy, Politico.
- Weave in analysis from: CSIS, IISS, Brookings, Carnegie Endowment, RAND, ECFR.
- Weave in market commentary from: Goldman Sachs Research, JPMorgan, Morgan Stanley where available.
- Embed all hyperlinks inline. Do not collect at the end.

STYLE
- British English throughout.
- Tight and scannable: use bullet points and short paragraphs. No long prose blocks.
- Each story or entry should be 2-4 lines maximum. Lead with the fact, follow with the implication.
- No filler phrases ("it's worth noting", "importantly", "it is clear that").
- Where geopolitics intersects markets, include capital-markets logic in one concise line.
- Mark any predictions clearly as predictions.
- Bold key terms and conclusions.

---

DELIVERY
Once the briefing is complete, run python3 /home/user/morning-briefing/send_draft.py via the Bash tool to create the Gmail draft.
