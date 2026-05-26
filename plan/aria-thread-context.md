# ARIA — Context Summary for New Thread
## Paste this at the start of a new conversation to restore full context

---

## Project Identity

**ARIA** (Adaptive Reasoning with Inspectable Architecture) is a
multi-agent cognitive architecture built on **Nanobot** (lightweight
~4k LoC agent framework, file-based, git-backed). It implements and
extends **Scene-Based Reasoning (SBR)** using LLMs instead of symbolic
engines, and is designed to maximize **Functional Consciousness (FC)**
— a measurable metric from the paper "Functional Consciousness: A Proxy
Metric Using Self-Models" (Bergmann, AGI-2026).

**Hardware**: NVIDIA 1050 Ti, 4GB VRAM. **Model**: Qwen2.5 7B Q4
(4.7GB, partial CPU offload, acceptable speed — use exclusively;
Phi-3 Mini 3.8B Q4 as fallback only). **Agents**: 3 max comfortable.

---

## Functional Consciousness (FC) — Essential Background

**FC definition**: observable capacity of a system to access and reason
about internal representations of its own states. Deliberately excludes
phenomenal consciousness / hard problem.

**FCS metric**: FCS = R × P, where:
- R = B × D̄ (representational capacity = breadth × depth)
- B = number of self-model variables tracked above noise threshold
- D̄ = average mutual information per variable
- P = state-space expansion rate per reasoning cycle (Bialek et al.)
- Multiplicative: R=0 OR P=0 → FCS=0 (map scores 0; stateless LLM scores 0)

**10 FC self-model domains**: Body, Spatial, Action/Planning,
Goal/Motivation, Cognitive, Informational, Emotional, Social,
Meta/Reflexive, Ethics/Safety.

**ARIA covers 8/10** (Body and Spatial irrelevant for software agent).

**FSMA** (Functional Self-Model Analysis): abductive method — if a
system consistently produces outputs requiring a self-model, that model
must exist. Used to infer self-models from behavioral evidence.

**FC research goal for ARIA**: agents with higher FCS should outperform
economically. If confirmed → criterion validity evidence for FC metric.

---

## SBR → ARIA Module Mapping

| ARIA Module | SBR Equivalent | LLM? | Output |
|---|---|---|---|
| Perception | Scene Reconstruction | Optional | WORLD.md slice |
| Action | Senso-Motoric | No | Tool calls |
| Planning | SBR Planner | Yes | PLAN.md (JSON) |
| Simulation | Prediction/Sandbox | Yes (per agent) | Predicted states |
| Memory | Episodic Memory | Yes (reflect only) | MEMORY.md |
| Plan Reflection | Plan Reasoning | Yes | Critique JSON |
| Belief | Logical Reasoning | Yes | MEMORY.md beliefs |
| Executive | Attention Subsystem | Yes | Goal doc + log |
| Self-Model Aggregator | (new) | No | SELF_MODEL.md |
| Self-Assessment | (new) | Yes | FCS scores |
| **world_tick.py** | (world engine) | **NEVER** | WORLD.md |

---

## File Structure

```
WORLD.md                    # Shared world: locations, resources, events, tick
SELF_MODEL.md               # Global FC aggregator (all 10 domains)
sim.log                     # Tick log
messages/{name}_inbox.md    # Per-agent message queue

agents/{name}/
  SOUL.md       # Goals (prioritized), values + VIOLATION CONDITIONS,
                # preferences, capability boundaries, aptitude modifiers
  MEMORY.md     # Episodes (dated) + Beliefs (confidence/source/verified)
  RELATIONS.md  # Trust scores, debt, interaction history per known agent
  INVENTORY.md  # food, tools, knowledge tokens
  PLAN.md       # Active plan with step status
  SELF_MODEL.md # FC self-assessment output
```

---

## SOUL.md Standard

Values MUST include violation conditions:
```markdown
## Value: Be honest in all communications
Violation condition: stating a false inventory number or factual claim

## Value: Share knowledge freely
Violation condition: charging resources in exchange for knowledge
```

---

## World + Social + Economics

**World tick** (pure Python, zero LLM):
- Food: depletes 3 units/agent/tick, regenerates 1 unit/tick
- Tools: produced in Workshop (0.3/tick × aptitude modifier)
- Knowledge tokens: acquired at Archive (capacity: 2 agents/tick),
  appreciates after Archive closes at tick 60
- Tick interval: 30s real time

**Three agents** (distinct SOUL.md personalities):
- alice: tool aptitude +20%
- bob: food aptitude +20%
- carlos: knowledge aptitude +20%

**Social mechanics**:
- Location-filtered observation (genuine info asymmetry)
- One message/tick to one agent (JSON, delivered next tick)
- Trust: +0.05 cooperative, -0.10 conflict (Python rule, no LLM)
- Reflection every 10 ticks: {behavioral, world, goal_update} JSON

**Trade protocol** (JSON):
```json
{"action":"trade","target":"bob","offer":"12 food",
 "request":"1 tool","justification":"...","expiry":55}
```
Response: accept/counter/decline. On accept: both INVENTORY.md update
atomically (Python). Outcome logged to WORLD.md + both MEMORY.md +
RELATIONS.md.

---

## Architectural Rules (Inviolable)

1. **world_tick.py: zero LLM calls.** Python owns all arithmetic.
2. **JSON schema defined before prompt.** Schema = API contract.
3. **SOUL.md values must include violation conditions.**
4. **Every module output is a readable file.** No opaque in-memory state.
5. **3 agents max on 1050 Ti.**
6. **Qwen2.5 for all LLM calls.** Phi-3 only under VRAM pressure.

---

## Test Suite: aria-tests.md

10 tests covering all major ARIA call types. All use JSON output.
Test types: json_key, json_match (regex), json_range, json_contains_any,
json_contains_all, not_contains, contains_any.

Key results from Qwen2.5 testing:
- Passes 9/10 tests reliably
- **Fails Test 9** (world food arithmetic: 201-9+3=195, model gets wrong)
  → confirms world_tick.py must be pure Python
- Explicit violation conditions in prompts (Test 8) are load-bearing
- Action menu must be injected explicitly in every agent_tick prompt
- JSON format required for all inter-module communication

---

## Phase Plan Summary

| Phase | Hours | Milestone |
|---|---|---|
| 0: Foundation | 3-4h | Nanobot + SOUL.md + MEMORY.md + self_assess |
| 1: World Model | 3-4h | world_tick.py + single agent + sim_runner |
| 2: Social | 5-7h | 3 agents + messaging + trust + reflection |
| 3: Economics | 5-7h | inventory + trade + archive + specialization |
| 4: FC Measure | 3h | fcs_estimate.py + interview.py + validity table |
| **Total** | **~19-25h** | **FC research platform** |

Each sprint (~1-2h) ends with a runnable test in `tests/sprint_NN.py`.

---

## Related Papers (Brief)

**FC paper**: Bergmann (AGI-2026). FCS = R×P. Proposes metric, benchmarks
(Waymo=74.5k, Gen.Agents=6.5M, Human=~14M). FSMA = abductive black-box
inference. Known issues: multiplicative aggregation formula needs formal
derivation (errata page: functional-consciousness.com/updates).

**Active Inference paper**: Wilson et al. (AGI-2026). Agency = intentionality
+ rationality + explainability, instantiated in POMDP/active inference.
Empowerment (channel capacity between actions and observations) as agency
metric. Three phenotypes: 0 bits (zero agency), 1 bit (intermediate),
log2(3)≈1.585 bits (high agency). Governance implication: high-agency
systems require internalist control (preference modulation), not external
constraints.

**SBR paper**: Bergmann & Fenton (AGI-2015).
URL: https://agi-conf.org/2015/wp-content/uploads/2015/07/agi15_bergmann.pdf
Nine subsystems, gödelization (plans as inspectable scenes). ARIA
re-implements each subsystem with LLM or Python rule.

**Nanobot**: lightweight agent framework, file-based, ~4k LoC.
Supports Ollama. ARIA extends it with world simulation, multi-agent
coordination, and FC measurement layer.

---

## Open Questions for ARIA Thread

1. How to implement observe.py most usefully for real-time research use?
2. fcs_estimate.py: how to estimate P from file content automatically?
3. Is 30s/tick the right interval, or should it be event-driven?
4. How to handle agent death (food=0) — respawn or permanent removal?
5. How to make reflection quality distinguishable between agents
   with different SOUL.md configurations?
6. What is the minimal economic outcome metric for criterion validity?
   (Suggestion: food-security-ticks + knowledge-holdings + trade-balance)
