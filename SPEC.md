# SPEC: MCP-realtime-tech-docs

## Overview
MCP server providing live documentation for realtime voice & video technologies.
Built with FastMCP 3.0 (Python) following the Anthropic Model Context Protocol specification.

## Products
- **Qwen (Alibaba Cloud):** Qwen3.5-Omni Realtime, Qwen3-TTS, Qwen3-ASR, CosyVoice, 55+ voices
- **Xiaomi MiMo:** V2.5 (omnimodal MoE), V2.5-Pro, V2-Flash, V2.5-TTS, Token Plan (tp- keys)
- **LiveKit:** Agents (67+ plugins), STT, TTS, LLM, Avatars, OpenAI Realtime

## Tools
| Tool | Description | Parameters |
|------|-------------|------------|
| search_docs | Search by keywords | query, product?, max_results? |
| get_doc | Read document | path, max_bytes? |
| get_quickstart | Quickstart guide | product, use_case? |
| compare_products | Compare products | products[] |
| get_examples | Code examples | product, feature? |
| list_catalog | Full catalog | product? |

## Architecture
```
MCP-realtime-tech-docs/
├── src/server.py          # FastMCP server (6 tools)
├── src/indexer.py         # Doc index builder/query
├── docs/                  # Documentation (Qwen, Xiaomi, LiveKit)
├── index/docs-index.json  # Pre-built search index
├── tests/                 # Unit tests
├── scripts/               # Install + update scripts
├── pyproject.toml
├── README.md
└── SPEC.md
```

## Protocol
- MCP Version: 2024-11-05
- Transport: stdio
- Framework: FastMCP 3.2+
- Language: Python 3.10+
- License: MIT
