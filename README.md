# MCP Realtime Tech Docs

[![MCP](https://img.shields.io/badge/MCP-Spec%202024--11--05-blue)](https://modelcontextprotocol.io)
[![FastMCP](https://img.shields.io/badge/FastMCP-3.2+-green)](https://github.com/PrefectHQ/fastmcp)
[![Python](https://img.shields.io/badge/Python-3.10+-yellow)](https://python.org)

Live documentation MCP server for realtime voice & video technologies: **Qwen**, **Xiaomi MiMo**, and **LiveKit**.

87+ documents covering TTS, STT, Realtime APIs, voice cloning, WebRTC, agents, and more.

## Quick Install

\`\`\`bash
curl -sSL https://raw.githubusercontent.com/Ruben-Alvarez-Dev/MCP-realtime-tech-docs/main/scripts/install.sh | bash
\`\`\`

Or manually:

\`\`\`bash
git clone https://github.com/Ruben-Alvarez-Dev/MCP-realtime-tech-docs.git
cd MCP-realtime-tech-docs
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
\`\`\`

## Goose Configuration

Add to \`~/.config/goose/config.yaml\`:

\`\`\`yaml
mcp-realtime-tech-docs:
  enabled: true
  type: stdio
  name: mcp-realtime-tech-docs
  description: "Live docs for realtime voice & video (Qwen, Xiaomi MiMo, LiveKit)"
  display_name: "Voice & Video Docs MCP"
  command: /Users/your-user/MCP-servers/MCP-realtime-tech-docs/.venv/bin/python3
  args:
    - -m
    - src.server
  timeout: 30
  bundled: false
  available_tools: []
\`\`\`

## Available Tools

| Tool | Description |
|------|-------------|
| \`search_docs\` | Search all docs by keywords |
| \`get_doc\` | Read specific document content |
| \`get_quickstart\` | Quickstart guide by product |
| \`compare_products\` | Side-by-side product comparison |
| \`get_examples\` | Code examples by product & feature |
| \`list_catalog\` | Full documentation catalog |

## Products

### Qwen (Alibaba Cloud)
- **Qwen3.5-Omni Realtime** — WebSocket + HTTP realtime API
- **Qwen3-TTS** — Voice Design + Voice Cloning
- **Qwen3-ASR** — Speech Recognition
- **CosyVoice** — TTS Engine (v2, v3)
- Models: Qwen3.5, Qwen3, Qwen-VL, Qwen-Audio

### Xiaomi MiMo
- **MiMo-V2.5** — Native omnimodal MoE model
- **MiMo-V2.5-Pro** — Flagship agent model
- **MiMo-V2-Flash** — 309B total / 15B active params
- **MiMo TTS** — Voice synthesis for agents
- **Token Plan** — Subscription service (tp- keys)
- Endpoints: \`token-plan-ams.xiaomimimo.com/{v1,anthropic}\`

### LiveKit
- **Agents** — 67+ plugins framework
- **STT** — Deepgram, AssemblyAI, Cartesia, Soniox...
- **TTS** — ElevenLabs, Cartesia, PlayHT...
- **LLM** — OpenAI, Anthropic, Google...
- **Avatars** — Tavus, Hedra, D-ID...
- **OpenAI Realtime** integration

## Documentation Structure

\`\`\`
docs/
├── qwen/                    # Scraped from Aliyun, GitHub, HuggingFace
├── qwen-realtime-official/  # Curated from Jart-OS (8 files)
├── xiaomi-mimo/             # Scraped from HuggingFace, OpenRouter
├── xiaomi-realtime-official/# Curated from Jart-OS (8 files)
└── livekit/                 # Scraped from GitHub, docs.livekit.io
\`\`\`

## Updating Docs

\`\`\`bash
# Update from Jart-OS sources
./scripts/update-docs.sh
\`\`\`

## License

MIT
