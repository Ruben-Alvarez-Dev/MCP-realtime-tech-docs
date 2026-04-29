# Qwen-Omni Offline HTTP API

> Source: https://www.alibabacloud.com/help/en/model-studio/qwen-omni

## Endpoint (OpenAI Compatible)

| Region | Base URL |
|---|---|
| International (Singapore) | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` |
| China (Beijing) | `https://dashscope.aliyuncs.com/compatible-mode/v1` |

## Key Requirements
- **`stream` MUST be `True`** — all requests require streaming
- OpenAI SDK 1.52.0+ (Python) or 4.68.0+ (Node.js)

## Text + Audio Output

```python
from openai import OpenAI
import os, base64, soundfile as sf, numpy as np

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3.5-omni-plus",
    messages=[{"role": "user", "content": "Who are you?"}],
    modalities=["text", "audio"],
    audio={"voice": "Tina", "format": "wav"},
    stream=True,
    stream_options={"include_usage": True},
)

audio_b64 = ""
for chunk in completion:
    if chunk.choices and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
    if chunk.choices and hasattr(chunk.choices[0].delta, 'audio') and chunk.choices[0].delta.audio:
        audio_b64 += chunk.choices[0].delta.audio.get("data", "")

if audio_b64:
    wav = np.frombuffer(base64.b64decode(audio_b64), dtype=np.int16)
    sf.write("output.wav", wav, samplerate=24000)
```

## Video Input

```python
completion = client.chat.completions.create(
    model="qwen3.5-omni-plus",
    messages=[{
        "role": "user",
        "content": [
            {"type": "video_url", "video_url": {"url": "https://example.com/video.mp4"}},
            {"type": "text", "text": "Describe this video"}
        ]
    }],
    modalities=["text", "audio"],
    audio={"voice": "Tina", "format": "wav"},
    stream=True,
)
```

**Limits:** Up to 512 files (3.5), 2GB/file, 1hr duration. Formats: MP4, AVI, MKV, MOV, FLV, WMV.

## Audio Input

```python
completion = client.chat.completions.create(
    model="qwen3.5-omni-plus",
    messages=[{
        "role": "user",
        "content": [
            {"type": "input_audio", "input_audio": {"data": "https://example.com/audio.wav", "format": "wav"}},
            {"type": "text", "text": "What is this audio about?"}
        ]
    }],
    modalities=["text"],
    stream=True,
)
```

**Limits:** 2048 files (3.5), 2GB/file, 3hr duration. Formats: AMR, WAV, 3GP, AAC, MP3.

## Image Input

```python
completion = client.chat.completions.create(
    model="qwen3.5-omni-plus",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}},
            {"type": "text", "text": "What's in this image?"}
        ]
    }],
    modalities=["text"],
    stream=True,
)
```

## Web Search (Qwen3.5-Omni only)

```python
completion = client.chat.completions.create(
    model="qwen3.5-omni-plus",
    messages=[{"role": "user", "content": "What's today's weather in Madrid?"}],
    stream=True,
    extra_body={
        "enable_search": True,
        "search_options": {"search_strategy": "agent"}
    }
)
```

## Thinking Mode (Qwen3-Omni-Flash only)

```python
completion = client.chat.completions.create(
    model="qwen3-omni-flash",
    messages=[{"role": "user", "content": "Explain relativity"}],
    extra_body={'enable_thinking': True},
    modalities=["text"],  # Audio not supported in thinking mode
    stream=True,
)
```

## Model Selection Guide

| Use Case | Model | Video Limit | Audio Limit | Special |
|---|---|---|---|---|
| Long video analysis | qwen3.5-omni-plus | 1 hour | 3 hours | Web search, voice control |
| Short video tagging | qwen3-omni-flash | 150 sec | 20 min | Thinking mode |
| Cost-sensitive | qwen3-omni-flash | 150 sec | 20 min | Cheapest |

## Token Conversion

- **Audio:** 3.5: `seconds × 7` | Flash: `seconds × 12.5` | Turbo: `seconds × 25`
- **Images:** 1 token per 32×32 (3.5/Flash), 28×28 (Turbo). Min 4, max 1280.
- **Video:** `video_tokens + audio_tokens` (complex calculation, see full docs)
