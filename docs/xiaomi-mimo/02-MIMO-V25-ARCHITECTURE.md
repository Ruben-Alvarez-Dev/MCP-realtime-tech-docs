# MiMo-V2.5 Architecture — Technical Deep Dive

> Source: HuggingFace, Xiaomi MiMo Platform

## Architecture Overview

MiMo-V2.5 is a **native omnimodal MoE model** built on MiMo-V2-Flash backbone with dedicated vision and audio encoders.

### Model Comparison

| Component | MiMo-V2.5-Pro | MiMo-V2.5 | MiMo-V2-Flash |
|---|---|---|---|
| **Total Parameters** | 1.02T | 310B | 309B |
| **Active Parameters** | 42B | 15B | 15B |
| **Hidden Size** | 6144 | 4096 | 4096 |
| **Layers** | 70 (1 dense + 69 MoE) | 48 (1 dense + 47 MoE) | 48 |
| **Full Attention Layers** | 10 | 9 | - |
| **SWA Layers** | 60 | 39 | - |
| **Attention Heads** | 128 | 64 | 64 |
| **KV Heads** | 8 (GQA) | 8/4 (GA/SWA) | 8 |
| **Routed Experts** | 384 | 256 | 256 |
| **Experts/Token** | 8 | 8 | 8 |
| **SWA Window** | 128 | 128 | 128 |
| **Max Context** | 1M | 1M | 256K |
| **MTP Layers** | 3 | 3 | 3 |
| **Hybrid Ratio** | 7:1 | 5:1 | 5:1 |

### Vision Encoder (MiMo-V2.5 only)
| Config | Value |
|---|---|
| Total Layers | 28 |
| SWA Layers | 24 |
| Full Attention | 4 |
| Attention Heads (Q/KV) | 32 / 8 |
| Head Dim (QK/V) | 64 / 64 |
| Window Size | 64/64 |
| Total Params | 729M |

### Audio Encoder (MiMo-V2.5 only)
| Config | Value |
|---|---|
| Total Layers | 24 |
| SWA Layers | 12 |
| Full Attention | 12 |
| Window Size | 128 |
| Attention Heads | 16 / 16 |
| Head Dim | 64 / 64 |
| Total Params | 261M |
| Initialized from | MiMo-Audio-Tokenizer |

---

## Key Innovations

### 1. Hybrid Sliding Window Attention
- Interleaves **Sliding Window Attention (SWA)** and **Global Attention (GA)**
- SWA uses 128-token window → **~6x KV cache reduction**
- Learnable **attention sink bias** maintains long-context performance

### 2. Multi-Token Prediction (MTP)
- 3 lightweight MTP modules (329M params)
- Uses dense FFNs (not MoE) + SWA for efficiency
- **Triples generation speed** via self-speculative decoding
- Also accelerates RL training rollouts

### 3. Multi-Teacher On-Policy Distillation (MOPD)
- Domain-specific expert models provide **token-level supervision**
- Student learns from **own generated responses** (eliminates exposure bias)
- Rewards from distribution divergence → **inherently reward-hack resistant**

### 4. Massive Agentic RL
- **100,000+ verifiable tasks** from real GitHub issues
- 10,000+ concurrent Kubernetes pods for environment setup
- Vision-based verifier for web dev tasks
- Cross-domain generalization (code → math → general agent)

---

## Training Process (MiMo-V2.5)
Total: **~48T tokens**

1. **Text Pre-training** — LLM backbone
2. **Projector Warmup** — Audio/visual MLP projectors
3. **Multimodal Pre-training** — Large-scale multimodal data
4. **SFT & Agentic Post Training** — Progressive context extension (32K → 256K → 1M)
5. **RL & MOPD Training** — Perception, reasoning, agentic capabilities

---

## Benchmarks

### MiMo-V2.5 Multimodal Results
- VideoMME: **87.7** (competitive with Gemini 3 Pro)
- CharXiv RQ: **81.0**
- Strong performance across image, video, and audio understanding

### MiMo-V2.5-Pro Agent Results
| Benchmark | Score | Rank |
|---|---|---|
| PinchBench | 81.0 | #3 globally |
| ClawEval | 61.5 | Approaching Opus 4.6 |
| SWE-Bench Verified | ~73 | Top tier |

### MiMo-V2-Flash Reasoning
| Benchmark | Score |
|---|---|
| MMLU-Pro | 84.9 |
| GPQA-Diamond | 83.7 |
| AIME 2025 | 94.1 |
| LiveCodeBench-v6 | 80.6 |
| SWE-Bench Verified | 73.4 |

---

## Deployment (SGLang)

```bash
# MiMo-V2.5 with SGLang (8x GPU recommended)
python3 -m sglang.launch_server \
    --model-path XiaomiMiMo/MiMo-V2.5 \
    --served-model-name mimo-v2.5 \
    --pp-size 1 --dp-size 2 --tp-size 8 \
    --enable-dp-attention \
    --moe-a2a-backend deepep \
    --page-size 1 \
    --trust-remote-code \
    --context-length 262144 \
    --quantization fp8 \
    --enable-mtp \
    --host 0.0.0.0 --port 9001
```

---

## Model Downloads

| Model | HuggingFace |
|---|---|
| MiMo-V2.5-Pro | `XiaomiMiMo/MiMo-V2.5-Pro` |
| MiMo-V2.5 | `XiaomiMiMo/MiMo-V2.5` |
| MiMo-V2-Flash | `XiaomiMiMo/MiMo-V2-Flash` |
| MiMo-V2-Flash-Base | `XiaomiMiMo/MiMo-V2-Flash-Base` |
| Collection | `https://huggingface.co/collections/XiaomiMiMo/mimo-v25` |

All under **MIT License** — free commercial use, no additional authorization needed.
