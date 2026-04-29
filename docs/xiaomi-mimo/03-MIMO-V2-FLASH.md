# MiMo-V2-Flash — Efficient Reasoning Model

> Source: https://github.com/xiaomimimo/MiMo-V2-Flash

## Overview
309B total / 15B active params MoE model. Hybrid attention + MTP for efficient reasoning and agentic workloads.

## Architecture
- **Hybrid Attention**: 5:1 SWA:GA ratio, 128-token window → ~6x KV cache reduction
- **MTP**: Dense FFN modules (0.33B params/block) → triples output speed
- **Training**: 27T tokens, FP8 mixed precision, native 32K → 256K context
- **Post-training**: MOPD + large-scale agentic RL

## Benchmarks (Post-Training)

| Benchmark | MiMo-V2-Flash | Kimi-K2 Think | DeepSeek-V3.2 Think | Gemini-3 Pro |
|---|---|---|---|---|
| MMLU-Pro | 84.9 | 84.6 | 85.0 | 90.1 |
| GPQA-Diamond | 83.7 | 84.5 | 82.4 | 91.9 |
| AIME 2025 | 94.1 | 94.5 | 93.1 | 95.0 |
| LiveCodeBench-v6 | 80.6 | 83.1 | 83.3 | 90.7 |
| SWE-Bench Verified | 73.4 | 71.3 | 73.1 | 76.2 |
| BrowseComp | 45.4 | - | 51.4 | - |
| τ²-Bench | 80.3 | 74.3 | 80.3 | 85.4 |
| LongBench V2 | 60.6 | 45.1 | 58.4 | 65.6 |

## Deployment (SGLang)
```bash
SGLANG_ENABLE_SPEC_V2=1 python3 -m sglang.launch_server \
    --model-path XiaomiMiMo/MiMo-V2-Flash \
    --served-model-name mimo-v2-flash \
    --tp-size 8 --dp-size 2 \
    --enable-dp-attention \
    --moe-a2a-backend deepep \
    --context-length 262144 \
    --quantization fp8 \
    --enable-mtp \
    --reasoning-parser qwen3 \
    --tool-call-parser mimo
```

## Recommended Parameters
- **temperature**: 0.8 (math/writing/web-dev), 0.3 (agentic/coding/tool-use)
- **top_p**: 0.95
- **System prompt**: Required (see API reference)

## Important Notes
- In thinking mode with multi-turn tool calls, **persist all reasoning_content** in messages
- MTP weights (3 layers) also open-sourced for community research
- License: **MIT**
