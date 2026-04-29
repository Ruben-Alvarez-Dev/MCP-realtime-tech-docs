# Qwen3.5-Omni Architecture & Benchmarks

> Source: https://qwen.ai/blog?id=qwen3.5-omni

## Architecture: Thinker-Talker

Qwen3.5-Omni uses a **Thinker-Talker** architecture:
- **Thinker** — Processes visual (ViT) and audio (AuT) signals, interleaved with text using **TMRoPE** positional encoding. Outputs text.
- **Talker** — Receives multimodal inputs + Thinker's text output → generates contextual speech using **ARIA** (Adaptive Rate Interleave Alignment)
- Both use **Hybrid-Attention MoE** architecture

### Key Innovation: ARIA
Solves text/speech token encoding efficiency differences that cause omissions, misreadings, or unclear pronunciation. Dynamically aligns text and speech units.

---

## Model Sizes

| Size | Context | Audio Input | AV Input (1fps) |
|---|---|---|---|
| Plus | 256K | 10+ hours | 400+ sec (720P) |
| Flash | 256K | - | - |
| Light | 256K | - | - |

Pretrained on **100+ million hours** of audio-visual data.

---

## Qwen3.5-Omni vs Qwen3-Omni

| Feature | Qwen3-Omni | Qwen3.5-Omni |
|---|---|---|
| Backbone | MoE | **Hybrid-MoE** |
| Sequence Length | 32K | **256K** |
| Captioning | Audio only | **Audio-Visual** |
| Semantic Interruption | ❌ | ✅ |
| WebSearch/Tool | ❌ | ✅ |
| Voice Control | ❌ | ✅ |
| Voice Clone | ❌ | ✅ |
| Talker | Dual-Track | **ARIA Interleave** |
| Speech Recognition | 11 langs + 8 dialects | **74 langs + 39 dialects** |
| Speech Synthesis | - | **29 langs + 7 dialects** |

---

## Benchmarks

### Audio-Visual
| Benchmark | Gemini-3.1 Pro | Qwen3.5-Flash | Qwen3.5-Plus |
|---|---|---|---|
| DailyOmni | 82.7 | 81.8 | **84.6** |
| VideoMME (audio) | **89.0** | 79.3 | 83.7 |
| OmniGAIA | **68.9** | 33.9 | 57.2 |

### Audio
| Benchmark | Gemini-3.1 Pro | Qwen3.5-Plus |
|---|---|---|
| MMAU | 81.1 | **82.2** |
| VoiceBench | 88.9 | **93.1** |
| Fleurs ASR (top60) | 7.32 | **6.55** |

### Text
| Benchmark | Qwen3.5-Plus |
|---|---|
| MMLU-Pro | 85.9 |
| GPQA | 83.9 |
| LiveCodeBench v6 | 65.6 |

### Speech Generation (vs competitors)
| Stability (WER ↓) | ElevenLabs | Gemini-2.5 Pro | **Qwen3.5-Plus** |
|---|---|---|---|
| Public Multilingual (20 lang) | 12.62 | 2.72 | **2.06** |
| Custom Voice Chinese | 13.08 | 2.42 | **1.07** |

---

## Recommended Usage (Offline API)

| Scenario | Max Pixels | Video Duration | Prompt |
|---|---|---|---|
| Low Cost / Moderation | 230K | ≤60 min | Short custom prompt |
| Long Video Segmentation | 921K-2M | ≤60 min | Short custom prompt |
| Detailed AV Description | 921K-2M | ≤4 min | Fixed structured prompt |
| Multi-Speaker/Complex | 2M | ≤2 min | Fixed structured prompt |
