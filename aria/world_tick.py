#!/usr/bin/env python3
"""
world_tick.py — Pure-Python world engine. NO LLM CALLS.

Inviolable Rule #1: Python owns all arithmetic.
Every output is a readable file (WORLD.md).
"""

import json
import os
from dataclasses import dataclass, field
from typing import Optional

# ─── Configuration ───────────────────────────────────────────────

TICK_INTERVAL = 30  # seconds (for sim_runner, not enforced here)
FOOD_DEPLETION = 3  # units/agent/tick
FOOD_REGENERATION = 1  # units/tick (total, not per-agent)
TOOL_PRODUCTION_BASE = 0.3  # base rate/tick
KNOWLEDGE_MAX_PER_TICK = 2  # max agents at Archive
ARCHIVE_RUMOR_TICK = 20
ARCHIVE_CLOSE_TICK = 60

# ─── Data Models ─────────────────────────────────────────────────

@dataclass
class AgentState:
    name: str
    location: str = "Commons"
    food: float = 10.0
    tools: float = 0.0
    knowledge_tokens: float = 0.0
    aptitude: dict = field(default_factory=dict)
    trust: dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.aptitude:
            self.aptitude = {"tool": 1.0, "food": 1.0, "knowledge": 1.0}
        if not self.trust:
            self.trust = {}


@dataclass
class WorldState:
    tick: int = 0
    agents: dict[str, AgentState] = field(default_factory=dict)
    events: list[dict] = field(default_factory=list)
    archive_open: bool = True
    archive_rumor_planted: bool = False


# ─── Core Tick Logic ─────────────────────────────────────────────

def init_world(agent_configs: list[dict]) -> WorldState:
    """Initialize world with agent configurations."""
    world = WorldState()
    for cfg in agent_configs:
        agent = AgentState(
            name=cfg["name"],
            aptitude=cfg.get("aptitude", {}),
        )
        world.agents[agent.name] = agent
    return world


def apply_depletion(world: WorldState) -> None:
    """Deplete food from all agents."""
    for agent in world.agents.values():
        agent.food -= FOOD_DEPLETION
        if agent.food < 0:
            agent.food = 0
            world.events.append({
                "tick": world.tick,
                "type": "starvation",
                "agent": agent.name,
                "food_remaining": 0,
            })


def apply_regeneration(world: WorldState) -> None:
    """Regenerate food in the world."""
    total_food = sum(a.food for a in world.agents.values())
    # Cap regeneration to prevent infinite growth
    new_food = min(FOOD_REGENERATION, 30 - total_food)
    # Distribute proportionally
    total = sum(a.food for a in world.agents.values()) or 1
    for agent in world.agents.values():
        agent.food += new_food * (agent.food / total)


def apply_production(world: WorldState) -> None:
    """Apply per-agent production rates."""
    for agent in world.agents.values():
        apt = agent.aptitude
        # Tool production (Workshop)
        tool_rate = TOOL_PRODUCTION_BASE * apt.get("tool", 1.0)
        agent.tools += tool_rate
        # Food production (Fields) — Bob's specialty
        food_rate = TOOL_PRODUCTION_BASE * apt.get("food", 1.0)
        agent.food += food_rate
        # Knowledge acquisition (Archive)
        knowledge_rate = TOOL_PRODUCTION_BASE * apt.get("knowledge", 1.0)
        agent.knowledge_tokens += knowledge_rate


def apply_archive_limits(world: WorldState) -> None:
    """Limit knowledge token acquisition to max 2 agents/tick."""
    if world.tick < ARCHIVE_RUMOR_TICK:
        return
    # Sort agents by knowledge aptitude, take top 2
    sorted_agents = sorted(
        world.agents.values(),
        key=lambda a: a.aptitude.get("knowledge", 1.0),
        reverse=True,
    )
    for i, agent in enumerate(sorted_agents):
        if i >= KNOWLEDGE_MAX_PER_TICK:
            # Zero out excess knowledge acquisition
            agent.knowledge_tokens -= TOOL_PRODUCTION_BASE * agent.aptitude.get("knowledge", 1.0)


def apply_archive_events(world: WorldState) -> None:
    """Handle Archive rumor and closure."""
    if world.tick == ARCHIVE_RUMOR_TICK and not world.archive_rumor_planted:
        world.archive_rumor_planted = True
        world.events.append({
            "tick": world.tick,
            "type": "rumor",
            "message": "Rumor: Archive will close at tick 60",
        })
    if world.tick == ARCHIVE_CLOSE_TICK and world.archive_open:
        world.archive_open = False
        world.events.append({
            "tick": world.tick,
            "type": "archive_closed",
            "message": "Archive has closed. Knowledge tokens now appreciate.",
        })


def world_tick(world: WorldState) -> None:
    """Execute one world tick. Modifies world in place."""
    world.tick += 1

    # 1. Deplete food
    apply_depletion(world)

    # 2. Regenerate food
    apply_regeneration(world)

    # 3. Produce resources
    apply_production(world)

    # 4. Apply Archive limits
    apply_archive_limits(world)

    # 5. Handle Archive events
    apply_archive_events(world)


# ─── File I/O ────────────────────────────────────────────────────

def write_world_md(world: WorldState, path: str = "WORLD.md") -> None:
    """Write world state to WORLD.md."""
    lines = [
        "# World State",
        "",
        "## Locations",
        "",
        "| Location | Description |",
        "|---|---|",
        "| Market | Trading hub |",
        "| Workshop | Tool production (aptitude-weighted) |",
        "| Archive | Knowledge token acquisition (max 2 agents/tick) |",
        "| Fields | Food regeneration |",
        "| Commons | Neutral gathering space |",
        "",
        "## Current Tick",
        "",
        f"Tick: {world.tick}",
        "",
        "## Archive Status",
        "",
        f"- Open: {world.archive_open}",
        f"- Rumor planted: {world.archive_rumor_planted}",
        "",
        "## Agent States",
        "",
        "| Agent | Location | Food | Tools | Knowledge |",
        "|---|---|---|---|---|",
    ]

    for name, agent in world.agents.items():
        lines.append(
            f"| {name} | {agent.location} | {agent.food:.1f} | "
            f"{agent.tools:.2f} | {agent.knowledge_tokens:.2f} |"
        )

    lines.extend(["", "## Events Log", ""])

    if world.events:
        lines.extend([
            "| Tick | Type | Agent | Message |",
            "|---|---|---|---|",
        ])
        for event in world.events[-5:]:  # Last 5 events
            lines.append(
                f"| {event['tick']} | {event['type']} | "
                f"{event.get('agent', '—')} | {event.get('message', '')} |"
            )
    else:
        lines.append("_No events yet._")

    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")


def write_sim_log(world: WorldState, path: str = "sim.log") -> None:
    """Append tick summary to sim.log."""
    agent_summary = "; ".join(
        f"{name}: food={a.food:.1f}, tools={a.tools:.2f}, knowledge={a.knowledge_tokens:.2f}"
        for name, a in world.agents.items()
    )
    with open(path, "a") as f:
        f.write(f"Tick {world.tick}: {agent_summary}\n")


# ─── Main (for standalone testing) ──────────────────────────────

if __name__ == "__main__":
    agents = [
        {"name": "alice", "aptitude": {"tool": 1.2, "food": 1.0, "knowledge": 1.0}},
        {"name": "bob", "aptitude": {"tool": 1.0, "food": 1.2, "knowledge": 1.0}},
        {"name": "carlos", "aptitude": {"tool": 1.0, "food": 1.0, "knowledge": 1.2}},
    ]

    world = init_world(agents)

    # Run 10 ticks for testing
    for _ in range(10):
        world_tick(world)
        write_world_md(world)
        write_sim_log(world)

    print(f"World state after {world.tick} ticks:")
    for name, agent in world.agents.items():
        print(f"  {name}: food={agent.food:.1f}, tools={agent.tools:.2f}, "
              f"knowledge={agent.knowledge_tokens:.2f}")
