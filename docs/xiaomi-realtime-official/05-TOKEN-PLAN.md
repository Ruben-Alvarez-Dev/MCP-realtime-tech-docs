# MiMo Token Plan — Complete Guide

> Source: Xiaomi MiMo Platform, Twitter/X announcements, community reports

## What is the Token Plan?

The **MiMo Token Plan** is a subscription service that provides API access to all MiMo models through dedicated endpoints. Unlike pay-per-use (`sk-` keys), Token Plan uses `tp-` prefixed tokens and special regional endpoints.

---

## Token Plan Endpoints

### OpenAI-Compatible Protocol

| Region | Endpoint |
|---|---|
| **China** | `https://token-plan-cn.xiaomimimo.com/v1` |
| **Europe (Amsterdam)** | `https://token-plan-ams.xiaomimimo.com/v1` |

### Anthropic-Compatible Protocol

| Region | Endpoint |
|---|---|
| **Europe (Amsterdam)** | `https://token-plan-ams.xiaomimimo.com/anthropic` |

---

## Authentication

Token Plan tokens start with **`tp-`** (NOT `sk-`):

```bash
# OpenAI-compatible
Authorization: Bearer tp-YOUR_TOKEN_PLAN_KEY

# Anthropic-compatible
x-api-key: tp-YOUR_TOKEN_PLAN_KEY
```

---

## Coverage

Token Plan covers **all current and upcoming models**:
- ✅ MiMo-V2.5-Pro (flagship)
- ✅ MiMo-V2.5 (omni-modal)
- ✅ MiMo-V2-Flash (efficient)
- ✅ MiMo-V2.5-TTS (voice synthesis) — **free for limited time**
- ✅ Voice Design
- ✅ Voice Cloning

---

## Subscription Tiers

| Tier | Credits | Price (CNY) | Notes |
|---|---|---|---|
| Max | 1.6 billion | ¥659 | Top tier |
| Other tiers available | Various | Various | See platform |

> **Orbit Program:** 100 trillion tokens distributed free within 30 days (April 28 - May 28, 2026). Apply at [100t.xiaomimimo.com](http://100t.xiaomimimo.com/)

---

## Usage Examples

### Python (OpenAI SDK — Token Plan)
```python
from openai import OpenAI

# Token Plan - Europe (Amsterdam)
client = OpenAI(
    api_key="tp-YOUR_TOKEN_PLAN_KEY",
    base_url="https://token-plan-ams.xiaomimimo.com/v1"
)

response = client.chat.completions.create(
    model="MiMo-V2.5-Pro",
    messages=[
        {"role": "system", "content": "You are MiMo, an AI assistant developed by Xiaomi."},
        {"role": "user", "content": "Explain quantum computing in simple terms"}
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

### curl (Token Plan — Europe)
```bash
curl -X POST https://token-plan-ams.xiaomimimo.com/v1/chat/completions \
  -H "Authorization: Bearer tp-YOUR_TOKEN_PLAN_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MiMo-V2.5-Pro",
    "messages": [
      {"role": "user", "content": "Write a sorting algorithm in Python"}
    ],
    "max_tokens": 4096,
    "temperature": 0.3,
    "stream": true
  }'
```

### Token Plan via Anthropic Protocol
```bash
curl -X POST https://token-plan-ams.xiaomimimo.com/anthropic/v1/messages \
  -H "x-api-key: tp-YOUR_TOKEN_PLAN_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MiMo-V2.5-Pro",
    "messages": [
      {"role": "user", "content": "Hello from Anthropic protocol!"}
    ],
    "max_tokens": 4096,
    "stream": true
  }'
```

---

## Integration with Agent Frameworks

MiMo Token Plan works seamlessly with:
- **OpenCode** — Coding agent
- **Hermes Agent** — General agent framework
- **KiloCode** — Code assistant
- **Cline** — VS Code extension
- **Blackbox** — Code intelligence

### Setting up in KiloCode/Cline
1. Set base URL to: `https://token-plan-ams.xiaomimimo.com/v1`
2. Set API key to your `tp-` token
3. Set model to: `MiMo-V2.5-Pro`

---

## Tips for Token Plan Users

1. **No 5-hour limits** — Token Plan removes throttling from free tier
2. **TTS is free** for a limited time across all tiers
3. **Monthly/annual subscriptions** available
4. **One first-purchase discount** per account
5. Use **temperature=0.3** for agentic/coding tasks
6. Use **temperature=0.8** for creative/writing tasks
7. Europe endpoint (`token-plan-ams`) recommended for EU users

---

## Where to Get Token Plan

Visit: [platform.xiaomimimo.com/#/token-plan](https://platform.xiaomimimo.com/#/token-plan)
