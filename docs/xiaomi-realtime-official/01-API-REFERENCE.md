# MiMo API Complete Reference

> Source: https://platform.xiaomimimo.com/docs/api/chat/openai-api

## Endpoints

### Standard Pay-Per-Use
```
POST https://api.xiaomimimo.com/v1/chat/completions
```

### Token Plan (Subscription)

**OpenAI-compatible endpoints:**
| Region | URL |
|---|---|
| China | `https://token-plan-cn.xiaomimimo.com/v1` |
| Europe (Amsterdam) | `https://token-plan-ams.xiaomimimo.com/v1` |

**Anthropic-compatible endpoints:**
| Region | URL |
|---|---|
| Europe (Amsterdam) | `https://token-plan-ams.xiaomimimo.com/anthropic` |

---

## Authentication

### Method 1: api-key header
```
api-key: $MIMO_API_KEY
Content-Type: application/json
```

### Method 2: Bearer token
```
Authorization: Bearer $MIMO_API_KEY
Content-Type: application/json
```

> Token Plan keys start with `tp-`, standard keys start with `sk-`.

---

## Available Models

| Model Name | Description | Context | Active Params |
|---|---|---|---|
| `MiMo-V2.5-Pro` | Flagship agent model | 1M | 42B |
| `MiMo-V2.5` | Omni-modal (text+image+video+audio) | 1M | 15B |
| `MiMo-V2-Flash` | Efficient reasoning/coding | 256K | 15B |

---

## Request Body (OpenAI Compatible)

```json
{
    "model": "MiMo-V2.5-Pro",
    "messages": [
        {
            "role": "system",
            "content": "You are MiMo, an AI assistant developed by Xiaomi."
        },
        {
            "role": "user",
            "content": "Hello, what can you do?"
        }
    ],
    "max_tokens": 4096,
    "temperature": 0.8,
    "top_p": 0.95,
    "stream": true,
    "chat_template_kwargs": {
        "enable_thinking": true
    }
}
```

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| model | string | required | Model name |
| messages | array | required | Chat messages array |
| max_tokens | int | - | Max tokens to generate |
| temperature | float | 0.8 | Sampling temperature (0.3 for agentic, 0.8 for creative) |
| top_p | float | 0.95 | Nucleus sampling threshold |
| stream | boolean | false | Enable streaming output |
| chat_template_kwargs | object | - | `enable_thinking: true` for thinking mode |

### Multimodal Input (MiMo-V2.5)

```json
{
    "model": "MiMo-V2.5",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": { "url": "https://example.com/image.jpg" }
                },
                {
                    "type": "text",
                    "text": "Describe this image"
                }
            ]
        }
    ],
    "stream": true
}
```

---

## Response Format (Non-Streaming)

```json
{
    "id": "chatcmpl-xxx",
    "object": "chat.completion",
    "created": 1718624400,
    "model": "MiMo-V2.5-Pro",
    "choices": [{
        "index": 0,
        "message": {
            "role": "assistant",
            "content": "Hello! I'm MiMo...",
            "reasoning_content": "Let me think about this..."
        },
        "finish_reason": "stop"
    }],
    "usage": {
        "prompt_tokens": 50,
        "completion_tokens": 100,
        "total_tokens": 150
    }
}
```

---

## Response Format (Streaming)

```
data: {"id":"chatcmpl-xxx","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"role":"assistant"},"finish_reason":null}]}
data: {"id":"chatcmpl-xxx","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"content":"Hello"},"finish_reason":null}]}
data: {"id":"chatcmpl-xxx","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"content":"!"},"finish_reason":null}]}
data: {"id":"chatcmpl-xxx","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"content":""},"finish_reason":"stop"}]}
```

---

## Thinking Mode

Enable reasoning content in responses:
```json
{
    "model": "MiMo-V2.5-Pro",
    "messages": [...],
    "chat_template_kwargs": {
        "enable_thinking": true
    }
}
```

Response includes `reasoning_content` field alongside `content`.

---

## Tool Use / Function Calling

MiMo models support function calling. In thinking mode with multi-turn tool calls, the model returns a `reasoning_content` field alongside `tool_calls`. **You must persist all history `reasoning_content`** in the messages array of subsequent requests.

---

## Pricing (MiMo-V2.5-Pro)

| Tier | Input (per 1M tokens) | Output (per 1M tokens) | Cache Write | Cache Read |
|---|---|---|---|---|
| Up to 256K context | $1 | $3 | $0.20 | $0 |
| 256K-1M context | $2 | $6 | $0.40 | $0 |

> Cache Write is temporarily free.

---

## Code Examples

### Python (OpenAI SDK)
```python
from openai import OpenAI

# Standard API
client = OpenAI(
    api_key="sk-xxx",
    base_url="https://api.xiaomimimo.com/v1"
)

# Token Plan (Europe)
client = OpenAI(
    api_key="tp-xxx",
    base_url="https://token-plan-ams.xiaomimimo.com/v1"
)

response = client.chat.completions.create(
    model="MiMo-V2.5-Pro",
    messages=[
        {"role": "system", "content": "You are MiMo, an AI assistant developed by Xiaomi."},
        {"role": "user", "content": "Write a Python quicksort"}
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

### Node.js
```javascript
import OpenAI from 'openai';

const client = new OpenAI({
    apiKey: 'tp-xxx',
    baseURL: 'https://token-plan-ams.xiaomimimo.com/v1'
});

const stream = await client.chat.completions.create({
    model: 'MiMo-V2.5-Pro',
    messages: [{ role: 'user', content: 'Hello!' }],
    stream: true,
});

for await (const chunk of stream) {
    process.stdout.write(chunk.choices[0]?.delta?.content || '');
}
```

### curl (Token Plan)
```bash
curl -X POST https://token-plan-ams.xiaomimimo.com/v1/chat/completions \
  -H "Authorization: Bearer tp-YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MiMo-V2.5-Pro",
    "messages": [{"role": "user", "content": "Hello!"}],
    "stream": true
  }'
```

### curl (Anthropic-compatible via Token Plan)
```bash
curl -X POST https://token-plan-ams.xiaomimimo.com/anthropic/v1/messages \
  -H "x-api-key: tp-YOUR_TOKEN" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MiMo-V2.5-Pro",
    "messages": [{"role": "user", "content": "Hello!"}],
    "max_tokens": 4096,
    "stream": true
  }'
```

---

## System Prompts (Recommended)

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
