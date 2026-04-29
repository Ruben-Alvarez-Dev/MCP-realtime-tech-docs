# MiMo Complete Code Examples

## 1. Basic Chat (Python — OpenAI SDK)

```python
from openai import OpenAI

# Standard pay-per-use
client = OpenAI(
    api_key="sk-xxx",
    base_url="https://api.xiaomimimo.com/v1"
)

# OR: Token Plan (Europe)
client = OpenAI(
    api_key="tp-xxx",
    base_url="https://token-plan-ams.xiaomimimo.com/v1"
)

response = client.chat.completions.create(
    model="MiMo-V2.5-Pro",
    messages=[
        {"role": "system", "content": "You are MiMo, an AI assistant developed by Xiaomi. Today's date: April 29 2026. Your knowledge cutoff date is December 2024."},
        {"role": "user", "content": "Explain quantum computing simply"}
    ],
    max_tokens=4096,
    temperature=0.8,
    top_p=0.95,
    stream=True
)

for chunk in response:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="")
```

---

## 2. Agentic Coding Task (Low Temperature)

```python
response = client.chat.completions.create(
    model="MiMo-V2.5-Pro",
    messages=[
        {"role": "system", "content": "You are MiMo, an AI assistant developed by Xiaomi."},
        {"role": "user", "content": "Create a Python REST API using FastAPI with CRUD operations for a todo app"}
    ],
    max_tokens=8192,
    temperature=0.3,  # Low temperature for coding/agent tasks
    top_p=0.95,
    stream=True
)
```

---

## 3. Thinking Mode (Reasoning)

```python
response = client.chat.completions.create(
    model="MiMo-V2.5-Pro",
    messages=[{"role": "user", "content": "What is the integral of x^2 * sin(x) dx?"}],
    max_tokens=4096,
    temperature=0.8,
    top_p=0.95,
    stream=True,
    extra_body={"chat_template_kwargs": {"enable_thinking": True}}
)

for chunk in response:
    delta = chunk.choices[0].delta
    if hasattr(delta, 'reasoning_content') and delta.reasoning_content:
        print(f"[Thinking] {delta.reasoning_content}", end="")
    if delta.content:
        print(f"[Answer] {delta.content}", end="")
```

---

## 4. Multimodal Input (MiMo-V2.5)

```python
# Image understanding
response = client.chat.completions.create(
    model="MiMo-V2.5",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": "https://example.com/photo.jpg"}},
            {"type": "text", "text": "What's in this image?"}
        ]
    }],
    max_tokens=2048,
    stream=True
)

# With base64 local image
import base64
with open("photo.jpg", "rb") as f:
    b64 = base64.b64encode(f.read()).decode()

response = client.chat.completions.create(
    model="MiMo-V2.5",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
            {"type": "text", "text": "Describe this image"}
        ]
    }],
    stream=True
)
```

---

## 5. curl — Standard API

```bash
curl -X POST https://api.xiaomimimo.com/v1/chat/completions \
  -H "api-key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MiMo-V2.5-Pro",
    "messages": [
      {"role": "system", "content": "You are MiMo, an AI assistant."},
      {"role": "user", "content": "Hello!"}
    ],
    "max_tokens": 4096,
    "temperature": 0.8,
    "stream": true
  }'
```

---

## 6. curl — Token Plan (Europe)

```bash
curl -X POST https://token-plan-ams.xiaomimimo.com/v1/chat/completions \
  -H "Authorization: Bearer tp-YOUR_TOKEN_PLAN_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MiMo-V2.5-Pro",
    "messages": [{"role": "user", "content": "Hello from Token Plan!"}],
    "stream": true
  }'
```

---

## 7. curl — Anthropic Protocol via Token Plan

```bash
curl -X POST https://token-plan-ams.xiaomimimo.com/anthropic/v1/messages \
  -H "x-api-key: tp-YOUR_TOKEN_PLAN_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MiMo-V2.5-Pro",
    "messages": [{"role": "user", "content": "Hello from Anthropic-compatible endpoint!"}],
    "max_tokens": 4096,
    "stream": true
  }'
```

---

## 8. Node.js

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
    apiKey: 'tp-YOUR_KEY',
    baseURL: 'https://token-plan-ams.xiaomimimo.com/v1'
});

const stream = await client.chat.completions.create({
    model: 'MiMo-V2.5-Pro',
    messages: [
        { role: 'system', content: 'You are MiMo, developed by Xiaomi.' },
        { role: 'user', content: 'Write a haiku about coding' }
    ],
    max_tokens: 256,
    temperature: 0.8,
    stream: true,
});

for await (const chunk of stream) {
    process.stdout.write(chunk.choices[0]?.delta?.content || '');
}
```

---

## 9. Self-Hosted (SGLang)

```bash
# Deploy MiMo-V2.5 locally (requires 8x GPU)
pip install sglang==0.5.6.post2.dev8005+pr.15207 \
    --index-url https://sgl-project.github.io/whl/pr/ \
    --extra-index-url https://pypi.org/simple

python3 -m sglang.launch_server \
    --model-path XiaomiMiMo/MiMo-V2.5 \
    --served-model-name mimo-v2.5 \
    --tp-size 8 --dp-size 2 \
    --enable-dp-attention \
    --moe-a2a-backend deepep \
    --context-length 262144 \
    --quantization fp8 \
    --enable-mtp \
    --host 0.0.0.0 --port 9001

# Then use locally:
# curl http://localhost:9001/v1/chat/completions -d '...'
```
