# Qwen Real-Time — Complete Code Examples

## 1. VAD Mode Voice Call (Python + DashScope SDK)

```python
# Dependencies: dashscope >= 1.23.9, pyaudio
import os, base64, time, pyaudio
from dashscope.audio.qwen_omni import MultiModality, OmniRealtimeCallback, OmniRealtimeConversation
import dashscope

region = 'intl'
base_domain = 'dashscope-intl.aliyuncs.com' if region == 'intl' else 'dashscope.aliyuncs.com'
url = f'wss://{base_domain}/api-ws/v1/realtime'
dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')

voice = 'Cherry'
model = 'qwen3.5-omni-plus-realtime'
instructions = "You are Xiaoyun, a personal assistant. Be humorous and witty."

class SimpleCallback(OmniRealtimeCallback):
    def __init__(self, pya):
        self.pya = pya
        self.out = None

    def on_open(self):
        self.out = self.pya.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)

    def on_event(self, response):
        if response['type'] == 'response.audio.delta':
            self.out.write(base64.b64decode(response['delta']))
        elif response['type'] == 'conversation.item.input_audio_transcription.completed':
            print(f"[User] {response['transcript']}")
        elif response['type'] == 'response.audio_transcript.done':
            print(f"[LLM] {response['transcript']}")

pya = pyaudio.PyAudio()
callback = SimpleCallback(pya)
conv = OmniRealtimeConversation(model=model, callback=callback, url=url)
conv.connect()
conv.update_session(
    output_modalities=[MultiModality.AUDIO, MultiModality.TEXT],
    voice=voice,
    instructions=instructions
)
mic = pya.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True)

print("Speak into the microphone (Ctrl+C to exit)...")
try:
    while True:
        audio_data = mic.read(3200, exception_on_overflow=False)
        conv.append_audio(base64.b64encode(audio_data).decode())
        time.sleep(0.01)
except KeyboardInterrupt:
    conv.close(); mic.close(); callback.out.close(); pya.terminate()
    print("\nConversation ended")
```

---

## 2. Manual Mode (Push-to-Talk) — DashScope SDK

```python
import os, base64, sys, threading, pyaudio
from dashscope.audio.qwen_omni import *
import dashscope

dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')

class MyCallback(OmniRealtimeCallback):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx

    def on_open(self):
        self.ctx['pya'] = pyaudio.PyAudio()
        self.ctx['out'] = self.ctx['pya'].open(
            format=pyaudio.paInt16, channels=1, rate=24000, output=True)

    def on_event(self, response):
        t = response['type']
        if t == 'response.audio.delta':
            self.ctx['out'].write(base64.b64decode(response['delta']))
        elif t == 'response.audio_transcript.delta':
            print(response['delta'], end='')
        elif t == 'response.done':
            self.ctx['resp_done'].set()

ctx = {'pya': None, 'out': None, 'conv': None, 'resp_done': threading.Event()}
conversation = OmniRealtimeConversation(
    model='qwen3.5-omni-plus-realtime',
    callback=MyCallback(ctx),
    url="wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime"
)
conversation.connect()
ctx['conv'] = conversation
conversation.update_session(
    output_modalities=[MultiModality.AUDIO, MultiModality.TEXT],
    voice='Cherry',
    enable_turn_detection=False,  # Manual mode
    instructions="You are a helpful assistant."
)

turn = 1
while True:
    print(f"\n--- Turn {turn} ---")
    input("Press Enter to start recording...")
    
    pya = pyaudio.PyAudio()
    stream = pya.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True)
    frames = []
    stop = threading.Event()
    
    def record():
        while not stop.is_set():
            frames.append(stream.read(3200, exception_on_overflow=False))
    
    t = threading.Thread(target=record, daemon=True)
    t.start()
    input("Press Enter to stop and send...")
    stop.set(); t.join(); stream.close(); pya.terminate()
    
    audio = b''.join(frames)
    for i in range(0, len(audio), 3200):
        conversation.append_audio(base64.b64encode(audio[i:i+3200]).decode())
    
    ctx['resp_done'].clear()
    conversation.commit()
    conversation.create_response()
    ctx['resp_done'].wait()
    print('\nResponse complete.')
    turn += 1
```

---

## 3. Web Search Enabled (Python)

```python
conv = OmniRealtimeConversation(model='qwen3.5-omni-plus-realtime', callback=callback, url=url)
conv.connect()
conv.update_session(
    output_modalities=[MultiModality.AUDIO, MultiModality.TEXT],
    voice='Tina',
    instructions="You are Xiao Yun, a personal assistant",
    enable_search=True,
    search_options={'enable_source': True}
)
# Rest is same as VAD mode...
```

---

## 4. Qwen-Omni Offline (HTTP) — Video Analysis

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3.5-omni-plus",
    messages=[{
        "role": "user",
        "content": [
            {"type": "video_url", "video_url": {"url": "https://example.com/video.mp4"}},
            {"type": "text", "text": "Describe this video in detail"}
        ]
    }],
    modalities=["text", "audio"],
    audio={"voice": "Tina", "format": "wav"},
    stream=True,
    stream_options={"include_usage": True},
)

for chunk in completion:
    if chunk.choices and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

---

## 5. Qwen-Omni Offline — Audio Analysis

```python
completion = client.chat.completions.create(
    model="qwen3.5-omni-plus",
    messages=[{
        "role": "user",
        "content": [
            {"type": "input_audio", "input_audio": {
                "data": "https://example.com/audio.wav", "format": "wav"
            }},
            {"type": "text", "text": "Transcribe and summarize this audio"}
        ]
    }],
    modalities=["text"],
    stream=True,
    stream_options={"include_usage": True},
)
```

---

## 6. Thinking Mode (Qwen3-Omni-Flash only)

```python
completion = client.chat.completions.create(
    model="qwen3-omni-flash",
    messages=[{"role": "user", "content": "Solve: what is 2^10?"}],
    extra_body={'enable_thinking': True},
    modalities=["text"],
    stream=True,
    stream_options={"include_usage": True},
)
```

---

## 7. Node.js Real-Time Client

```javascript
// omni_realtime_client.js
import OpenAI from "openai";
const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
});

const completion = await openai.chat.completions.create({
    model: "qwen3.5-omni-plus",
    messages: [{ role: "user", content: "Who are you?" }],
    stream: true,
    stream_options: { include_usage: true },
    modalities: ["text", "audio"],
    audio: { voice: "Tina", format: "wav" }
});

for await (const chunk of completion) {
    if (chunk.choices[0]?.delta?.content) {
        process.stdout.write(chunk.choices[0].delta.content);
    }
}
```

---

## 8. Java VAD Mode (DashScope SDK)

```java
OmniRealtimeParam param = OmniRealtimeParam.builder()
    .model("qwen3.5-omni-plus-realtime")
    .apikey(System.getenv("DASHSCOPE_API_KEY"))
    .url("wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime")
    .build();

OmniRealtimeConversation conversation = new OmniRealtimeConversation(param, new OmniRealtimeCallback() {
    @Override public void onOpen() { System.out.println("Connected"); }
    @Override public void onEvent(JsonObject event) { /* handle events */ }
    @Override public void onClose(int code, String reason) { /* cleanup */ }
});

conversation.connect();
conversation.updateSession(OmniRealtimeConfig.builder()
    .modalities(Arrays.asList(OmniRealtimeModality.AUDIO, OmniRealtimeModality.TEXT))
    .voice("Cherry")
    .enableTurnDetection(true)
    .build());
```
