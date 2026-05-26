#!/usr/bin/env python3
"""
sim_runner.py — Tick orchestrator for ARIA simulation.

Coordinates:
- world_tick.py (pure-Python world updates)
- Agent skills (LLM-based perception, planning, action)
- File I/O (read/write agent states)

Usage:
    python sim_runner.py [--ticks N] [--interval SECONDS] [--dry-run]
"""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from world_tick import (
    WorldState,
    AgentState,
    init_world,
    world_tick,
    write_world_md,
    write_sim_log,
)

# ─── Agent Configuration ─────────────────────────────────────────

AGENT_CONFIGS = [
    {
        "name": "alice",
        "aptitude": {"tool": 1.2, "food": 1.0, "knowledge": 1.0},
        "start_location": "Commons",
    },
    {
        "name": "bob",
        "aptitude": {"tool": 1.0, "food": 1.2, "knowledge": 1.0},
        "start_location": "Commons",
    },
    {
        "name": "carlos",
        "aptitude": {"tool": 1.0, "food": 1.0, "knowledge": 1.2},
        "start_location": "Commons",
    },
]

# ─── Agent Tick Logic ────────────────────────────────────────────

async def agent_tick(agent_name: str, world: WorldState) -> dict:
    """
    Execute one tick for a single agent.

    This is where LLM-based skills would be called:
    1. Perception: read WORLD.md slice relevant to agent's location
    2. Planning: generate PLAN.md steps based on SOUL.md + current state
    3. Action: execute plan steps (move, produce, trade, etc.)

    For now, returns a stub result.
    """
    agent = world.agents[agent_name]

    result = {
        "agent": agent_name,
        "tick": world.tick,
        "actions": [],
        "perception": {},
        "plan_update": None,
    }

    # TODO: LLM calls for perception, planning, action
    # For Phase 1, use simple rule-based behavior

    # Simple rule: move to aptitude location
    if agent.aptitude.get("tool", 1.0) > 1.0:
        agent.location = "Workshop"
        result["actions"].append({"type": "move", "to": "Workshop"})
    elif agent.aptitude.get("food", 1.0) > 1.0:
        agent.location = "Fields"
        result["actions"].append({"type": "move", "to": "Fields"})
    elif agent.aptitude.get("knowledge", 1.0) > 1.0:
        agent.location = "Archive"
        result["actions"].append({"type": "move", "to": "Archive"})

    return result


async def run_tick(world: WorldState) -> list[dict]:
    """Execute one full simulation tick."""
    results = []

    # 1. Agent ticks (LLM-based perception/planning/action)
    for agent_name in world.agents:
        result = await agent_tick(agent_name, world)
        results.append(result)

    # 2. World tick (pure Python, no LLM)
    world_tick(world)

    # 3. Write outputs
    write_world_md(world)
    write_sim_log(world)

    return results


async def run_simulation(
    ticks: int = 100,
    interval: float = 30.0,
    dry_run: bool = False,
) -> None:
    """Run the full simulation."""
    # Initialize world
    world = init_world(AGENT_CONFIGS)

    # Clear sim.log
    log_path = Path(__file__).parent / "sim.log"
    if log_path.exists():
        log_path.unlink()

    print(f"Starting ARIA simulation: {len(world.agents)} agents, {ticks} ticks")
    print(f"Agents: {', '.join(world.agents.keys())}")
    print()

    for i in range(ticks):
        if dry_run:
            print(f"Tick {i + 1} (dry run)")
            world.tick += 1
            write_world_md(world)
            write_sim_log(world)
            continue

        results = await run_tick(world)

        # Print summary
        agent_summary = ", ".join(
            f"{r['agent']}@{world.agents[r['agent']].location}"
            for r in results
        )
        print(f"Tick {world.tick}: {agent_summary}")

        # Check for termination conditions
        if world.tick >= ARCHIVE_CLOSE_TICK + 10:
            print(f"\nSimulation complete (tick {world.tick})")
            break

        # Wait for tick interval
        if i < ticks - 1:
            await asyncio.sleep(interval)


# ─── CLI ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ARIA Simulation Runner")
    parser.add_argument("--ticks", type=int, default=100, help="Number of ticks")
    parser.add_argument("--interval", type=float, default=30.0, help="Tick interval in seconds")
    parser.add_argument("--dry-run", action="store_true", help="Run without waiting")
    args = parser.parse_args()

    asyncio.run(run_simulation(
        ticks=args.ticks,
        interval=args.interval,
        dry_run=args.dry_run,
    ))
