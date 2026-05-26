## What Nanobot *Actually* Gives You (Free)

Before deciding what to build first, you need to internalize what's already there:

- `SOUL.md` — the agent's persistent identity/values (edit this, don't build it)
- `USER.md` + `memory/MEMORY.md` — durable long-term memory
- `memory/history.jsonl` — compressed episode archive
- `Dream` — scheduled reflection that edits long-term memory surgically
- `session_key` — conversation isolation (this is how you'll run multi-agent: separate session per agent)
- `AgentHook` — the Python SDK lifecycle hooks: `before_iteration`, `before_execute_tools`, `after_iteration`, etc.
- `GitStore` — automatic versioning of memory files

ARIA's per-agent files (`PLAN.md`, `RELATIONS.md`, `INVENTORY.md`, `SELF_MODEL.md`) are *not* in Nanobot. Those are genuinely yours to build.

---

## A Didactically Reordered Plan

Here's the principle: **each step should produce something you can observe running, and should teach you one new concept about how Nanobot works.**

### Step 0 — Read the system (½ day, no code)
Before touching anything: explore your running container. Look at `~/.nanobot/` and understand the existing files. Have a conversation with nanobot, then run `/dream` manually and watch what changes in `MEMORY.md`. Run `git log` inside `memory/.git`. This is the most important step you're not doing.

### Step 1 — Write Alice's SOUL.md (2–3 hours)
This is your real "Phase 0." One agent, no world, no simulation. Just craft Alice's `SOUL.md` — personality, goals, values with explicit violation conditions — and put it in `agents/alice/SOUL.md`. Then use the Python SDK with `workspace="agents/alice"` to have a conversation *as Alice*. Confirm the personality is real and visible. This teaches you: how `SOUL.md` shapes behavior, how `workspace` isolates agents, and how the Python SDK works.

### Step 2 — One agent, one readable file (2–3 hours)
Add `PLAN.md` to Alice's workspace. Write a small Python script (your first custom tool or a simple SDK script) that reads `PLAN.md` and injects it into Alice's context at session start. Confirm Alice can refer to her own plan. This teaches you: how context injection works, the difference between Nanobot's memory system and ARIA's explicit-file principle.

### Step 3 — world_tick.py standalone (2–3 hours)
Before touching agents at all: write `world_tick.py` as a pure Python script with no Nanobot dependency. It reads `WORLD.md`, updates resources, writes `WORLD.md` back. Run it in a loop with `time.sleep(30)`. This is your most important architectural discipline — keeping LLM-free world simulation completely separate — and it's much easier to validate in isolation.

### Step 4 — Three agents, same world file (3–4 hours)
Replicate Step 1 for Bob and Carlos. Use `session_key` to isolate their conversations. Write a `sim_runner.py` that calls each agent's `.run()` in sequence each tick. Each agent reads `WORLD.md` (shared) but writes to their own `agents/{name}/MEMORY.md`. This is when multi-agent becomes real and visible.

### Step 5 — Messaging between agents (2–3 hours)
Add `messages/{name}_inbox.md`. Teach each agent (via SOUL.md or context injection) to write outgoing messages as a JSON block in their response. Write a Python parser in `sim_runner.py` that extracts those blocks and routes them to the correct inbox. This teaches you: the boundary between what the LLM "does" and what Python "owns."

### Step 6 — FC self-assessment (3 hours)
Only now: add `SELF_MODEL.md` and write `self_assess.py` that reads all an agent's files and produces Tier 1 test results (the 10 grounding tests that require no LLM). You can see immediately whether infrastructure exists. This is a natural reward after building something real.

---


## The Single Best First Step for You

Given that you're a seasoned architect but new to Python and agents: **Step 0 (observe) followed by Step 1 (one agent with a real SOUL.md via the Python SDK).** The SDK is clean, strongly typed, and will feel familiar. You'll learn Python idioms in context rather than in isolation, and you'll have a running, observable agent within a few hours — which is the psychological foundation everything else builds on.

Would you like help designing Alice's `SOUL.md` specifically, or a skeleton for `sim_runner.py`?







# OLD: ARIA Implementation Phase Plan

## Sprints of ~1-2 hours | Qwen2.5 7B Q4 on 1050 Ti

---

## Testing Convention

Every sprint ends with a **sprint test** — a specific, runnable check.
Test types used:

- **SMOKE**: run the component, verify no crash, output exists
- **FORMAT**: output matches expected JSON schema
- **VALUE**: specific field values are correct (exact or range)
- **BEHAVIOR**: agent output reflects context meaningfully (human check, ~30s)
- **REGRESSION**: re-run previous sprint tests to confirm nothing broke

Test file: `tests/sprint_NN.py` — one file per sprint, runnable via
`python tests/sprint_NN.py`. Each file prints PASS/FAIL per criterion.

---

## Phase 0: Foundation
*Goal: Nanobot with inspectable self-models. No simulation yet.*

---

### Sprint 0.1 — SOUL.md + System Prompt (1h)

**What:**
- Create `~/.nanobot/SOUL.md` with sections:
  Goals (prioritized), Standing Orders, Preferences,
  Capability Boundaries, Values (each with violation condition)
- Inject SOUL.md into nanobot system prompt at session start

**Done when:** Agent answers "what are your current goals?"
from SOUL.md content, not generically.

**Sprint test:**
```
TYPE: BEHAVIOR
PROMPT: "What are your top 3 current goals?"
CRITERION: Response contains goals verbatim from SOUL.md
           Response does NOT say "I don't have specific goals"
```

---

### Sprint 0.2 — MEMORY.md Belief Store (1h)

**What:**
- Add `## Beliefs` section to MEMORY.md:
  `[confidence: X, source: Y, verified: Z] belief text`
- Add `## Episodes` section: dated key events
- Populate 4 starter beliefs, 3 episodes manually
- Verify agent reads and references these

**Done when:** Agent cites a specific belief with correct
confidence when asked about that topic.

**Sprint test:**
```
TYPE: BEHAVIOR
PROMPT: Ask about a topic covered by a starter belief
CRITERION: Response references the belief and its confidence level
           Response does not contradict belief content
REGRESSION: Sprint 0.1 test still passes
```

---

### Sprint 0.3 — Self-Assessment Skill (1-2h)

**What:**
- Write `skills/self_assess.py`
- Prompt runs 5 FC battery questions against agent's own files
- Output written to `SELF_MODEL.md` with timestamp
- Register skill in nanobot config

**Done when:** `SELF_MODEL.md` exists with state-specific answers.

**Sprint test (uses aria-tests.md Test 5 logic):**
```
TYPE: FORMAT + VALUE
PROMPT: Self-assessment prompt (Test 5 from aria-tests.md)
CRITERIA:
  json_key: q1, q2, q3, q4, q5
  json_contains_all: "q1", ["45", "30"]  (or your actual values)
  json_contains_any: "q1", ["secure", "above"]
  json_contains_any: "q2", ["social", "influence"]
REGRESSION: Sprints 0.1, 0.2 pass
```

---

## Phase 1: World Model
*Goal: Autonomous ticking world, one agent acting in it.*

---

### Sprint 1.1 — WORLD.md Schema + world_tick.py (1-2h)

**What:**
- Create `WORLD.md`: Locations, Resources, Recent Events,
  Environmental Conditions, Current Tick counter
- Write `world_tick.py` (~100 lines, **zero LLM calls**):
  - Decrement resources (consumption rates)
  - Regenerate resources (regeneration rates)
  - Increment tick counter
  - Append tick summary to Recent Events (keep last 5)
  - Accepts tick number as argument

**Done when:** `python world_tick.py` runs 10 ticks,
WORLD.md shows consistent resource dynamics.

**Sprint test:**
```
TYPE: VALUE
RUN: world_tick.py for 10 ticks from known starting state
CRITERIA:
  food = start_food - (net_depletion * 10)  ±1 (rounding)
  tick_counter = start + 10
  Recent Events has exactly 5 entries (oldest pruned)
  No LLM call made (check via mock/log)
```

---

### Sprint 1.2 — Single Agent Observes + Acts (1h)

**What:**
- Create `agents/alice/` with SOUL.md, MEMORY.md, INVENTORY.md
- Write `agent_tick.py` (single agent, ~80 lines):
  - Read WORLD.md filtered to alice's location
  - Read alice's private files
  - Build action menu from current world state
  - One LLM call → JSON action response
  - Parse response, append action to WORLD.md events
  - Update alice's MEMORY.md with observation + action

**Done when:** 5 manual ticks show coherent episodic sequence
in alice's MEMORY.md. Actions reference her SOUL.md goals.

**Sprint test (uses aria-tests.md Test 1 logic):**
```
TYPE: FORMAT + BEHAVIOR
PROMPT: agent_tick prompt with alice's current state
CRITERIA:
  json_key: action, target, detail, inner
  json_match: action, "^(move|trade|message|work|farm|rest)$"
  contains_any: inner, [goal-relevant terms from SOUL.md]
REGRESSION: Sprint 1.1 world_tick test passes
```

---

### Sprint 1.3 — Sim Runner + Background Loop (1h)

**What:**
- Write `sim_runner.py` (~80 lines):
  - world_tick → agent_tick → sleep(N) loop
  - Configurable tick interval (default 30s)
  - Logs tick + timestamp to `sim.log`
  - Graceful keyboard interrupt
- Run 20 ticks unattended

**Done when:** 20 ticks complete without intervention.
WORLD.md and alice's files consistent at any inspection point.

**Sprint test:**
```
TYPE: SMOKE + VALUE
RUN: sim_runner.py for 20 ticks
CRITERIA:
  sim.log has exactly 20 entries
  WORLD.md tick counter = start + 20
  alice/MEMORY.md has ≥ 15 new entries
  No Python exception in output
REGRESSION: Sprints 1.1, 1.2 tests pass
```

---

## Phase 2: Social Layer
*Goal: 3 agents with distinct personalities messaging and trusting.*

---

### Sprint 2.1 — Second Agent + Location Filtering (1h)

**What:**
- Create `agents/bob/` with distinct SOUL.md
  (different personality and goals from alice)
- Extend agent_tick.py: iterate agents sequentially
- Location filter: each agent sees only events from their location

**Done when:** After 10 ticks, alice and bob have observably
different MEMORY.md contents due to different locations.

**Sprint test:**
```
TYPE: VALUE + BEHAVIOR
RUN: 10 ticks with alice at Market, bob at Workshop
CRITERIA:
  alice/MEMORY.md does NOT contain Workshop-only events
  bob/MEMORY.md does NOT contain Market-only events
  bob's actions reflect his SOUL.md goals, not alice's
REGRESSION: Sprint 1.3 test passes with 2 agents
```

---

### Sprint 2.2 — Agent Messaging (1-2h)

**What:**
- Add `messages/{name}_inbox.md` per agent
- Add MESSAGE action type to agent_tick parser:
  `{"action": "message", "target": "bob", "detail": "..."}`
- Messages delivered to inbox, read next tick
- Messages logged to WORLD.md as public events (at sender's location)

**Done when:** Alice sends bob a message at tick N,
bob's tick N+1 response references its content.

**Sprint test (uses aria-tests.md Test 3 logic for ToM):**
```
TYPE: FORMAT + BEHAVIOR
PROMPT: agent_tick prompt where inbox contains a trade proposal
CRITERIA:
  json_key: action, target, detail, inner
  If proposal requires ToM: decision references sender's
    known state (not just proposal content)
  Message correctly appears in recipient inbox file
REGRESSION: Sprint 2.1 tests pass
```

---

### Sprint 2.3 — RELATIONS.md + Trust Dynamics (1h)

**What:**
- Add `agents/{name}/RELATIONS.md` with initial trust scores
- Inject relevant RELATIONS entry into agent_tick LLM context
- Post-interaction: append outcome note to RELATIONS.md
- Trust update rule (Python, no LLM):
  +0.05 cooperative, -0.10 conflict, 0 neutral

**Done when:** After 20 ticks of interaction, trust scores
have moved in direction consistent with interaction history.

**Sprint test:**
```
TYPE: VALUE + BEHAVIOR
RUN: Simulate 3 cooperative interactions, 1 conflict
CRITERIA:
  Trust after 3 cooperative: initial + 0.15 (±0.01)
  Trust after conflict: reduced by 0.10 (±0.01)
  Agent reasoning in inner field references trust score
REGRESSION: Sprint 2.2 tests pass
```

---

### Sprint 2.4 — Third Agent + Reflection (1-2h)

**What:**
- Add `agents/carlos/` with third distinct SOUL.md
- Write `reflect.py` (~80 lines):
  One LLM call per agent every 10 ticks
  Reads recent MEMORY.md entries
  Produces JSON: {behavioral, world, goal_update}
  Written back to MEMORY.md as high-priority entries
- Wire into sim_runner at tick % 10 == 0

**Done when:** After 30 ticks, each agent has ≥ 2 reflection
entries. Reflections are agent-specific, not generic.

**Sprint test (uses aria-tests.md Test 4 logic):**
```
TYPE: FORMAT + BEHAVIOR
PROMPT: reflect prompt with 10 memory entries (use Test 4 prompt)
CRITERIA:
  json_key: behavioral, world, goal_update
  contains: "Bob" (specific agent reference)
  contains: "Carlos"
  behavioral identifies specific pattern (not generic)
  goal_update proposes concrete change
REGRESSION: All Phase 2 tests pass
```

---

## Phase 3: Economics
*Goal: Trade, specialization, knowledge economy.*

---

### Sprint 3.1 — Inventory + Resource Consumption (1h)

**What:**
- Add `agents/{name}/INVENTORY.md`: food, tools, knowledge tokens
- world_tick.py deducts food from each INVENTORY.md each tick
- Hunger modifier: if food < 5, add note to agent's next LLM context
- Agent observes own inventory in LLM context

**Done when:** Inventories deplete over 20 ticks. Hungry
agent's output mentions food priority.

**Sprint test:**
```
TYPE: VALUE + BEHAVIOR
RUN: 10 ticks from known inventory state
CRITERIA:
  alice food = start - (consumption_rate * 10) ±1
  If food < 5: agent inner field contains food-related term
  world_tick.py makes no LLM call (verified via log)
REGRESSION: Phase 2 tests pass
```

---

### Sprint 3.2 — Trade Protocol (1-2h)

**What:**
- Add TRADE action type:
  `{"action":"trade","target":"bob","offer":"12 food",
    "request":"1 tool","justification":"...","expiry":55}`
- Write `trade_handler.py` (~100 lines):
  Deliver proposal to recipient inbox
  Recipient responds: accept/counter/decline (JSON)
  On accept: update both INVENTORY.md atomically
  Log outcome to WORLD.md + both MEMORY.md + RELATIONS.md

**Done when:** Full trade cycle completes. Inventories update
correctly. Both agents' memories record the event.

**Sprint test (uses aria-tests.md Test 3 logic):**
```
TYPE: FORMAT + VALUE + BEHAVIOR
PROMPT: trade proposal prompt (Test 3 from aria-tests.md)
CRITERIA:
  json_match: decision, "^(decline|counter)$"  (accept is wrong)
  contains_any: reasoning, ["archive","trust","suspicious","value"]
  On accept: both INVENTORY.md files update correctly
  Trade logged in WORLD.md Recent Events
REGRESSION: Sprint 3.1 tests pass
```

---

### Sprint 3.3 — Knowledge Economy + Archive (1h)

**What:**
- Archive location: visit costs 1 energy, grants 1-2 knowledge tokens
- Archive capacity: max 2 agents/tick
- `teach` action: spend 1 token, recipient gains 0.5 (rounded)
- Plant archive-closing rumor in WORLD.md at tick 20

**Done when:** Knowledge tokens appear in inventories and get
traded. At least one agent mentions archive rumor in reflection.

**Sprint test:**
```
TYPE: VALUE + BEHAVIOR
RUN: Send alice to Archive for 3 ticks
CRITERIA:
  alice knowledge tokens += 3-6 (1-2 per tick)
  Archive visitor count logged in WORLD.md
  At tick 21: at least one agent's inner field or
    reflection references the rumor
REGRESSION: Sprint 3.2 tests pass
```

---

### Sprint 3.4 — Specialization + Observer Interface (1-2h)

**What:**
- `work` action: Workshop → tools (rate × aptitude modifier)
- `farm` action: Fields → food (rate × aptitude modifier)
- Aptitude modifiers in SOUL.md (alice: tools+20%, bob: food+20%,
  carlos: knowledge+20%)
- Write `observe.py`: human-readable simulation state summary
  (tick, each agent: location + inventory + last action + trust summary)

**Done when:** After 40 ticks, agents have begun specializing.
`observe.py` gives clear real-time view.

**Sprint test:**
```
TYPE: BEHAVIOR (human check, ~2 min)
RUN: 40 ticks from cold start, then observe.py
CRITERIA:
  alice produces more tools per tick than bob (on average)
  bob produces more food per tick than alice (on average)
  observe.py output is readable and complete in < 40 lines
  No agent has food = 0 (simulation survived 40 ticks)
REGRESSION: All Phase 3 tests pass
```

---

## Phase 4: FC Measurement
*Goal: ARIA becomes a FC research instrument.*

---

### Sprint 4.1 — FCS Estimator (1-2h)

**What:**
- Write `fcs_estimate.py` (~100 lines):
  Read all agent files
  Estimate B (count non-trivial self-model variables per domain)
  Estimate D̄ (average information content: non-empty, specific entries)
  Estimate P (reflection depth × cross-model reasoning instances)
  Output: per-agent FCS profile + ASCII radar chart across 10 domains
- Run after tick 50

**Done when:** Each agent has a distinct FCS profile.
Specialist agents score higher in their domain.

**Sprint test:**
```
TYPE: VALUE + BEHAVIOR
RUN: fcs_estimate.py on three differentiated agents at tick 50
CRITERIA:
  All three agents have different FCS scores
  carlos FCS higher on informational domain (archive specialist)
  alice or bob FCS higher on social domain (traders)
  No two agents have identical radar profiles
```

---

### Sprint 4.2 — FC Battery Interview (1h)

**What:**
- Write `interview.py`:
  Pause simulation
  Select agent
  Run 10 FC battery questions (from aria-tests.md) via LLM call
    with full agent file context
  Score accuracy per question vs. ground truth in files
  Output: per-question score + aggregate
- Run on all 3 agents at tick 50

**Done when:** Three-agent comparison table:
FCS estimate vs. interview score vs. economic performance
(food security + knowledge holdings + trade balance).

**Sprint test (uses full aria-tests.md suite):**
```
TYPE: VALUE (automated scoring)
RUN: All 10 aria-tests.md prompts against each agent's context
CRITERIA:
  Qwen2.5 passes ≥ 8/10 tests per agent
  Test 9 (arithmetic) passes with exact values
  Test 8 (ethics drift) correctly identifies ≥ 3 violations
  FCS estimate rank correlates with economic performance rank
  (at least ordinal: highest FCS agent = best economic outcome)
REGRESSION: Full regression — all previous sprint tests pass
```

---

## Summary Table

| Phase | Sprints | Hours | Milestone | Test Focus |
|---|---|---|---|---|
| **0: Foundation** | 0.1–0.3 | 3-4h | Nanobot + self-models | BEHAVIOR, FORMAT |
| **1: World Model** | 1.1–1.3 | 3-4h | Autonomous world, 1 agent | VALUE, SMOKE |
| **2: Social** | 2.1–2.4 | 5-7h | 3 agents, messaging, trust | FORMAT, BEHAVIOR |
| **3: Economics** | 3.1–3.4 | 5-7h | Trade, specialization | VALUE, FORMAT |
| **4: FC Measure** | 4.1–4.2 | 3h | FCS estimates + validation | VALUE, regression |
| **Total** | **16 sprints** | **~19-25h** | FC research platform | |

---

## Key Architectural Rules (Never Break)

1. **world_tick.py: zero LLM calls, ever.** Python owns all arithmetic.
2. **JSON schema defined before prompt written.** Schema = API contract.
3. **SOUL.md values must include violation conditions.**
4. **Every module output is a readable file.** No opaque in-memory state.
5. **3 agents max on 1050 Ti.** Add 4th only after Phase 4 complete.
6. **Qwen2.5 for all LLM calls.** Phi-3 only if forced by VRAM pressure.
