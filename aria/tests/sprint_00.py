#!/usr/bin/env python3
"""
sprint_00.py — Phase 0 validation: Foundation files exist and are valid.

Tests:
1. All agent directories exist (alice, bob, carlos)
2. Each agent has SOUL.md, MEMORY.md, RELATIONS.md, INVENTORY.md, PLAN.md
3. SOUL.md contains violation conditions
4. WORLD.md exists and has required sections
5. world_tick.py runs without error
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from world_tick import init_world, world_tick, write_world_md

AGENTS = ["alice", "bob", "carlos"]
REQUIRED_FILES = ["SOUL.md", "MEMORY.md", "RELATIONS.md", "INVENTORY.md", "PLAN.md"]

def test_agent_directories():
    """Test 1: All agent directories exist."""
    base = Path(__file__).parent.parent / "agents"
    for agent in AGENTS:
        assert (base / agent).exists(), f"Missing agent directory: {agent}"
    print("✓ Test 1: All agent directories exist")

def test_agent_files():
    """Test 2: Each agent has required files."""
    base = Path(__file__).parent.parent / "agents"
    for agent in AGENTS:
        for fname in REQUIRED_FILES:
            fpath = base / agent / fname
            assert fpath.exists(), f"Missing {fname} for {agent}"
            assert fpath.stat().st_size > 0, f"Empty {fname} for {agent}"
    print("✓ Test 2: All agent files exist and are non-empty")

def test_soul_violations():
    """Test 3: SOUL.md contains violation conditions."""
    base = Path(__file__).parent.parent / "agents"
    for agent in AGENTS:
        soul = (base / agent / "SOUL.md").read_text()
        assert "Violation condition" in soul, f"No violation conditions in {agent}/SOUL.md"
    print("✓ Test 3: All SOUL.md files contain violation conditions")

def test_world_md():
    """Test 4: WORLD.md exists and has required sections."""
    world_path = Path(__file__).parent.parent / "WORLD.md"
    assert world_path.exists(), "Missing WORLD.md"
    content = world_path.read_text()
    assert "Locations" in content, "WORLD.md missing Locations section"
    assert "Resources" in content or "Current Tick" in content, "WORLD.md missing key sections"
    print("✓ Test 4: WORLD.md exists with required sections")

def test_world_tick_runs():
    """Test 5: world_tick.py executes without error."""
    agents = [
        {"name": "alice", "aptitude": {"tool": 1.2, "food": 1.0, "knowledge": 1.0}},
        {"name": "bob", "aptitude": {"tool": 1.0, "food": 1.2, "knowledge": 1.0}},
        {"name": "carlos", "aptitude": {"tool": 1.0, "food": 1.0, "knowledge": 1.2}},
    ]
    world = init_world(agents)
    for _ in range(5):
        world_tick(world)
    assert world.tick == 5, f"Expected tick 5, got {world.tick}"
    # Verify agents still have food (depletion + regeneration + production)
    for name, agent in world.agents.items():
        assert agent.food >= 0, f"{name} food went negative: {agent.food}"
        assert agent.tools > 0, f"{name} should have produced tools"
    print("✓ Test 5: world_tick.py runs correctly")

def test_self_model():
    """Test 6: SELF_MODEL.md exists."""
    sm_path = Path(__file__).parent.parent / "SELF_MODEL.md"
    assert sm_path.exists(), "Missing SELF_MODEL.md"
    print("✓ Test 6: SELF_MODEL.md exists")

if __name__ == "__main__":
    tests = [
        test_agent_directories,
        test_agent_files,
        test_soul_violations,
        test_world_md,
        test_world_tick_runs,
        test_self_model,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__doc__.split('.')[0]}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__doc__.split('.')[0]}: ERROR: {e}")
            failed += 1

    print(f"\n{passed}/{passed + failed} tests passed")
    sys.exit(0 if failed == 0 else 1)
