# Qwen Real-Time Ecosystem — Complete Guide

> Last updated: April 2026  
> Source: Alibaba Cloud Model Studio (DashScope)

## Table of Contents
1. [What is Qwen Real-Time?](#what-is-qwen-real-time)
2. [Model Family Overview](#model-family-overview)
3. [API Endpoints](#api-endpoints)
4. [Quick Start: Which Model to Use?](#quick-start)

---

## What is Qwen Real-Time?

Qwen offers a suite of **multimodal real-time models** capable of processing streaming audio, images, video, and text simultaneously, and responding with **text and audio in real time** via WebSocket connections.

Two main API modes exist:
- **Realtime API** — WebSocket-based, streaming audio/video input, real-time audio output. For voice/video calls, live agents.
- **Offline API** — HTTP-based, batch processing of audio/video/image/text inputs with streaming text+audio output.

---

## Model Family Overview

| Model | Type | Input | Output | Context | Languages In | Languages Out | Voices | Key Feature |
|---|---|---|---|---|---|---|---|---|
| **qwen3.5-omni-plus-realtime** | Realtime WS | Audio + Images | Text + Audio | 120 min session | 113 langs + 21 dialects | 36 langs + 7 dialects | 55 | Latest flagship. Web search, semantic interruption, voice control, voice cloning |
| **qwen3-omni-flash-realtime** | Realtime WS | Audio + Images | Text + Audio | 120 min session | 10 langs + 9 dialects | 10 langs + 9 dialects | 17-49 | Thinking mode support, cost-effective |
| **qwen3.5-omni-plus** | Offline HTTP | Audio, Video, Image, Text | Text + Audio | 256K | 113 langs + 21 dialects | 36 langs + 7 dialects | 55 | Long video (1hr), long audio (3hr), web search |
| **qwen3-omni-flash** | Offline HTTP | Audio, Video, Image, Text | Text + Audio | 256K | 10 langs + 9 dialects | 10 langs + 9 dialects | 17-49 | Thinking mode, short video/audio |
| **qwen3-tts-vc-realtime** | TTS Realtime WS | Text + Voice ref | Audio | - | 10 languages | 10 languages | Custom | 3-second voice cloning |
| **qwen3-tts-vd-realtime** | TTS Realtime WS | Text + Prompt | Audio | - | Multi-language | Multi-language | Custom | Voice design from text description |

### Deprecated Models
- `qwen-omni-turbo-realtime` — No longer updated, limited features. Migrate to qwen3.5-omni or qwen3-omni-flash.

---

## API Endpoints

### Realtime API (WebSocket)
| Region | Endpoint |
|---|---|
| International (Singapore) | `wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime` |
| China (Beijing) | `wss://dashscope.aliyuncs.com/api-ws/v1/realtime` |

**Connection:** Append `?model=<model_name>` as query parameter.  
**Auth:** `Authorization: Bearer <DASHSCOPE_API_KEY>` header.

### Offline API (HTTP — OpenAI Compatible)
| Region | Endpoint |
|---|---|
| International (Singapore) | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` |
| China (Beijing) | `https://dashscope.aliyuncs.com/compatible-mode/v1` |

### TTS Voice Design/Cloning API (HTTP)
| Region | Endpoint |
|---|---|
| International (Singapore) | `https://dashscope-intl.aliyuncs.com/api/v1/services/audio/tts/customization` |
| China (Beijing) | `https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization` |

### TTS Realtime API (WebSocket)
Same WebSocket endpoint as Realtime API — uses different models (`qwen3-tts-vc-realtime-*` or `qwen3-tts-vd-realtime-*`).

---

## Quick Start: Which Model to Use?

| Scenario | Recommended Model | API Mode |
|---|---|---|
| Voice/video call with AI | `qwen3.5-omni-plus-realtime` | Realtime WS |
| Cost-sensitive voice chat | `qwen3-omni-flash-realtime` | Realtime WS |
| Long video analysis (up to 1hr) | `qwen3.5-omni-plus` | Offline HTTP |
| Short video/audio analysis | `qwen3-omni-flash` | Offline HTTP |
| Voice cloning TTS | `qwen3-tts-vc-realtime-2025-11-27` | TTS Realtime WS |
| Voice design from text | `qwen3-tts-vd-realtime-2025-12-16` | TTS Realtime WS |
| Web search + voice | `qwen3.5-omni-plus-realtime` | Realtime WS |

---

## Key Capabilities (Qwen3.5-Omni-Realtime)

1. **Semantic Interruption** — Detects real conversation intent, ignores filler sounds and background noise
2. **Web Search** — Model autonomously decides when to search for real-time info
3. **Voice Control** — Say "speak faster", "speak louder", "speak cheerfully" to control output
4. **Voice Cloning** — Upload a voice sample to customize the AI's voice
5. **113 Languages/Dialects** for speech recognition
6. **36 Languages/Dialects** for speech synthesis
7. **55 Voices** (47 multilingual + 8 dialect-specific)
8. **Server VAD** or **Manual (push-to-talk)** modes
9. **Image Input** — Send frames from video streams alongside audio
10. **Session Duration** — Up to 120 minutes per WebSocket session

---

## Files in this Directory

| File | Content |
|---|---|
| [00-OVERVIEW.md](./00-OVERVIEW.md) | This overview |
| [01-REALTIME-WEBSOCKET-API.md](./01-REALTIME-WEBSOCKET-API.md) | Full WebSocket API reference, interaction flows, VAD/Manual modes |
| [02-OFFLINE-HTTP-API.md](./02-OFFLINE-HTTP-API.md) | HTTP API for audio/video/image analysis |
| [03-QWEN35-OMNI-BLOG.md](./03-QWEN35-OMNI-BLOG.md) | Architecture, benchmarks, Qwen3.5-Omni blog content |
| [04-QWEN3-TTS.md](./04-QWEN3-TTS.md) | TTS Voice Design & Voice Cloning API |
| [05-CLIENT-SERVER-EVENTS.md](./05-CLIENT-SERVER-EVENTS.md) | Complete client/server event reference |
| [06-VOICES.md](./06-VOICES.md) | Complete voice list for all models |
| [07-CODE-EXAMPLES.md](./07-CODE-EXAMPLES.md) | Working code examples (Python, Node.js, Java, curl) |
