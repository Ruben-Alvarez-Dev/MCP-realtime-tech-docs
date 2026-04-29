# Xiaomi MiMo Real-Time Ecosystem — Complete Guide

> Last updated: April 2026  
> Source: Xiaomi MiMo Platform, GitHub, HuggingFace

## Table of Contents
1. [MiMo Ecosystem Overview](#mimo-ecosystem-overview)
2. [Model Family](#model-family)
3. [API Endpoints](#api-endpoints)
4. [Token Plan — Special Endpoints](#token-plan--special-endpoints)
5. [Quick Start](#quick-start)

---

## MiMo Ecosystem Overview

Xiaomi MiMo is a family of large language models developed by Xiaomi. The V2.5 series (released April 2026) represents the latest generation, featuring:

- **Native omni-modal** capabilities (text, image, video, audio)
- **Agentic optimization** — built for real-world agent workflows
- **1M-token context window**
- **Open-source** under MIT license
- **Token Plan** subscription for API access with special endpoints

---

## Model Family

### MiMo-V2.5-Pro — Flagship Agent Model
| Spec | Value |
|---|---|
| Total Parameters | 1.02T |
| Active Parameters | 42B |
| Context Length | 1M tokens |
| Architecture | Sparse MoE, Hybrid Attention (7:1 SWA:GA) |
| MTP Layers | 3 |
| License | MIT |
| Open Source | ✅ (including Base weights) |

**Key benchmarks:**
- Artificial Analysis Intelligence Index: **#8 globally, #2 in Chinese LLMs**
- PinchBench: **81.0 (#3 globally)**
- ClawEval: **61.5 (approaching Claude Opus 4.6 at 66.3)**
- SWE-Bench Verified: competitive with Claude Opus 4.6

### MiMo-V2.5 — Native Omni-Modal Model
| Spec | Value |
|---|---|
| Total Parameters | 310B |
| Active Parameters | 15B |
| Context Length | 1M tokens |
| Architecture | Sparse MoE, Hybrid Attention (5:1 SWA:GA) |
| Vision Encoder | 729M-param ViT (28 layers: 24 SWA + 4 Full) |
| Audio Encoder | 261M-param Audio Transformer (24 layers) |
| MTP Layers | 3 |
| License | MIT |

**Capabilities:** Text, image, video, and audio understanding in a unified architecture. Strong agentic performance, competitive with much larger models.

### MiMo-V2-Flash — Efficient Reasoning Model
| Spec | Value |
|---|---|
| Total Parameters | 309B |
| Active Parameters | 15B |
| Context Length | 256K tokens |
| Architecture | Sparse MoE, Hybrid Attention (5:1 SWA:GA) |
| License | MIT |

### MiMo-V2.5-TTS-Series — Voice Synthesis
- **Premium TTS Voices** — Built-in high-quality voices with style-instruction following
- **Voice Design** — Generate entirely new voices from a single text prompt
- **Voice Cloning** — High-fidelity voice replication from minimal audio samples

---

## API Endpoints

### Standard API (Pay-per-use)
```
https://api.xiaomimimo.com/v1/chat/completions
```

**Authentication (choose one):**
```
# Method 1: api-key header
api-key: $MIMO_API_KEY
Content-Type: application/json

# Method 2: Bearer token
Authorization: Bearer $MIMO_API_KEY
Content-Type: application/json
```

### Token Plan Endpoints (Subscription)

> ⚠️ These are the **Token Plan** endpoints for subscribers. Token Plan uses tokens starting with `tp-` (not `sk-`).

**OpenAI Compatibility Protocol:**
| Region | Endpoint |
|---|---|
| China | `https://token-plan-cn.xiaomimimo.com/v1` |
| Europe (Amsterdam) | `https://token-plan-ams.xiaomimimo.com/v1` |

**Anthropic Compatibility Protocol:**
| Region | Endpoint |
|---|---|
| China | (check platform) |
| Europe (Amsterdam) | `https://token-plan-ams.xiaomimimo.com/anthropic` |

**Token Plan Features:**
- Token prefix: `tp-` (not `sk-`)
- Monthly/annual subscriptions available
- Covers all V2.5 models (Pro, Omni, TTS)
- One account = one first-purchase discount
- TTS free across all tiers for a limited time

---

## Quick Start

### Minimal API Call (curl)
```bash
curl -X POST https://api.xiaomimimo.com/v1/chat/completions \
  -H "api-key: $MIMO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MiMo-V2.5-Pro",
    "messages": [
      {"role": "system", "content": "You are MiMo, an AI assistant developed by Xiaomi."},
      {"role": "user", "content": "Hello, what can you do?"}
    ],
    "max_tokens": 4096,
    "temperature": 0.8,
    "top_p": 0.95,
    "stream": true
  }'
```

### Token Plan Call
```bash
curl -X POST https://token-plan-ams.xiaomimimo.com/v1/chat/completions \
  -H "Authorization: Bearer tp-YOUR_TOKEN_PLAN_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MiMo-V2.5-Pro",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ],
    "stream": true
  }'
```

### With OpenAI Python SDK
```python
from openai import OpenAI

# Standard API
client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://api.xiaomimimo.com/v1"
)

# Or Token Plan (Europe)
client_tp = OpenAI(
    api_key="tp-YOUR_TOKEN_PLAN_KEY",
    base_url="https://token-plan-ams.xiaomimimo.com/v1"
)

response = client.chat.completions.create(
    model="MiMo-V2.5-Pro",
    messages=[
        {"role": "system", "content": "You are MiMo, an AI assistant developed by Xiaomi."},
        {"role": "user", "content": "Write a Python function to sort a list"}
    ],
    max_tokens=4096,
    temperature=0.8,
    top_p=0.95,
    stream=True
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### Recommended Parameters
| Parameter | Reasoning/Writing/Dev | Agentic Tasks |
|---|---|---|
| temperature | 0.8 | 0.3 |
| top_p | 0.95 | 0.95 |

### Recommended System Prompt
**English:**
```
You are MiMo, an AI assistant developed by Xiaomi.
Today's date: {date} {week}. Your knowledge cutoff date is December 2024.
```

**Chinese:**
```
你是MiMo（中文名称也是MiMo），是小米公司研发的AI智能助手。
今天的日期：{date} {week}，你的知识截止日期是2024年12月。
```

---

## Pricing

| Model | Input (per 1M tokens) | Output (per 1M tokens) | Cache Write | Cache Read |
|---|---|---|---|---|
| MiMo-V2.5-Pro (up to 256K) | $1 | $3 | $0.20 | $0 |
| MiMo-V2.5-Pro (256K-1M) | $2 | $6 | $0.40 | $0 |
| Claude Sonnet 4.6 (comparison) | $3 | $15 | $0.30 | $3.75 |
| Claude Opus 4.6 (comparison) | $5 | $25 | $0.50 | $6.25 |

> MiMo Cache Write is temporarily free.

---

## Files in this Directory

| File | Content |
|---|---|
| [00-OVERVIEW.md](./00-OVERVIEW.md) | This overview |
| [01-API-REFERENCE.md](./01-API-REFERENCE.md) | Full API reference, endpoints, parameters |
| [02-MIMO-V25-ARCHITECTURE.md](./02-MIMO-V25-ARCHITECTURE.md) | MiMo-V2.5/V2.5-Pro architecture details |
| [03-MIMO-V2-FLASH.md](./03-MIMO-V2-FLASH.md) | MiMo-V2-Flash architecture & benchmarks |
| [04-MIMO-V25-PRO.md](./04-MIMO-V25-PRO.md) | MiMo-V2.5-Pro agent capabilities & benchmarks |
| [05-TOKEN-PLAN.md](./05-TOKEN-PLAN.md) | Token Plan details, special endpoints, migration |
| [06-MIMO-TTS.md](./06-MIMO-TTS.md) | MiMo TTS voice synthesis capabilities |
| [07-CODE-EXAMPLES.md](./07-CODE-EXAMPLES.md) | Working code examples |
