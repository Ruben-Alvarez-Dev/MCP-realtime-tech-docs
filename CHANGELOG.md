# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.0] - 2026-04-29

### Added
- Initial release of MCP-realtime-tech-docs
- FastMCP 3.0 Python server (Anthropic MCP spec canonical)
- 6 MCP tools: search_docs, get_doc, get_quickstart, compare_products, get_examples, list_catalog
- 102 documentation files across 3 products:
  - **Qwen** (Alibaba Cloud): Omni Realtime, CosyVoice TTS, ASR, Models, Pricing
  - **Xiaomi MiMo**: Omni, TTS, Models, Token Plan API, Architecture
  - **LiveKit**: Agents, STT, LLM, Plugins, OpenAI Realtime
- DocIndex indexer with keyword search
- Install script with curl one-liner
- Update script for syncing docs from local sources
- SPEC.md technical specification
- Full test suite
- GitHub Actions CI pipeline
- MIT License
