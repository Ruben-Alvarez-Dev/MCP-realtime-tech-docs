# Qwen Real-Time WebSocket API — Complete Reference

> Source: https://www.alibabacloud.com/help/en/model-studio/realtime

## Connection

### WebSocket Endpoints
| Region | URL |
|---|---|
| International (Singapore) | `wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime` |
| China (Beijing) | `wss://dashscope.aliyuncs.com/api-ws/v1/realtime` |

### Connect via Native WebSocket
```python
import websocket, json, os

API_KEY = os.getenv("DASHSCOPE_API_KEY")
API_URL = "wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime?model=qwen3.5-omni-plus-realtime"

headers = ["Authorization: Bearer " + API_KEY]

def on_open(ws):
    print(f"Connected to server")
def on_message(ws, message):
    data = json.loads(message)
    print("Received:", json.dumps(data, indent=2))
def on_error(ws, error):
    print("Error:", error)

ws = websocket.WebSocketApp(API_URL, header=headers,
    on_open=on_open, on_message=on_message, on_error=on_error)
ws.run_forever()
```

### Connect via DashScope SDK
```python
import os, json
from dashscope.audio.qwen_omni import OmniRealtimeConversation, OmniRealtimeCallback
import dashscope

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

class PrintCallback(OmniRealtimeCallback):
    def on_open(self):
        print("Connected!")
    def on_event(self, response):
        print(json.dumps(response, indent=2))
    def on_close(self, code, msg):
        print(f"Closed: code={code}, msg={msg}")

conversation = OmniRealtimeConversation(
    model="qwen3.5-omni-plus-realtime",
    callback=PrintCallback(),
    url="wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime"
)
conversation.connect()
```

---

## Session Configuration

Send `session.update` as the **first event** after connecting:

```json
{
    "event_id": "event_unique_id",
    "type": "session.update",
    "session": {
        "modalities": ["text", "audio"],
        "voice": "Cherry",
        "input_audio_format": "pcm",
        "output_audio_format": "pcm",
        "instructions": "You are a helpful AI assistant...",
        "turn_detection": {
            "type": "server_vad",
            "threshold": 0.5,
            "silence_duration_ms": 800
        },
        "enable_search": true,
        "search_options": { "enable_source": true },
        "seed": 1314,
        "max_tokens": 16384,
        "repetition_penalty": 1.05,
        "presence_penalty": 0.0,
        "top_k": 50,
        "top_p": 1.0,
        "temperature": 0.9
    }
}
```

### Parameter Reference

| Parameter | Type | Default | Range | Notes |
|---|---|---|---|---|
| modalities | array | ["text","audio"] | ["text"] or ["text","audio"] | Output modalities |
| voice | string | "Tina" (3.5) / "Cherry" (3-flash) | See voices list | Voice for audio output |
| input_audio_format | string | "pcm" | "pcm" only | 16-bit, 16kHz, mono PCM |
| output_audio_format | string | "pcm" | "pcm" only | 24kHz output |
| instructions | string | - | Any | System prompt / role |
| turn_detection | object/null | server_vad | See VAD config | null = manual mode |
| enable_search | boolean | false | true/false | **Qwen3.5 only** — web search |
| search_options | object | - | enable_source: bool | Return search sources |
| temperature | float | 0.9 | [0, 2) | Sampling temperature |
| top_p | float | 1.0 | (0, 1.0] | Nucleus sampling |
| top_k | int | 50 | >= 0 | Candidate set size |
| max_tokens | int | model max | - | Max output tokens |
| repetition_penalty | float | 1.05 | > 0 | Repetition control |
| presence_penalty | float | 0.0 | [-2.0, 2.0] | Diversity control |
| seed | int | -1 | 0 to 2^31-1 | Deterministic output |

### VAD Configuration (turn_detection)

| Parameter | Type | Default | Range | Notes |
|---|---|---|---|---|
| type | string | "server_vad" | "server_vad" | Must be server_vad |
| threshold | float | 0.5 | [-1.0, 1.0] | Lower = more sensitive |
| silence_duration_ms | int | 800 | [200, 6000] | Silence to trigger response |

---

## Interaction Modes

### Mode 1: VAD (Voice Activity Detection) — Automatic

Server automatically detects speech start/end. Best for voice calls.

**Flow:**
1. Server detects speech start → `input_audio_buffer.speech_started`
2. Client sends `input_audio_buffer.append` (audio) + optionally `input_image_buffer.append` (images)
3. Server detects speech end → `input_audio_buffer.speech_stopped`
4. Server commits audio → `input_audio_buffer.committed`
5. Server creates response → streams `response.audio.delta` + `response.audio_transcript.delta`
6. Response complete → `response.done`

### Mode 2: Manual (Push-to-Talk) — Client Controlled

Client explicitly sends commit + create_response. Best for chat apps.

**Flow:**
1. Client sends `input_audio_buffer.append` (audio)
2. Client optionally sends `input_image_buffer.append` (images)
3. Client sends `input_audio_buffer.commit` → Server: `input_audio_buffer.committed`
4. Client sends `response.create`
5. Server streams response
6. Response complete → `response.done`

**Set `turn_detection` to `null` to enable manual mode.**

---

## Sending Audio

Audio must be **16-bit, 16kHz, mono PCM**, Base64-encoded. Send in 3200-byte chunks (100ms at 16kHz):

```json
{
    "type": "input_audio_buffer.append",
    "audio": "<base64_encoded_pcm>"
}
```

## Sending Images

Images from video streams or local files. Must be JPG/JPEG, ≤500KB, recommended 480p-720p, max 1 FPS:

```json
{
    "type": "input_image_buffer.append",
    "image": "<base64_encoded_jpg>"
}
```

> **Important:** You MUST send at least one `input_audio_buffer.append` before sending images.

## Manual Mode: Commit Audio Buffer

```json
{ "type": "input_audio_buffer.commit" }
```

## Manual Mode: Request Response

```json
{ "type": "response.create" }
```

## Cancel Response

```json
{ "type": "response.cancel" }
```

## Clear Audio Buffer

```json
{ "type": "input_audio_buffer.clear" }
```

---

## Server Events (What You Receive)

| Event | Description |
|---|---|
| `session.created` | Session initialized |
| `session.updated` | Config updated |
| `input_audio_buffer.speech_started` | VAD detected speech start |
| `input_audio_buffer.speech_stopped` | VAD detected speech end |
| `input_audio_buffer.committed` | Audio buffer committed |
| `response.created` | Response started |
| `response.output_item.added` | New output item |
| `conversation.item.created` | Conversation item created |
| `response.content_part.added` | New content part |
| `response.text.delta` | Streaming text |
| `response.audio_transcript.delta` | Streaming transcript of audio |
| `response.audio.delta` | Streaming audio (Base64 PCM) |
| `response.text.done` | Text complete |
| `response.audio_transcript.done` | Audio transcript complete |
| `response.audio.done` | Audio generation complete |
| `response.content_part.done` | Content part complete |
| `response.output_item.done` | Output item complete |
| `response.done` | Full response complete |
| `error` | Error occurred |

---

## Billing

### Token Conversion
- **Qwen3.5-Omni-Realtime:** `tokens = audio_seconds × 7`
- **Qwen3-Omni-Flash-Realtime:** `tokens = audio_seconds × 12.5`
- **Qwen-Omni-Turbo-Realtime:** `tokens = audio_seconds × 25`
- **Images:** 1 token per 32×32 pixels (3.5/Flash), 28×28 pixels (Turbo)
- Audio < 1 second = 1 second minimum

### Session Limits
- Max session duration: **120 minutes**
- Qwen3.5-Omni-Realtime is in **preview** — model invocation is temporarily free (tool calling still incurs fees)

---

## Web Search (Qwen3.5-Realtime Only)

Enable in `session.update`:
```json
{
    "session": {
        "enable_search": true,
        "search_options": { "enable_source": true }
    }
}
```

The model **autonomously decides** whether to search. Response includes search metrics in `usage.plugins.search`.

---

## Voice Control

In Qwen3.5-Omni-Realtime, you can control the voice by saying:
- "Speak faster" / "Speak slower"
- "Speak louder" / "Speak quieter"  
- "Speak cheerfully" / "Speak calmly"
