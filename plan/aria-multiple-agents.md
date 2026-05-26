Prompt:
The most important question mark for me is whether to build multiple
agents into one Nanobot "session" / agent, or maybe spawn a Nanobot
for each agent?
My core doubt is particularly around "SOUL.md", which exists and is
valid for one Nanobot session. Also, future use of ARIA would be more
as one agent to support one user, and not simulating multiple users.

Can you produce a comparison and recommendation?



## The Core Question

You have two options:

**Option A — One Nanobot, multiple workspaces** (Python SDK, `workspace=` per agent)
**Option B — Multiple Nanobot instances** (separate configs, separate processes)

---

## Comparison

| Dimension | Option A: One Nanobot, multiple workspaces | Option B: Multiple Nanobot instances |
|---|---|---|
| **SOUL.md** | One per workspace — fully isolated, each agent gets their own | One per instance — same result, but heavier to set up |
| **Memory isolation** | Complete — each workspace has its own `MEMORY.md`, `history.jsonl`, Dream cursor | Complete — but requires separate config files and ports |
| **Orchestration** | Your `sim_runner.py` calls `bot.run(..., workspace="agents/alice")` in sequence — one Python process owns everything | You'd need HTTP calls or subprocess coordination between processes |
| **WORLD.md (shared state)** | Trivial — it's just a file all three SDK calls can read | Requires a shared filesystem mount or an API layer |
| **world_tick.py** | Lives naturally alongside `sim_runner.py` in the same process | Would need to be a separate process or daemon |
| **Complexity** | Low — one config, one Python entry point, all agents are function calls | High — three configs, three ports, inter-process communication |
| **Dream / memory consolidation** | Works per workspace automatically | Works per instance automatically |
| **Future single-agent use (ARIA for one user)** | Trivially reduced: just use one workspace, remove sim_runner | Requires decommissioning infrastructure |
| **Debugging** | One log stream, one Python stack trace | Three separate log streams |
| **Nanobot upgrade path** | One version to update | Three instances to keep in sync |

---

## The SOUL.md Question Specifically

Your instinct was right to flag this, but the good news is: **SOUL.md is scoped to a workspace, not to a Nanobot installation.** The Python SDK's `workspace=` parameter is precisely the isolation boundary. So:

```python
alice_bot = Nanobot.from_config(workspace="agents/alice")  # reads agents/alice/SOUL.md
bob_bot   = Nanobot.from_config(workspace="agents/bob")    # reads agents/bob/SOUL.md
```

These are fully independent identities sharing one process. No conflict.

---

## The Future-Use Consideration

This is the decisive factor you raised. ARIA's end state is one agent supporting one user — not a simulation. Under Option B, Alice/Bob/Carlos are three real Nanobot instances, and when you transition to single-agent use, you're dismantling infrastructure. Under Option A, the simulation is just `sim_runner.py` calling three workspaces in a loop — remove the loop and you have a single-agent system. The architecture doesn't change, only the orchestration script does.

---

## Recommendation

**Option A — One Nanobot, multiple workspaces via the Python SDK.**

The `workspace=` parameter is exactly the right seam for agent isolation in Nanobot. The simulation layer (world_tick, sim_runner, messaging) lives entirely in your Python code, which is where ARIA's logic belongs anyway per your inviolable rules. The transition from multi-agent simulation to single-agent production is a deletion, not a migration.

Option B is the right choice only if you need agents to run *concurrently in real time* on separate channels (e.g., Alice on Telegram, Bob on Discord). For a controlled FC experiment where you tick agents sequentially, it's pure overhead.