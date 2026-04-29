# MCP Realtime Tech Docs — Specification

## Overview
An MCP (Model Context Protocol) server providing live documentation for realtime voice and video technologies. Built with FastMCP 3.0 (canonical Anthropic MCP spec).

## Architecture
- **Protocol:** MCP (Model Context Protocol) by Anthropic
- **Framework:** FastMCP 3.2+ (Python)
- **Transport:** stdio (default), SSE (optional)
- **Index:** In-memory JSON index, rebuilt on startup if stale

## Tools (6)

| Tool | Description | Parameters |
|------|-------------|------------|
| search_docs | Search all docs by keywords | query, product?, max_results? |
| get_doc | Read specific document | path, max_bytes? |
| get_quickstart | Quickstart guide by product | product, use_case? |
| compare_products | Side-by-side comparison | products[] |
| get_examples | Code examples | product, feature? |
| list_catalog | Full documentation catalog | product? |

## Products Covered

### Qwen (Alibaba Cloud)
- Qwen3.5-Omni Realtime (WebSocket + HTTP)
- Qwen3-TTS (Voice Design + Voice Cloning)
- Qwen3-ASR (Speech Recognition)
- CosyVoice (TTS Engine)
- Models: Qwen3.5, Qwen3, Qwen-VL, Qwen-Audio

### Xiaomi MiMo
- MiMo-V2.5 (native omnimodal MoE)
- MiMo-V2.5-Pro (flagship agent model)
- MiMo-V2-Flash (efficient reasoning, 309B/15B active)
- MiMo TTS (voice synthesis)
- Token Plan (subscription service, tp- keys)
- Endpoints: token-plan-ams.xiaomimimo.com/{v1,anthropic}

### LiveKit
- Agents framework (67+ plugins)
- STT: Deepgram, AssemblyAI, Cartesia, Soniox, etc.
- TTS: ElevenLabs, Cartesia, PlayHT, etc.
- LLM: OpenAI, Anthropic, Google, etc.
- Avatars: Tavus, Hedra, D-ID, etc.
- OpenAI Realtime integration

## Documentation Sources
1. Jart-OS/ (Ruben's curated docs) - PRIMARY source
2. Scraped from official sites (Aliyun, GitHub, HuggingFace)
3. OpenRouter model docs

## Installation
See README.md for the one-line install command.
