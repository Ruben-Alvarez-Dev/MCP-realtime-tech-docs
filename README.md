# MCP-realtime-tech-docs

**Live documentation MCP server for realtime voice & video technologies.**

Qwen (Alibaba Cloud) · Xiaomi MiMo · LiveKit — 87+ files, 1.8MB of documentation.

## Quick Install

```bash
curl -sSL https://raw.githubusercontent.com/Ruben-Alvarez-Dev/MCP-realtime-tech-docs/main/scripts/install.sh | bash
```

Or custom path:
```bash
git clone https://github.com/Ruben-Alvarez-Dev/MCP-realtime-tech-docs.git
cd MCP-realtime-tech-docs
./scripts/install.sh /your/custom/path
```

## MCP Configuration

### Goose Desktop
```yaml
realtime-tech-docs:
  enabled: true
  type: stdio
  name: realtime-tech-docs
  command: /Users/MCP-servers/MCP-realtime-tech-docs/.venv/bin/python
  args: [-m, src.server]
  env:
    PYTHONPATH: /Users/MCP-servers/MCP-realtime-tech-docs
  timeout: 30
```

### Claude Desktop
```json
{
  "mcpServers": {
    "realtime-tech-docs": {
      "command": "/Users/MCP-servers/MCP-realtime-tech-docs/.venv/bin/python",
      "args": ["-m", "src.server"],
      "env": {"PYTHONPATH": "/Users/MCP-servers/MCP-realtime-tech-docs"}
    }
  }
}
```

## Tools (6)

| Tool | Description |
|------|-------------|
| search_docs(query, product?) | Search all docs by keywords |
| get_doc(path) | Read a specific document |
| get_quickstart(product) | Quickstart guide for a product |
| compare_products(products[]) | Compare products side-by-side |
| get_examples(product, feature?) | Get code examples |
| list_catalog(product?) | Browse full catalog |

## Products

### Qwen (Alibaba Cloud)
- Qwen3.5-Omni Realtime — WebSocket + HTTP, 55+ voices
- Qwen3-TTS — Voice Design + Voice Cloning
- Qwen3-ASR — Speech recognition (open source)
- CosyVoice TTS — Streaming + batch

### Xiaomi MiMo
- MiMo-V2.5 — Native omnimodal MoE
- MiMo-V2.5-TTS — Voice synthesis
- Token Plan — Subscription API (tp- keys)
  - OpenAI: https://token-plan-ams.xiaomimimo.com/v1
  - Anthropic: https://token-plan-ams.xiaomimimo.com/anthropic

### LiveKit
- Agents — 67+ plugins
- STT/TTS/LLM/Avatar plugins
- OpenAI Realtime integration

## Update Docs
```bash
./scripts/update-docs.sh
```

## License
MIT
