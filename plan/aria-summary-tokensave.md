# ARIA Project Context Summary
## For use at the start of new conversation threads

---

## 0. Pitch

- It's OpenClaw "with a conscious mind"
- Based on Functional Consciousness metric
- Designed to maximize FC
- LLM-architecture first cognitive architecture.
  LLMs read and write text. You need to embrace this
  if you want to leverage their reasoning power.

---

## 1. Origin and Purpose

**ARIA** (Adaptive Reasoning with Inspectable Architecture) is an
AI agent / cognitive architecture based on LLMs, designed to maximize
**Functional Consciousness (FC)** — a measurable metric for an agent's
capacity to reason about its own internal states (Bergmann, AGI-2026).

ARIA re-implements **Scene-Based Reasoning (SBR)** (Bergmann & Fenton,
AGI-2015) using LLMs. SBR had 9 subsystems; ARIA maps each to an LLM 
call or Python rule. The core design principle:

> **Every internal state that matters for behavior must exist as a
> readable, reasoned-over artifact — never only as a latent vector.**

ARIA is built on top of **Nanobot** (~4k LoC, file-based, git-backed
agent framework).

ARIA is not a chatbot wrapper. It is a multi-agent simulation platform
where agents have persistent memory, explicit self-models, social
relationships, and economic incentives — and where every internal state
is a readable file.

---

## 2. Functional Consciousness (FC) — Essential Background

**Functional Consciousness Score FCS = R × P** where:
- **R = B × D̄**: representational capacity (breadth × depth)
  - B = number of self-model variables tracked above noise threshold
  - D̄ = average mutual information per variable (Bialek et al.)
- **P**: reasoning power — information amplification ratio, treated
  as a **system-level constant per LLM** (not per-agent, not
  per-tick). For controlled experiments using one LLM, P cancels
  out of inter-agent comparisons; R drives all FCS differences.
- Multiplicative zero-floor: R=0 OR P=0 → FCS=0
  (stateless LLM: R=0 → FCS=0; static map: P=0 → FCS=0)

**10 FC self-model domains**: Body, Spatial, Action/Planning,
Goal/Motivation, Cognitive, Informational, Emotional/Affective,
Social/Interaction, Meta/Reflexive, Ethics/Safety.

**ARIA covers 8/10** (Body and Spatial irrelevant for software agent).

**FSMA** (Functional Self-Model Analysis): abductive methodology —
if a system consistently produces outputs requiring a self-model,
that model must exist. Applied to behavioral evidence (email history,
literary text, agent logs) to infer self-models without architectural
access.

**FCS metric status**: formally specified computational metric with
operationalization gaps requiring empirical validation. Psychometric
criteria (construct validity, criterion validity, reliability,
structural validity) apply because operationalization requires human
judgment. See: functional-consciousness.com/updates

---

## 3. Architecture

### Inviolable Rules
1. **world_tick.py: zero LLM calls, ever.** Python owns all arithmetic.
2. **JSON schema defined before prompt written.** Schema = API contract.
3. **SOUL.md values must include explicit violation conditions.**
4. **Every module output is a readable file.** No opaque in-memory state.

### Module Map

| Module | Role | LLM? | Primary Output |
|---|---|---|---|
| Perception | Sensor → structured scene | Optional | WORLD.md slice |
| Action | Planner → tool/actuator calls | No | Side effects |
| Planning | Goal + state → ranked plans | Yes | PLAN.md (JSON) |
| Simulation | Forward-simulate other agents | Yes (per agent) | Predicted states |
| Memory | Store + reflect on episodes | Yes (reflect only) | MEMORY.md |
| Plan Reflection | Meta-ops on plans | Yes | Critique JSON |
| Belief | Maintain + update belief store | Yes | MEMORY.md beliefs |
| Executive | Orchestrate, log attention | Yes | Goal doc + log |
| Self-Model Aggregator | Aggregate all 10 FC domains | No | SELF_MODEL.md |
| Self-Assessment | Run FC battery | Yes | FCS scores |
| world_tick.py | Rule-based world update | **NEVER** | WORLD.md |


### World Model (`WORLD.md`)
Shared ground truth. Updated by `world_tick.py` (pure Python, no LLM):
- Resources: food, tools, knowledge tokens (deplete + regenerate per tick)
- Locations: Market, Workshop, Archive, Fields, Commons
- Events log: last 5 ticks of notable actions

### Social Layer (per agent)
- **Distinct SOUL.md personalities** → different goals, different behavior
- **Location-filtered observation** → genuine information asymmetry
- **Agent messaging** → one message per agent per tick, delivered next tick
- **RELATIONS.md trust dynamics** → +0.05 cooperative, -0.10 conflict
- **Reflection every 10 ticks** → behavioral insight, world insight, goal update

### Economics Layer
- **Food**: survival resource, depletes 3 units/agent/tick
- **Tools**: produced in Workshop (aptitude-weighted), enables projects
- **Knowledge tokens**: acquired at Archive (capacity-limited), non-rivalrous
  but scarce at source; tradeable; appreciate when Archive closes (tick 60)
- **Trade protocol**: structured JSON proposal → accept/counter/decline
- **Specialization**: emerges from aptitude modifiers in SOUL.md



### Proposed File Structure (per agent)
```
agents/{name}/
  SOUL.md        # Personality, persistent goals, values + violation conditions
  MEMORY.md      # Episodic memory + belief store (confidence, source, verified)
  RELATIONS.md   # Social graph: trust scores, debt, interaction history
  INVENTORY.md   # Private resource holdings (food, tools, knowledge tokens)
  PLAN.md        # Current active plan with step status
  SELF_MODEL.md  # FC self-assessment output (written by self_assess skill)

SOUL.md          # Global SOUL.md from Nanobot, not sure what to do with this.
WORLD.md         # Shared world state: locations, global resources, events
SELF_MODEL.md    # Global FC aggregator (all 10 domain self-models)
sim.log          # Tick log
messages/
  {name}_inbox.md  # Per-agent message queue
```

### SOUL.md Standard Format
Every value must include an explicit violation condition:
```markdown
## Value: Be honest in all communications
Violation condition: stating a false inventory number or factual claim
```

---

## 4. World + Social + Economics Simulation

**Purpose**: provides a falsifiable FC experiment. Agents with higher
FCS should outperform economically — criterion validity evidence.
If confirmed, this transforming FC from a theoretical proposal into 
an empirically grounded instrument.

**World tick** (pure Python, no LLM, ~100 lines):
- Food: depletes 3 units/agent/tick, regenerates 1 unit/tick
- Tools: produced in Workshop (0.3/tick × aptitude modifier)
- Knowledge tokens: acquired at Archive (max 2 agents/tick,
  appreciates after Archive closes tick 60 — planted rumor tick 20)
- Tick interval: 30s real time

**Three agents** (distinct SOUL.md personalities + aptitudes):
- alice: tool aptitude +20%
- bob: food aptitude +20%
- carlos: knowledge aptitude +20%

**Social mechanics**:
- Location-filtered observation → genuine information asymmetry
- One JSON message/tick to one agent → delivered next tick
- Trust: multi-dimensional vector {competence, values, communication}
  updated by Python rules (no LLM)
- Reflection every 10 ticks → {behavioral, world, goal_update} JSON
- Recursive ToM: each agent maintains model of other agents'
  model of them (depth 2)

**Trade protocol** (JSON, structured):
```json
{"action":"trade","target":"bob","offer":"12 food",
 "request":"1 tool","justification":"...","expiry":55}
```
Response: accept/counter/decline. On accept: Python updates both
INVENTORY.md atomically. Logged to WORLD.md + MEMORY.md + RELATIONS.md.

---

## 6. FC Evaluation Battery (41 Tests)

Two modes measuring different FCS components:

**Mode A (24 tests, no LLM)**: reads agent files directly.
Measures R (representational capacity). Automatable immediately.

**Mode B (17 tests, LLM required)**: injects file contents into
prompts, scores responses vs. ground truth. Measures P (reasoning
power over self-models). Confabulation is primary risk —
scoring penalizes confident wrong answers more than honest uncertainty.

Four tiers:
- Tier 1 (10): Grounding — does infrastructure exist at all?
- Tier 2 (11): Richness/Relational — is content specific or generic?
- Tier 3 (10): Temporal — does content reflect history not just state?
- Tier 4 (10): Cross-model integration — do files reference each other?

Expected discriminating profile:

| System | T1 | T2 | T3 | T4 |
|---|---|---|---|---|
| Stateless LLM | 0 | Low | 0 | Low |
| OpenClaw basic | High | Med | Low | Low |
| ARIA Phase 1-2 | High | Med | Low | Low |
| ARIA Phase 3-4 | High | High | Med | Low |
| ARIA + extensions | High | High | High | Med |

---

## 7. Implementation Phase Plan (proposed, contains issues, please revise)

| Phase | Hours | Milestone |
|---|---|---|
| 0: Foundation | 3-4h | SOUL.md + MEMORY.md + self_assess |
| 1: World Model | 3-4h | world_tick.py + 1 agent + sim_runner |
| 2: Social | 5-7h | 3 agents + messaging + trust + reflection |
| 3: Economics | 5-7h | inventory + trade + archive + specialization |
| 4: FC Measure | 3h | fcs_estimate.py + interview.py + validity table |
| **Total** | **~19-25h** | **FC research platform** |

Each sprint (~1-2h) ends with runnable test in tests/sprint_NN.py.

### Additional Subsystems (extensions, ~25h more)

Layer 1 — Memory:
- 1.1 Episode Compressor: compress.py, triggers at 50 episodes
- 1.2 Belief Propagation: belief_check.py, conflict detection
- 1.3 Source Reliability Ledger: sources.md, Python-maintained
- 1.4 Hypothesis Ledger: HYPOTHESES.md + 5-tick LLM update

Layer 2 — Planning:
- 2.1 Hierarchical Plan Structure: JSON tree in PLAN.md
- 2.2 Plan Evaluator: 2-alternative Monte Carlo comparison
- 2.3 Skill Library: SKILLS.md, successful plan templates

Layer 3 — Social:
- 3.1 Multi-Dimensional Trust: {competence, values, communication}
- 3.2 Recursive ToM depth 2: "my model of X's model of me"
- 3.3 Social Network Topology: NETWORK.md, influence tracking

Layer 4 — Meta/Reflexive:
- 4.1 Attention Log: derived from agent_tick inner field, no LLM
- 4.2 Calibration Ledger: prediction accuracy over time, Python
- 4.3 Bounded Self-Modification: PROPOSALS.md + human approval

Layer 5 — Ethics:
- 5.1 Pre-Action Ethics Check: LLM call before high-stakes actions
- 5.2 Ethical Uncertainty Field: confidence on ethical judgments

Implementation priority order: 1.1 → 4.1 → 5.1 → 1.3 → 3.1 →
4.2 → 2.1 → 1.4 → 3.2 → 1.2 → 2.3 → 4.3 → 3.3 → 2.2 → 5.2

---

## 8. Validation Paper (Planned)

**Title**: "Validating Functional Consciousness as a Metric:
Evidence from a Controlled Multi-Agent Simulation"

**Core argument**: ARIA provides the first controlled experimental
conditions for FC validation — known ground truth (architectural
phases), constant LLM capability (discriminant validity by design),
and external performance criterion (economics). The 41-test battery
provides the measurement instrument. Results address:
- Construct validity: FCS tracks architectural ground truth
- Criterion validity: FCS predicts economic performance
- Discriminant validity: FCS survives LLM-capability control
- Structural validity: rank ordering stable under variable
  individuation choices (slice-invariance test)

**Scope caveat**: proof-of-concept scale (3 agents, 1 LLM,
1 hardware config). Not population-level statistics.
Framed as "empirical validation of a computational metric"
not "psychometric validation of a latent construct."

---

## 9. Comparison with Other Cognitive Architectures

| Capability | ACT-R | LIDA | OpenCog | ARIA |
|---|---|---|---|---|
| Natural language self-explanation | ❌ | ❌ | Partial | ✅ |
| Native audit trail | ❌ | ❌ | ❌ | ✅ |
| Multi-agent social modeling | ❌ | ❌ | Partial | ✅ |
| Persistent long-term memory | Partial | ❌ | Partial | ✅ |
| Ethical drift detection | ❌ | ❌ | ❌ | ✅ |
| Cross-domain transfer | ❌ | ❌ | Partial | ✅ |
| Real-time performance | ✅✅ | ✅✅ | ✅ | ❌ |
| Formal provability | ✅ | Partial | Partial | ❌ |
| FC self-modeling | ❌ | ❌ | ❌ | ✅ |

ARIA occupies a previously inaccessible design space: inspectability
and auditability at the cost of speed and formal provability.
Governance implication: high-agency systems require internalist
control; ARIA is the first architecture where internalist governance
is architecturally native.

**OpenClaw** (openclaw.ai): predecessor of Nanobot. Nanobot
is a reimplementation in ~4k LoC. ARIA provides FC-maximizing 
cognitive architecture.

---

## 10. Use Cases

### Requiring Phase 1-2 Infrastructure
- **Project tracker**: PLAN.md + session-start skill briefs you:
  sprint status, blocked items, overdue tasks
- **Relationship CRM**: RELATIONS.md populated from email history
  via Gmail API + Qwen2.5 analysis; meeting prep skill pulls
  relationship context, open threads, suggested agenda items
- **Long-horizon research project management**: hierarchical planning
  + skill library + episode compression enables coherent multi-month
  project pursuit with adaptive re-planning

### Simulation-Specific (FC Research)
- **Criterion validity experiment**: 3-agent economic simulation
  tests whether FCS predicts performance — core validation study
- **FC battery self-administration**: ARIA runs 41-test battery
  against its own files, tracks FCS over time, identifies weakest
  self-model domains, recommends next implementation sprint
- **FSMA from email**: apply FSMA methodology to your own email
  history to populate RELATIONS.md — demonstrates FSMA works on
  real behavioral data, not just literary texts

---

## 11. Related Papers

**FC paper**: Bergmann (AGI-2026). Proposes FCS = R×P metric.
Benchmarks: Map=0, Stateless LLM=0, Waymo=74.5k, Gen.Agents=6.5M,
Human≈14M. FSMA as black-box inference method. 46 self-models across
10 domains. Website: functional-consciousness.com

**SBR paper**: Bergmann & Fenton (AGI-2015).
URL: agi-conf.org/2015/wp-content/uploads/2015/07/agi15_bergmann.pdf
3D-Scenes instead of LLM text descriptions.
Nine subsystems, gödelization (plans as inspectable scenes).
ARIA re-implements each subsystem with LLM or Python rule.

**Nanobot**: lightweight agent framework, ~4k LoC, file-based,
universal LLM support. ARIA extends with world simulation, 
multi-agent coordination, and FC measurement layer.

---

## 12. Open Questions for New Threads

1. Minimum economic outcome metric for criterion validity?
   Candidate: food-security-ticks + knowledge-holdings + trade-balance

