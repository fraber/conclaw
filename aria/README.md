# ARIA — Adaptive Reasoning with Inspectable Architecture

## Purpose

A multi-agent simulation platform for validating **Functional Consciousness (FC)** as a measurable metric.

## Structure

```
aria/
├── agents/
│   ├── alice/          # Agent with tool aptitude +20%
│   │   ├── SOUL.md     # Personality, goals, values + violation conditions
│   │   ├── MEMORY.md   # Episodic memory + belief store
│   │   ├── RELATIONS.md # Social graph: trust scores, interaction history
│   │   ├── INVENTORY.md # Private resources: food, tools, knowledge tokens
│   │   └── PLAN.md     # Current active plan with step status
│   ├── bob/            # Agent with food aptitude +20%
│   └── carlos/         # Agent with knowledge aptitude +20%
├── skills/             # Agent-facing skill definitions
│   └── self_assess/    # FC battery (41 tests)
├── tests/              # Sprint tests
├── docs/               # Design docs
├── world_tick.py       # Pure-Python world engine (NO LLM)
├── sim_runner.py       # Tick orchestrator
├── WORLD.md            # Shared world state
├── SELF_MODEL.md       # Global FC aggregator
└── sim.log             # Tick log
```

## Inviolable Rules

1. **world_tick.py: zero LLM calls, ever.** Python owns all arithmetic.
2. **JSON schema defined before prompt written.** Schema = API contract.
3. **SOUL.md values must include explicit violation conditions.**
4. **Every module output is a readable file.** No opaque in-memory state.

## FC Metric

**FCS = R × P**
- R = B × D̄ (representational capacity: breadth × depth)
- P = reasoning power (system-level constant per LLM)
- Zero-floor: R=0 OR P=0 → FCS=0

## Simulation Parameters

- Tick interval: 30s real time
- Food depletion: 3 units/agent/tick
- Food regeneration: 1 unit/tick
- Tool production: 0.3/tick × aptitude modifier
- Knowledge tokens: max 2 agents/tick at Archive
- Reflection: every 10 ticks
- Archive rumor: planted tick 20, closes tick 60
