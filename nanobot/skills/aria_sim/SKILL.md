---
name: aria_sim
description: Control the ARIA multi-agent FC simulation. Run ticks, check status, send messages, manage trades.
---

# ARIA Simulation Controller

Control the ARIA multi-agent simulation platform. ARIA simulates agents with persistent memory, social relationships, and economic incentives — designed to maximize Functional Consciousness.

## Quick Reference

| Command | Description |
|---|---|
| `/aria tick` | Advance one simulation tick |
| `/aria tick N` | Advance N ticks (dry-run if N > 10) |
| `/aria status` | Show all agent states and world info |
| `/aria world` | Show full WORLD.md |
| `/aria agents` | Show per-agent details (SOUL, inventory, plan) |
| `/aria talk <agent> <message>` | Send a message to an agent (queued for next tick) |
| `/aria inbox <agent>` | Show an agent's message queue |
| `/aria trade <from> <to> <offer> <request>` | Initiate a trade between agents |
| `/aria assess` | Run FC self-assessment battery |
| `/aria reset` | Reset simulation to tick 0 |
| `/aria log` | Show last 20 lines of sim.log |

## Prerequisites

ARIA is located at `/app/aria/`. The core engine is `world_tick.py` (pure Python, no LLM).

## Workflows

### Advance a Tick

When the user says "tick" or "advance" or "next":

1. Run: `cd /app/aria && python world_tick.py`
2. Read `/app/aria/WORLD.md` and report the current state
3. If there are events in the log, summarize them
4. If tick >= 10, remind the user about reflection (every 10 ticks)

Example response:
```
Tick 5 complete.
- alice@Workshop: food=2.0, tools=1.80, knowledge=0.00
- bob@Fields: food=5.0, tools=1.50, knowledge=0.00
- carlos@Archive: food=2.0, tools=1.50, knowledge=1.80

Events: None this tick.
```

### Show Status

When the user says "status" or "how are they doing":

1. Read `/app/aria/WORLD.md`
2. Read each agent's `/app/aria/agents/{name}/INVENTORY.md`
3. Summarize: locations, resources, current plans

### Send a Message

When the user says "talk to alice" or "send bob a message":

1. Parse the agent name and message content
2. Append to `/app/aria/messages/{agent}_inbox.md`:
   ```
   | Tick | From | Message |
   |---|---|---|
   | {current_tick} | user | {message} |
   ```
3. Confirm: "Message queued for {agent}, will be delivered next tick."

### Show Inbox

When the user says "alice's inbox" or "what did bob receive":

1. Read `/app/aria/messages/{agent}_inbox.md`
2. Display the message queue

### Initiate a Trade

When the user says "alice trades with bob":

1. Parse the trade details (offer, request, agents)
2. Append a trade proposal to `/app/aria/messages/{from}_inbox.md`:
   ```json
   {"action":"trade","target":"bob","offer":"12 food","request":"1 tool","justification":"...","expiry":55}
   ```
3. The trade will be processed by the next world tick (when trade logic is implemented)

### Run FC Assessment

When the user says "assess" or "check FC" or "functional consciousness":

1. Note: Mode A (24 tests, no LLM) reads agent files directly
2. Note: Mode B (17 tests, LLM required) injects files into prompts
3. For now, report: "FC assessment skill not yet implemented. Coming in Phase 4."
4. Show what domains are currently tracked in SELF_MODEL.md

### Reset Simulation

When the user says "reset" or "start over":

1. Delete and recreate all agent files from templates
2. Reset WORLD.md to tick 0
3. Clear sim.log and messages/
4. Confirm: "Simulation reset to tick 0."

### Show Log

When the user says "log" or "simulation log":

1. Read the last 20 lines of `/app/aria/sim.log`
2. If the file doesn't exist, say "No simulation has been run yet."

## Important Notes

- **world_tick.py never uses LLM calls** — it's pure Python arithmetic
- Agent files are the source of truth — always read them after a tick
- Messages are queued per-agent and delivered on the next tick
- Trade logic is not yet implemented in world_tick.py (Phase 3)
- Reflection every 10 ticks is not yet implemented (Phase 2)

## File Locations

```
/app/aria/
├── world_tick.py          # Core engine
├── sim_runner.py          # Full orchestrator (async)
├── WORLD.md               # Shared world state
├── SELF_MODEL.md          # FC aggregator
├── sim.log                # Tick history
├── agents/
│   ├── alice/             # Agent files
│   ├── bob/
│   └── carlos/
├── messages/              # Per-agent message queues
└── skills/                # ARIA skills (self_assess, etc.)
```
