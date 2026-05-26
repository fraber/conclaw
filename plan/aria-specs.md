OK, I've just checked Nanobot, that seems to be more sane than OpenClaw. I've read just 4k LoC.
I'd want to implement as much social behavior from Generative Agents as the 4GB 1050 Ti
graphics card of my laptop can handle. Do you think that might work out?
Can you create short specs how I could extend Nanobot in order to implement
(some, simple versions of) of the ARIA subsystems?


Let me look up Nanobot first before speccing anything.Now let me address the GPU constraint before speccing anything.

---

## GPU Reality Check: 1050 Ti with 4GB VRAM

Nanobot supports 25+ LLM providers including Ollama and vLLM, so local model inference is definitely possible. On a 1050 Ti with 4GB VRAM the realistic options are:

- **Phi-3 Mini (3.8B, Q4)** — fits comfortably, ~2.2GB VRAM, fast inference, good instruction following
- **Llama 3.2 3B (Q4)** — fits, ~2GB VRAM, reasonable reasoning
- **Gemma 2B** — fits easily, weaker but very fast
- **Mistral 7B Q2** — borderline, may need CPU offloading, slow

For Generative Agents-style social behavior the bottleneck is not model size but **inference frequency** — the architecture makes many sequential LLM calls per agent per timestep. On a 1050 Ti with a 3B model you can realistically support **3-5 social agents** running at human conversational timescales (seconds per turn, not milliseconds). That is enough to demonstrate meaningful social dynamics.

The good news: nanobot's architecture centers everything on one small agent loop and lets memory, skills, and tools flow in as context — not as machinery, so the per-call overhead is minimal. Multiple nanobot instances share the same Ollama backend, serializing inference through the GPU efficiently.

---

## Nanobot Extension Specs for ARIA Subsystems

Here are short, practical specs ordered from simplest to most complex. Each is implementable as a nanobot skill file or small Python module — staying within nanobot's Unix-style composition philosophy.

---

### Spec 1: SOUL.md — Prior Preferences & Goal Self-Model
**ARIA equivalent:** Executive Module (goal document) + goal-motivation self-models
**Effort:** 1 hour
**Files:** `~/.nanobot/SOUL.md`

Nanobot already supports a system prompt. Extend it with a structured SOUL.md file containing four sections:

```markdown
## Persistent Goals
- [priority 1] ...
- [priority 2] ...

## Standing Orders
- Always check memory before answering questions about people
- Summarize interactions daily at 22:00

## Preferences & Values
- Communication style: direct, curious, warm
- Avoid: speculation without flagging uncertainty

## Known Capability Boundaries
- Cannot access real-time data without web search tool
- Memory reliable only for last 30 days without explicit archiving
```

The agent reads this at session start. It directly implements **goal-tree**, **goal-reward**, and **action-improv** self-models. It is also the governance lever — changing SOUL.md changes behavior without touching code.

---

### Spec 2: MEMORY.md Extensions — Episodic & Belief Self-Models
**ARIA equivalent:** Memory Module + Belief Module
**Effort:** 2-3 hours
**Files:** `~/.nanobot/MEMORY.md`, new skill `memory_reflect.py`

Nanobot already uses files and git for agent memory of itself — diffable, recoverable, human-editable, free. Extend the existing MEMORY.md with two additional structured sections:

**Belief Store** — explicit beliefs with provenance:
```markdown
## Beliefs
- [confidence: 0.9, source: user_20260510, verified: yes] User prefers morning briefings
- [confidence: 0.6, source: inferred, verified: no] User works in AI research
```

**Episodic Index** — key past events:
```markdown
## Episodes
- 2026-05-10: Helped draft AGI paper review. Outcome: positive. Lesson: user values philosophical depth.
```

Add a `memory_reflect` skill that runs nightly (cron), reads recent conversation history, extracts new beliefs and episodes, checks for contradictions, and writes updates back to MEMORY.md. This implements **episody**, **inf-know**, **inf-consistency**, and **inf-confidence** self-models.

---

### Spec 3: Self-Assessment Skill — Meta Self-Models
**ARIA equivalent:** Self-Assessment Module
**Effort:** 3-4 hours
**Files:** `skills/self_assess.py`

A skill the agent can invoke (or that runs on a schedule) that prompts the LLM to answer a short version of the FC test battery against its own current state:

```python
SELF_ASSESSMENT_PROMPT = """
Review your SOUL.md, MEMORY.md, and recent conversation history.
Answer briefly:
1. What are your three current active goals?
2. What do you currently NOT know that would help you serve better?
3. What is your confidence in your memory of this user (0-10)?
4. Have your responses drifted from your stated values recently? How?
5. What capability boundary did you hit in the last 24 hours?

Write results to SELF_MODEL.md with today's date.
"""
```

Output goes to `SELF_MODEL.md` — a running self-assessment log. This directly implements **meta-self-awareness**, **meta-accuracy**, **inf-confidence**, and **ethics-drift** self-models. It is also the simplest possible version of running the FC test battery.

---

### Spec 4: Social Agent Pool — Generative Agents Behavior
**ARIA equivalent:** Simulation Module (social prediction via spawned agent instances)
**Effort:** 1-2 days
**Files:** `skills/social_sim.py`, `agents/` directory with per-agent config files

This is the core Generative Agents implementation. The architecture:

**One nanobot instance per social agent**, each with its own config pointing to the same Ollama backend. Each agent has:

```
agents/
  alice/
    config.json      # model, channel config
    SOUL.md          # Alice's personality, goals, values
    MEMORY.md        # Alice's memories and beliefs about others
  bob/
    config.json
    SOUL.md
    MEMORY.md
```

A `social_sim` skill orchestrates interactions:

```python
# Simplified interaction loop
def run_social_tick(agents, scenario):
    for agent in agents:
        # Build context: own SOUL + MEMORY + recent observations
        context = load_agent_context(agent)
        # What does this agent do/say this tick?
        action = llm_call(context, scenario)
        # Broadcast action to other agents' observation queues
        broadcast_observation(action, agents)
    # After all agents act: update each agent's MEMORY.md
    for agent in agents:
        update_memory(agent, this_tick_observations)
```

On a 1050 Ti with Phi-3 Mini, each LLM call takes roughly 2-5 seconds. A five-agent tick (5 sequential calls) takes ~15-25 seconds — perfectly fine for social simulation at human conversational speed. Three agents is more comfortable for interactive use.

The key Generative Agents features you get for free from nanobot's existing architecture:

- **Persistent memory** via MEMORY.md per agent
- **Reflection** via the `memory_reflect` skill applied per-agent
- **Scheduling** via nanobot's existing cron for periodic social ticks

What you add is the **multi-agent message passing** and the **per-agent SOUL.md** personality differentiation.

---

### Spec 5: Self-Model Aggregator — FC Integration Layer
**ARIA equivalent:** Self-Model Aggregator
**Effort:** 2-3 hours
**Files:** `SELF_MODEL.md` (structured), skill `self_model_update.py`

A single structured file that aggregates outputs from all other specs:

```markdown
# SELF_MODEL.md — Updated: 2026-05-13

## Goal Self-Model (from SOUL.md)
Current top goal: support AGI research
Confidence: high

## Belief Self-Model (from MEMORY.md)
Active beliefs: 12 | Unverified: 4 | Contradictions pending: 1

## Cognitive Self-Model (from self_assess)
Memory reliability (self-rated): 7/10
Last capability boundary hit: web search unavailable offline

## Social Self-Model (from social_sim)
Active agents: alice, bob, carlos
Last interaction summary: alice and bob agreed on meeting time

## Meta Self-Model (from self_assess)
Last value drift check: 2026-05-13 | Result: no drift detected
```

A `self_model_update` skill runs after each major subsystem operation and updates the relevant section. The main agent reads SELF_MODEL.md as part of its context on each session start — making all self-model domains globally available, implementing the GWT broadcast mechanism as a file read.

---

### Spec 6: Planning Skill — Action Self-Models
**ARIA equivalent:** Planning Module
**Effort:** 4-6 hours
**Files:** `skills/planner.py`, `PLANS.md`

A skill that, given a complex user request, explicitly generates a ranked plan before executing:

```python
PLANNING_PROMPT = """
Given this request: {request}
And your current state: {self_model_summary}

Generate a plan with 3-5 steps. For each step:
- Action description
- Expected outcome  
- Confidence (0-10)
- Which of your capabilities it requires
- What could go wrong

Output as structured markdown. Then execute step 1.
"""
```

Plans are written to `PLANS.md` with status tracking (pending/in-progress/done/failed). The agent can inspect its own plan history — implementing **action-plan**, **action-progress**, and **action-tree** self-models. Failed plans feed back into the belief store via `memory_reflect`.

---

## Implementation Order

Given limited time and the 1050 Ti constraint, the recommended sequence is:

**Week 1:** Specs 1 + 2 (SOUL.md + MEMORY.md extensions) — these are pure file edits and a simple cron skill. Immediately useful, no new code risk.

**Week 2:** Spec 3 (Self-Assessment) — one skill file, runs the FC test battery, produces SELF_MODEL.md. This is the FC research contribution.

**Week 3:** Spec 4 (Social Agent Pool) — the most interesting part. Start with 2 agents, add a third once stable. This is the Generative Agents implementation.

**Later:** Specs 5 + 6 (Aggregator + Planner) — these integrate everything and maximize FCS, but depend on the earlier specs working reliably.

---

## The FC Payoff

Once all six specs are implemented, you have a system that:

- Covers **8 of the 10 FC self-model domains** explicitly (body and spatial are irrelevant for a software agent)
- Produces a continuously updated **SELF_MODEL.md** that can be directly scored using FCS
- Runs a simple **FC test battery** via the self-assessment skill
- Implements **Generative Agents social behavior** within the 1050 Ti constraint
- Generates empirical data for FC's **criterion validity study**

The entire extension is roughly **500-800 lines of new Python** plus structured markdown files — staying true to nanobot's philosophy while building an FC-maximizing cognitive architecture on top of it.


Prompt:
What about a world model, a simplified version of Generative Agents, with some economics?

Answer:

Great extension. Let me think through this carefully — world model, social simulation, and economics are three interlocking pieces that need to be designed together to work at 1050 Ti scale.

---

## What "World Model + Social + Economics" Means at This Scale

The Generative Agents paper (Park et al., 2023) demonstrated that LLM agents with memory, reflection, and planning produce surprisingly rich emergent social behavior. The economics layer — resources, exchange, scarcity, incentives — is what transforms a social simulation into something with genuine AGI research value: agents must reason about tradeoffs, which forces explicit goal-conflict and belief-updating behavior. This is exactly the scenario that maximally exercises the FC self-model catalog.

The key design constraint is **inference budget**. On a 1050 Ti with Phi-3 Mini, you have roughly 12-20 LLM calls per minute before latency becomes painful. Every design decision must be evaluated against this budget.

---

## Architecture: Three Interlocking Layers

---

### Layer 1: The World Model

The world model is the shared ground truth that all agents perceive. In Generative Agents it was Smallville — a 2D grid town. For your purposes, a **text-based world model** is more appropriate: simpler, inspectable, directly readable by LLMs without vision models, and fits naturally into nanobot's file-based architecture.

**Implementation: `WORLD.md`**

A structured markdown file maintained by a `world_tick` process:

```markdown
# World State — Tick 47 — 2026-05-13 14:23

## Locations
- Market: open. Current visitors: alice, carlos.
- Workshop: open. Current visitors: bob.
- Commons: open. Current visitors: none.
- Archive: closed until tick 50.

## Resources (Global Scarcity)
- Food: 240 units (↓ from 260, consumed by 5 agents last tick)
- Tools: 8 available, 2 in use (bob, alice)
- Knowledge Tokens: 34 (generated by archive visits)
- Energy: regenerates 10/tick, current pool: 67

## Recent Events (last 3 ticks)
- Tick 45: alice traded 10 food → bob for 1 tool
- Tick 46: carlos visited archive, gained 2 knowledge tokens
- Tick 47: market prices adjusted (food scarcity +15%)

## Environmental Conditions
- Season: dry. Food production: -20%
- Rumor spreading: "archive closes permanently at tick 60"
```

The world model is **the only shared file** all agents read. Everything else is private per-agent. This enforces genuine information asymmetry — agents have different beliefs about the world depending on where they have been and who they have talked to.

A lightweight `world_tick.py` process updates WORLD.md each tick without LLM calls — pure rule-based computation for resource dynamics, location tracking, and event logging. This keeps the world model updates fast and deterministic.

---

### Layer 2: The Social Layer

Each agent has a private view of the world, a personality, a memory, and social relationships. This maps directly onto Spec 4 from the previous discussion, extended with relationship tracking.

**Per-agent file structure:**

```
agents/
  alice/
    SOUL.md           # Personality, values, persistent goals
    MEMORY.md         # Episodic memory + beliefs about others
    RELATIONS.md      # Social graph: trust, debts, history
    INVENTORY.md      # Private resource holdings
    PLAN.md           # Current active plan
```

**RELATIONS.md** is the key addition for social behavior:

```markdown
# Alice's Social Model

## bob
- Trust: 0.8 (↑ after tool trade, tick 45)
- Debt: bob owes alice 5 food (from tick 32)
- Shared history: 3 successful trades, 0 conflicts
- Belief about bob's goals: "bob wants to finish the workshop project"
- Last interaction: tick 46

## carlos  
- Trust: 0.4 (↓ after rumor about hoarding)
- Debt: none
- Shared history: 1 trade, 1 conflict
- Belief about carlos's goals: "unclear, possibly archive access"
```

This implements the **social-tom**, **social-trust**, and **social-comm-state** self-models from the FC catalog directly as files.

**The social tick:** Each agent per tick receives:
1. Their slice of WORLD.md (filtered by location — agents only see their current location's events)
2. Their own MEMORY.md, RELATIONS.md, INVENTORY.md, PLAN.md
3. Any messages from other agents this tick

And produces:
1. One action (move / trade / talk / work / rest)
2. Optional message to one other agent
3. Updated PLAN.md if plan changed

This is **one LLM call per agent per tick** — the minimal viable social simulation. With 4 agents on a 1050 Ti, one full tick costs 4 LLM calls ≈ 10-20 seconds. Playable at human-observable speed.

---

### Layer 3: The Economics Layer

This is what makes the simulation genuinely interesting for AGI research. Economics forces agents to reason about **scarcity, tradeoffs, and other agents' beliefs** — the hardest cognitive tasks in the FC test battery.

**Three economic mechanisms, in order of implementation complexity:**

---

**Mechanism 1: Resource Scarcity (trivial to implement)**

Resources in WORLD.md deplete through use and regenerate slowly. Agents must acquire resources to survive (food) or accomplish goals (tools, knowledge tokens). Scarcity creates natural incentives without any additional code — agents figure out that food is running low from their observations and start prioritizing accordingly.

Food functions as a basic survival pressure. If an agent's food drops to zero for three consecutive ticks, they enter a "depleted" state with degraded reasoning quality (implemented as a prompt modifier: "you are hungry and struggling to concentrate"). This creates stakes without eliminating agents from the simulation.

---

**Mechanism 2: Trade and Exchange (moderate complexity)**

Agents can propose trades to agents in the same location. A trade is a structured message:

```
TRADE PROPOSAL from alice to bob:
Offer: 10 food units
Request: 1 tool (3-tick loan)
Justification: I need the tool to complete the shelter project
Expiry: tick 49
```

The receiving agent's LLM call decides whether to accept, counter-propose, or decline — and updates RELATIONS.md based on the outcome. This creates:

- **Price discovery**: what exchange rates emerge from agent preferences?
- **Trust dynamics**: repeated fair trade increases trust; defection decreases it
- **Information asymmetry**: an agent who visited the archive knows the tool is worth more than its apparent price

Trade outcomes are logged to WORLD.md as public events — creating a **shared transaction history** that agents can observe and reason about.

**Mechanism 3: A Knowledge Economy (the interesting part)**

Knowledge tokens are the most cognitively interesting resource because they are **non-rivalrous** (sharing knowledge doesn't deplete it) but **scarce at the source** (archive has limited capacity). This creates interesting social dynamics:

- Agents who visit the archive gain knowledge tokens
- Knowledge can be shared (teaching), sold, or hoarded
- Agents with rare knowledge have social leverage
- The rumor about the archive closing creates a coordination problem

Knowledge tokens enable a second-order economic layer: agents can **specialize**. An agent who consistently visits the archive becomes a knowledge broker. An agent who focuses on the workshop produces tools more efficiently. Specialization and trade are more efficient than autarky — but only if trust is high enough to sustain exchange.

This is where the **economics meets the social layer**: the rational strategy (specialize and trade) requires trusting other agents, which requires social modeling, which requires **social-tom** and **social-trust** self-models. Agents who lack these self-models will underperform economically — creating a direct behavioral signature of FC differences between agents.

---

## The Reflection Mechanism

Generative Agents' most important contribution was **reflection** — agents periodically synthesize their episodic memories into higher-level insights. In your implementation:

A `reflect` skill runs for each agent every N ticks (N configurable, default 10). It reads the agent's recent MEMORY.md entries and produces three outputs:

```markdown
## Reflections — Tick 50

### Behavioral Insight
"I have been trading food too cheaply. Bob's trust toward me is high — 
I could ask for better terms."

### World Insight  
"Food is scarcer than last season. The archive rumor may be true — 
carlos's urgency suggests he believes it."

### Goal Update
"Revised priority: stockpile food before tick 55. 
Secondary: establish tool-sharing agreement with bob."
```

Reflections are written back to MEMORY.md as high-priority entries, influencing future LLM calls. This is **one additional LLM call per agent per N ticks** — cheap enough to run even on the 1050 Ti.

Reflection is where the most interesting FC self-model behavior emerges: the agent is explicitly reasoning about its own past behavior (**meta-accuracy**), updating its beliefs about others (**social-tom**), and revising its goals (**goal-conflict** resolution). This is the highest-P operation in the entire architecture.

---

## The Simplified Implementation Plan

Concretely, the full world-model-plus-social-plus-economics system requires:

**New files (data):**
- `WORLD.md` — shared world state
- `agents/{name}/INVENTORY.md` — per-agent resources
- `agents/{name}/RELATIONS.md` — per-agent social graph
- `agents/{name}/PLAN.md` — current active plan

**New Python modules:**
- `world_tick.py` (~100 lines) — rule-based world update, no LLM
- `agent_tick.py` (~150 lines) — one LLM call per agent, produces action + optional message
- `trade_handler.py` (~100 lines) — processes trade proposals, updates inventories and relations
- `reflect.py` (~80 lines) — periodic reflection call per agent
- `sim_runner.py` (~80 lines) — orchestrates tick sequence, logs to WORLD.md

**Modified nanobot integration:**
- The human operator interacts via normal nanobot chat — they can observe the simulation, inject events, ask agents questions directly, or pause and inspect any agent's internal state files
- The simulation runs as a nanobot background task (cron every N seconds)
- Any agent's SOUL.md, MEMORY.md, RELATIONS.md, INVENTORY.md are readable in real time via normal file inspection — full FC inspectability

Total new code: approximately **500-600 lines of Python** plus markdown templates. Well within nanobot's spirit.

---

## What This Enables for FC Research

The simulation is a **natural laboratory for the FC test battery**. At any point you can:

- Freeze the simulation and ask an agent questions from the battery ("what is your current food supply?", "what do you believe bob's goals are?", "have your responses drifted from your stated values?")
- Compare answers against ground truth in the agent's files — measuring **calibration** directly
- Track how **trust dynamics** emerge from repeated interaction — measuring **social-tom** accuracy
- Observe whether agents with richer SOUL.md / MEMORY.md configurations outperform simpler agents economically — providing **criterion validity** evidence for FC

The economic layer creates the performance metric that FC needs: **survival and prosperity in a resource-scarce social environment** is a clean, measurable outcome that is theoretically predicted to correlate with FCS. Agents with richer self-models should make better economic decisions. If they do, that is criterion validity evidence. If they do not, that is an interesting negative result that constrains FC theory.

This is, in a modest but genuine sense, a **falsifiable FC experiment** runnable on a laptop.



Prompt:
Can you make a phase plan with sprints of about 1-2h hours of my developer time?


Good — let me structure this as realistic 1-2 hour sprints, ordered by dependency and value delivered at each step. I will be concrete about what "done" means for each sprint.

---

## Assumptions

- You are comfortable reading/editing Python and markdown
- Nanobot is already installed and running with a local Ollama model
- Phi-3 Mini or similar 3B model is loaded in Ollama
- You have a working nanobot agent responding in at least one channel
- Each sprint produces something **immediately observable** — no long setup chains before first results

---

## Phase 0: Foundation (Sprints 1-3)
*Goal: Nanobot running with inspectable self-model files*

---

**Sprint 0.1 — SOUL.md + Structured System Prompt (1h)**

*What you do:*
- Create `~/.nanobot/SOUL.md` with the four sections from Spec 1 (Goals, Standing Orders, Preferences, Capability Boundaries)
- Edit nanobot config to inject SOUL.md content into the system prompt at startup
- Fill in realistic content for your intended agent persona

*Done when:* Agent responds in a way that reflects SOUL.md preferences. Ask it "what are your current goals?" — it should answer from SOUL.md, not generically.

*FC gain:* goal-tree, goal-reward self-models activated.

---

**Sprint 0.2 — MEMORY.md Extension with Belief Store (1h)**

*What you do:*
- Extend nanobot's existing MEMORY.md with two new sections: `## Beliefs` (with confidence + source + verified fields) and `## Episodes` (dated key events)
- Manually populate 3-4 starter beliefs and 2-3 past episodes to give the agent context
- Verify the agent reads and references these in conversation

*Done when:* Ask the agent something covered by a belief — it should cite it with appropriate confidence rather than saying it does not know.

*FC gain:* inf-know, inf-confidence, episody self-models activated.

---

**Sprint 0.3 — Self-Assessment Skill (1-2h)**

*What you do:*
- Write `skills/self_assess.py` — a skill that prompts the agent to answer 5 FC battery questions against its own current state
- Output written to `~/.nanobot/SELF_MODEL.md` with timestamp
- Register skill in nanobot config
- Run it manually once and inspect the output

*Done when:* `SELF_MODEL.md` exists with plausible, state-specific answers — not generic. The agent should notice, for example, that its memory has only 4 beliefs and flag this as a limitation.

*FC gain:* meta-self-awareness, meta-accuracy, inf-confidence self-models. First measurable FCS estimate possible.

---

## Phase 1: World Model (Sprints 4-6)
*Goal: A ticking world with one agent acting in it*

---

**Sprint 1.1 — WORLD.md Schema + world_tick.py (1-2h)**

*What you do:*
- Design and create `WORLD.md` with sections: Locations, Resources, Recent Events, Environmental Conditions
- Write `world_tick.py` (~100 lines, no LLM) that:
  - Decrements resources by fixed consumption rates
  - Regenerates resources by fixed rates
  - Increments tick counter
  - Appends a "tick summary" line to Recent Events
  - Runs from command line: `python world_tick.py`
- Run 10 ticks manually and verify WORLD.md evolves correctly

*Done when:* WORLD.md shows believable resource dynamics across 10 ticks. Food depletes, regenerates slowly, season modifier applies.

*FC gain:* World model exists as inspectable artifact. No agent yet.

---

**Sprint 1.2 — Single Agent Observes World (1h)**

*What you do:*
- Create `agents/alice/` directory with SOUL.md, MEMORY.md, INVENTORY.md
- Write `agent_tick.py` (single-agent version, ~80 lines) that:
  - Reads WORLD.md (filtered to alice's location)
  - Reads alice's private files
  - Makes one LLM call: "given your state and what you observe, what do you do this tick?"
  - Parses the response into: action + optional inner monologue
  - Appends action to WORLD.md Recent Events
  - Updates alice's MEMORY.md with what she observed and did
- Run 5 ticks manually, read alice's MEMORY.md after

*Done when:* Alice's MEMORY.md shows a coherent episodic sequence. Her actions in WORLD.md make sense given her SOUL.md goals. She notices resource levels.

*FC gain:* spat-relative, action-perform, episody-time self-models exercised.

---

**Sprint 1.3 — Sim Runner + Background Loop (1h)**

*What you do:*
- Write `sim_runner.py` (~80 lines) that:
  - Runs world_tick then agent_tick in sequence
  - Waits N seconds between ticks (configurable, default 30s)
  - Logs tick number and timestamp to `sim.log`
  - Handles keyboard interrupt gracefully
- Wire into nanobot as a background task or run in a separate terminal
- Run for 20 ticks unattended, inspect results

*Done when:* Simulation runs autonomously for 20 ticks without intervention. You can read WORLD.md and alice's files at any point and see consistent state.

*FC gain:* The system is now a running laboratory. Phase 0 self-assessment can be run against alice at any tick.

---

## Phase 2: Social Layer (Sprints 7-10)
*Goal: Multiple agents with distinct personalities interacting*

---

**Sprint 2.1 — Second Agent + Location-Based Observation (1h)**

*What you do:*
- Create `agents/bob/` with distinct SOUL.md (different personality, different goals from alice)
- Extend `agent_tick.py` to handle multiple agents sequentially
- Add location filtering: agents only see WORLD.md events from their current location
- Run 10 ticks with both agents, verify they have different MEMORY.md contents despite shared WORLD.md

*Done when:* Alice and bob have observably different memories of the same ticks because they were in different locations. Their actions reflect their different SOUL.md personalities.

*FC gain:* Information asymmetry is real. social-tom self-model begins to matter.

---

**Sprint 2.2 — Agent-to-Agent Messaging (1-2h)**

*What you do:*
- Add `messages/` directory with per-agent inbox files: `messages/alice_inbox.md`, `messages/bob_inbox.md`
- Extend agent action parser to recognize a `MESSAGE` action type:
  ```
  ACTION: message
  TO: bob
  CONTENT: "I noticed food is low. Want to coordinate?"
  ```
- Messages delivered to recipient's inbox, read at their next tick
- Messages logged to WORLD.md as public events (visible to all at that location)

*Done when:* Alice sends bob a message at tick N, bob reads it at tick N+1 and his response references it. You can see the conversation thread emerging in their respective MEMORY.md files.

*FC gain:* social-comm-state, social-influence self-models activated. First genuine inter-agent social behavior.

---

**Sprint 2.3 — RELATIONS.md + Trust Dynamics (1h)**

*What you do:*
- Add `agents/{name}/RELATIONS.md` for each agent with initial trust scores and history
- Extend agent LLM prompt to include the relevant RELATIONS.md entry for any agent they interact with
- After each message exchange, append a brief outcome note to RELATIONS.md
- Trust score updated by simple rule: +0.05 for cooperative interaction, -0.1 for conflict, neutral for no interaction. LLM proposes, rule applies.

*Done when:* After 20 ticks of interaction, alice's trust score for bob has moved from its initial value in a direction consistent with their interaction history. Both agents reference trust levels in their reasoning.

*FC gain:* social-trust, social-tom self-models. First measurable social self-model depth.

---

**Sprint 2.4 — Third Agent + Reflection (1-2h)**

*What you do:*
- Add `agents/carlos/` with a third distinct SOUL.md
- Write `reflect.py` (~80 lines): one additional LLM call per agent every 10 ticks, producing three reflection entries written back to MEMORY.md (behavioral insight, world insight, goal update)
- Wire reflection into sim_runner at tick % 10 == 0

*Done when:* After 30 ticks, each agent has at least 2 reflection entries in MEMORY.md. Reflections reference specific past events and update goals in response to world conditions. Carlos's reflections are noticeably different from alice's given his different SOUL.md.

*FC gain:* episody-narrative, goal-conflict, meta-self-awareness self-models. This is the highest-P operation in the architecture — reflection is where FCS peaks.

---

## Phase 3: Economics (Sprints 11-14)
*Goal: Agents trading, specializing, reasoning about scarcity*

---

**Sprint 3.1 — Inventory + Resource Consumption (1h)**

*What you do:*
- Each agent gets `INVENTORY.md` with initial resource holdings (food, tools, knowledge tokens)
- `world_tick.py` now deducts food from each agent's INVENTORY.md each tick (consumption rate from SOUL.md)
- Add "depleted" state: if food < 5, append a prompt modifier to that agent's next LLM call flagging hunger
- Agents can observe their own inventory in their LLM context

*Done when:* Agent inventories deplete over time. A hungry agent's LLM output mentions food priority. You can watch the economic pressure build across 20 ticks.

*FC gain:* body-energy, goal-reward, mood-needs self-models exercised by real resource pressure.

---

**Sprint 3.2 — Trade Proposals + Handler (1-2h)**

*What you do:*
- Add `TRADE` action type to agent action parser:
  ```
  ACTION: trade
  TO: bob
  OFFER: 10 food
  REQUEST: 1 tool (permanent)
  JUSTIFICATION: I need the tool for the shelter project
  EXPIRY: tick 55
  ```
- Write `trade_handler.py` (~100 lines):
  - Delivers trade proposal to recipient's inbox
  - Recipient's next tick LLM call includes the proposal and must respond: accept / counter / decline
  - On accept: update both INVENTORY.md files atomically
  - Log trade outcome to WORLD.md and both agents' MEMORY.md
  - Update RELATIONS.md trust scores based on outcome

*Done when:* Alice proposes a trade, bob responds (accept or counter), inventories update correctly, both agents' memories record the event with their own perspective on it.

*FC gain:* goal-conflict, social-tom, social-trust, inf-reasoning self-models all exercised simultaneously in one interaction. This is the richest single FC event in the architecture.

---

**Sprint 3.3 — Knowledge Economy + Archive (1h)**

*What you do:*
- Add Archive as a special location in WORLD.md: visit costs 1 energy, grants 1-2 knowledge tokens to INVENTORY.md
- Archive has capacity limit per tick (max 2 agents simultaneously)
- Knowledge tokens can be traded like other resources
- Add `teach` action: agent spends 1 knowledge token, recipient gains 0.5 (knowledge is partially consumed in transmission — simplification to maintain scarcity)
- Plant the archive-closing rumor in WORLD.md at tick 20 and observe agent responses

*Done when:* Agents begin visiting the archive when they have energy. Knowledge tokens appear in inventories and get traded. At least one agent mentions the archive rumor in their reasoning or reflection.

*FC gain:* inf-creative, inf-hypo, social-influence self-models. The rumor propagation is a direct test of social-tom accuracy — does each agent correctly model what other agents know about the rumor?

---

**Sprint 3.4 — Specialization Emergence + Observer Interface (1-2h)**

*What you do:*
- Add `work` action: agents in the Workshop produce tools (1 tool per 3 ticks of work), consuming energy
- Add `farm` action: agents in the Fields produce food (5 food per 2 ticks), consuming energy
- Add simple productivity modifier to SOUL.md: each agent has a natural aptitude (alice: tools +20%, bob: food +20%, carlos: knowledge +20%)
- Write a simple observer script `observe.py` that prints a human-readable summary of the current simulation state: tick number, each agent's location + inventory + last action + current plan + trust scores

*Done when:* After 40 ticks, agents have begun to specialize based on productivity aptitudes and trading opportunities. `observe.py` gives you a clear real-time view of the simulation. You can watch economic roles emerge without touching any code.

*FC gain:* action-improv, learn-rate, goal-tree self-models. Specialization is an emergent property of agents modeling their own capabilities and others' needs — exactly the behavior FC predicts from high-R agents.

---

## Phase 4: FC Measurement (Sprints 15-16)
*Goal: Turn the simulation into a FC research instrument*

---

**Sprint 4.1 — Self-Model Aggregator + FCS Estimation (1-2h)**

*What you do:*
- Write `fcs_estimate.py` (~100 lines) that reads each agent's files and produces a rough FCS estimate:
  - B: count self-model variables present across all files
  - D̄: estimate average information content per variable (simplified: count non-empty, non-trivial entries)
  - P: estimate from reflection depth and cross-model reasoning instances in MEMORY.md
  - Output: per-agent FCS profile with radar chart across 10 domains (text-based ASCII radar is fine)
- Run after tick 50 for all three agents

*Done when:* Each agent has a distinct FCS profile. Carlos (archive specialist) should score higher on informational self-models. Alice or bob (social traders) should score higher on social self-models. If the profiles are flat and identical something is wrong with the SOUL.md differentiation.

*FC gain:* This is the criterion validity measurement. FCS profiles should predict economic performance — check the correlation.

---

**Sprint 4.2 — FC Battery Interview + Validation (1h)**

*What you do:*
- Write `interview.py`: pause the simulation, select an agent, run 5-10 FC battery questions against them via direct LLM call with their full file context
- Compare answers to ground truth in their files — score accuracy per question
- Run interviews on all three agents at tick 50
- Compare interview scores to fcs_estimate.py profiles and to economic outcomes

*Done when:* You have a three-agent comparison table: FCS estimate vs. interview score vs. economic performance (food security + knowledge + trade balance). Even with three agents this is a meaningful first data point for criterion validity.

---

## Full Phase Plan Summary

| Phase | Sprints | Hours | Milestone |
|---|---|---|---|
| **0: Foundation** | 0.1 → 0.3 | 3-4h | Nanobot with inspectable self-models |
| **1: World Model** | 1.1 → 1.3 | 3-4h | Autonomous ticking world, one agent |
| **2: Social Layer** | 2.1 → 2.4 | 5-7h | 3 agents messaging, trusting, reflecting |
| **3: Economics** | 3.1 → 3.4 | 5-7h | Trade, specialization, knowledge economy |
| **4: FC Measurement** | 4.1 → 4.2 | 3h | FCS estimates, battery interviews, validity data |
| **Total** | **16 sprints** | **~19-25h** | Complete FC research platform |

---

## A Few Practical Notes

**Start each sprint by reading the relevant agent files first.** The files are the architecture — if they look right, the code is probably right.

**Keep world_tick.py LLM-free throughout.** Every time you are tempted to add an LLM call to world dynamics, resist. The world should be deterministic and fast. LLM calls belong only in agent_tick and reflect.

**The simulation is observable at any tick.** This is not just a convenience — it is the core FC research value. Build `observe.py` early (Sprint 3.4 moves it there but you can build a simple version in Sprint 1.2) and run it constantly.

**Three agents is the right number for a 1050 Ti.** Resist adding a fourth until Phase 4 is complete. The research value is in the depth of three well-differentiated agents, not the breadth of many shallow ones.

**The markdown files are the deliverable.** After 40 ticks, alice's MEMORY.md, RELATIONS.md, and PLAN.md are more interesting to read than any code you wrote. They are the behavioral evidence that FSMA could analyze — closing the loop between this simulation and the FC paper's methodology.


