## nanobot — Summary

**What it is:**
An open-source, ultra-lightweight personal AI agent (Python).
Inspired by OpenClaw, Claude Code and OpenAI Codex. MIT license. ~41.8k GitHub stars.

**Core philosophy:**
Keep the agent loop small and readable.
Memory, MCP, and skills are injected as context,
not a heavy orchestration layer.
Designed to be studied, modified, and extended.

**Install:**
```bash
pip install nanobot-ai        # PyPI (stable)
uv tool install nanobot-ai    # via uv
# or clone + pip install -e . # from source (latest)
```

**Quick start:** `nanobot onboard` → configure `~/.nanobot/config.json` with provider/model → `nanobot agent`

**Key capabilities:**
- Most industry chat channels, email
- Most LLM providers: OpenRouter, ...
- MCP (Model Context Protocol) support
- Web search (Kagi, Olostep, multi-provider)
- Memory system (token-based, Dream two-stage)
- Cron/scheduled tasks with natural language
- OpenAI-compatible API + Python SDK
- Docker + Linux service deployment
- WebUI (dev; requires source checkout)
- Langfuse observability

**Architecture:** Messages → LLM → tools
(workspace, shell, web, MCP) → memory/skills as context.
Single agent loop. No monolith.

**Language:** Python 91%, TypeScript 8% (WebUI).
Requires Python ≥ 3.11.

**Latest release:** v0.1.5.post3 (2026-04-29)

**Docs:** `github.com/HKUDS/nanobot/blob/main/docs/` or `nanobot.wiki`

---

