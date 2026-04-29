# Qwen3-TTS — Voice Design & Voice Cloning API

> Source: https://qwen.ai/blog?id=qwen3-tts-vc-voicedesign

## Overview

Qwen3-TTS offers two powerful capabilities via the Qwen API:
1. **Voice Design (VD)** — Create voices from natural language descriptions
2. **Voice Cloning (VC)** — Clone a voice from a 3-second audio sample

---

## Models

| Model | Purpose | Access |
|---|---|---|
| `qwen3-tts-vd-realtime-2025-12-16` | Voice Design | Qwen API |
| `qwen3-tts-vc-realtime-2025-11-27` | Voice Cloning | Qwen API |

---

## Voice Design — Create Custom Voices

Create any voice from a text description:

```python
import requests, base64, os

api_key = os.getenv("DASHSCOPE_API_KEY")
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "qwen-voice-design",
    "input": {
        "action": "create",
        "target_model": "qwen3-tts-vd-realtime-2025-12-16",
        "voice_prompt": "A composed middle-aged male announcer with a deep, rich voice, steady speaking speed, clear articulation",
        "preview_text": "Welcome to the evening news.",
        "preferred_name": "announcer",
        "language": "en"
    },
    "parameters": {
        "sample_rate": 24000,
        "response_format": "wav"
    }
}

url = "https://dashscope-intl.aliyuncs.com/api/v1/services/audio/tts/customization"
response = requests.post(url, headers=headers, json=data, timeout=60)

if response.status_code == 200:
    result = response.json()
    voice_name = result["output"]["voice"]
    audio_b64 = result["output"]["preview_audio"]["data"]
    
    # Save preview audio
    with open(f"{voice_name}_preview.wav", 'wb') as f:
        f.write(base64.b64decode(audio_b64))
    print(f"Voice created: {voice_name}")
```

### Voice Design Controls
- **Acoustic attributes**: Pitch, speed, volume, timbre
- **Persona/role-play**: Character descriptions, backgrounds
- **Emotion**: Happy, sad, angry, calm, etc.
- **Language**: Chinese, English, and more

---

## Voice Cloning — 3-Second Clone

Clone a voice from a short audio sample, then generate speech in 10 languages:

```python
import requests, base64, pathlib, os

api_key = os.getenv("DASHSCOPE_API_KEY")
voice_file = "voice.mp3"

# 1. Create cloned voice
file_bytes = pathlib.Path(voice_file).read_bytes()
b64 = base64.b64encode(file_bytes).decode()

url = "https://dashscope-intl.aliyuncs.com/api/v1/services/audio/tts/customization"
payload = {
    "model": "qwen-voice-enrollment",
    "input": {
        "action": "create",
        "target_model": "qwen3-tts-vc-realtime-2025-11-27",
        "preferred_name": "my_voice",
        "audio": {"data": f"data:audio/mpeg;base64,{b64}"}
    }
}

resp = requests.post(url, json=payload, 
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})
voice_name = resp.json()["output"]["voice"]
print(f"Cloned voice: {voice_name}")
```

### Supported Languages for Cloning
Chinese, English, German, Italian, Portuguese, Spanish, Japanese, Korean, French, Russian

---

## TTS Realtime Streaming (WebSocket)

Stream generated speech in real time via WebSocket:

```python
import pyaudio, os, base64, time, threading
import dashscope
from dashscope.audio.qwen_tts_realtime import QwenTtsRealtime, QwenTtsRealtimeCallback, AudioFormat

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

class MyCallback(QwenTtsRealtimeCallback):
    def __init__(self):
        self.complete = threading.Event()
        self.player = pyaudio.PyAudio()
        self.stream = self.player.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)
    
    def on_open(self):
        print('[TTS] Connected')
    
    def on_event(self, response):
        t = response.get('type', '')
        if t == 'response.audio.delta':
            self.stream.write(base64.b64decode(response['delta']))
        elif t == 'session.finished':
            self.complete.set()
    
    def on_close(self, code, msg):
        self.stream.close()
        self.player.terminate()

tts = QwenTtsRealtime(
    model="qwen3-tts-vc-realtime-2025-11-27",
    callback=MyCallback(),
    url="wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime"
)
tts.connect()

# Use voice_name from cloning step
tts.update_session(
    voice="your_cloned_voice_name",
    response_format=AudioFormat.PCM_24000HZ_MONO_16BIT,
    mode='server_commit'
)

for text in ["Hello!", "How are you?", "Goodbye!"]:
    tts.append_text(text)
    time.sleep(0.1)

tts.finish()
```

---

## Voice Reuse — Multi-Turn, Multi-Role Dialogues

Voices can be stored and reused for multi-role conversations:

```python
# Define multiple voices with descriptions
voices = {
    "narrator": "沉稳、客观、略带叙事感的女播音腔",
    "xiaolin": "25岁男性上班族，声音清亮但时常犹豫",
    "yujie": "成熟性感的御姐音色，声音略带磁性且沉稳"
}

# Each voice can be used in different turns with different text
# The system maintains voice consistency across the conversation
```

---

## Performance

| Metric | Value |
|---|---|
| Streaming latency | ~97ms end-to-end |
| Architecture | Dual-track hybrid streaming |
| Voice clone minimum | 3 seconds |
| Languages (VC) | 10 |
| Sample rate | 24kHz |

### Benchmarks vs Competitors

**Voice Clone Stability (WER ↓ = better):**
| Public Multilingual (20 langs) | ElevenLabs: 10.29 | Minimax: 2.52 | **Qwen3.5-Omni-Plus: 1.87** |
| Inhouse Multilingual (9 langs) | - | - | **Qwen3.5-Omni-Plus: 7.04** |

**Voice Clone Similarity (↑ = better):**
| Public Multilingual | ElevenLabs: 0.65 | Minimax: 0.76 | **Qwen3.5-Omni-Plus: 0.79** |
