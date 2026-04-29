# Qwen Real-Time Client & Server Events Reference

> Source: https://www.alibabacloud.com/help/en/model-studio/client-events

## Client Events (You Send)

### session.update
Configure the session. **Send this first** after connecting.

```json
{
    "type": "session.update",
    "session": {
        "modalities": ["text", "audio"],
        "voice": "Cherry",
        "input_audio_format": "pcm",
        "output_audio_format": "pcm",
        "instructions": "System prompt here",
        "turn_detection": {
            "type": "server_vad",
            "threshold": 0.5,
            "silence_duration_ms": 800
        },
        "enable_search": true,
        "search_options": { "enable_source": true },
        "temperature": 0.9,
        "top_p": 1.0,
        "top_k": 50,
        "max_tokens": 16384,
        "repetition_penalty": 1.05,
        "presence_penalty": 0.0,
        "seed": 1314
    }
}
```

### input_audio_buffer.append
Append Base64-encoded 16-bit/16kHz/mono PCM audio:
```json
{ "type": "input_audio_buffer.append", "audio": "UklGRi4AAABXQVZFZm10..." }
```

### input_image_buffer.append
Append Base64-encoded JPG image (≤500KB, 480p-720p recommended, max 1fps):
```json
{ "type": "input_image_buffer.append", "image": "/9j/4AAQSkZJRg..." }
```
> Must send audio first before sending images.

### input_audio_buffer.commit
Commit audio (+ images) buffer. Creates user message. **Manual mode only.**
```json
{ "type": "input_audio_buffer.commit" }
```

### input_audio_buffer.clear
Clear the audio buffer:
```json
{ "type": "input_audio_buffer.clear" }
```

### response.create
Request model response. **Manual mode only.**
```json
{ "type": "response.create" }
```

### response.cancel
Cancel ongoing response:
```json
{ "type": "response.cancel" }
```

---

## Server Events (You Receive)

### Session Events
| Event | Fields | Description |
|---|---|---|
| `session.created` | session.id | Session initialized |
| `session.updated` | session (full config) | Configuration applied |

### Audio Buffer Events
| Event | Fields | Description |
|---|---|---|
| `input_audio_buffer.speech_started` | audio_start_ms | VAD detected speech start |
| `input_audio_buffer.speech_stopped` | audio_end_ms | VAD detected speech end |
| `input_audio_buffer.committed` | item_id | Buffer committed |
| `input_audio_buffer.cleared` | - | Buffer cleared |

### Response Events
| Event | Key Fields | Description |
|---|---|---|
| `response.created` | response.id | Response started |
| `response.output_item.added` | item | Output item added |
| `conversation.item.created` | item | Conversation item created |
| `response.content_part.added` | part | Content part added |
| `response.text.delta` | delta | Streaming text chunk |
| `response.audio_transcript.delta` | delta | Streaming audio transcript |
| `response.audio.delta` | delta | Streaming audio (Base64 PCM) |
| `response.text.done` | text | Text complete |
| `response.audio_transcript.done` | transcript | Transcript complete |
| `response.audio.done` | - | Audio complete |
| `response.content_part.done` | part | Content part done |
| `response.output_item.done` | item | Output item done |
| `response.done` | response (with usage) | **Full response complete** |

### Error Event
```json
{
    "type": "error",
    "error": { "code": "...", "message": "..." }
}
```

---

## Response.usage Format (with Web Search)
```json
{
    "usage": {
        "total_tokens": 2937,
        "input_tokens": 2554,
        "output_tokens": 383,
        "input_tokens_details": { "text_tokens": 2512, "audio_tokens": 42 },
        "output_tokens_details": { "text_tokens": 90, "audio_tokens": 293 },
        "plugins": {
            "search": { "count": 1, "strategy": "agent" }
        }
    }
}
```
