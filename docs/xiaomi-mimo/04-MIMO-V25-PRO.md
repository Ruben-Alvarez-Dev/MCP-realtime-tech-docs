# MiMo-V2.5-Pro — Flagship Agent Model

> Source: https://mimo.xiaomi.com/mimo-v2-pro

## Overview
MiMo-V2.5-Pro is Xiaomi's flagship model built for real-world agentic workloads — coding, tool-use, and multi-step reasoning.

## Key Specs
- **1.02T total / 42B active parameters**
- **1M token context window**
- **Hybrid Attention 7:1** (SWA:GA) — improved from 5:1 in V2-Flash
- **MTP** for fast generation
- **MIT License** — fully open source including Base weights

## Agent Benchmarks

### PinchBench (Agent Benchmark)
| Model | Score |
|---|---|
| Claude Opus 4.6 | 81.5 |
| MiMo-V2-Omni | 81.2 |
| **MiMo-V2.5-Pro** | **81.0** |
| Claude Sonnet 4.6 | 79.2 |
| GPT-5.2 | 77.0 |
| Gemini 3 Pro | 67.7 |

### ClawEval
| Model | Score |
|---|---|
| Claude Opus 4.6 | 66.3 |
| Claude Sonnet 4.6 | 66.3 |
| **MiMo-V2.5-Pro** | **61.5** |
| Gemini 3 Pro | 51.9 |
| GPT-5.2 | 50.0 |
| MiMo-V2-Flash | 48.1 |

## Coding Capabilities
- Coding ability **surpasses Claude 4.6 Sonnet** in internal evaluations
- Approaches **Claude Opus 4.6** experience in deep evaluations
- #1 coding tool usage during "Hunter Alpha" stealth test phase

## Token Efficiency
On Claw-Eval leaderboard, MiMo V2.5 ranks at the **optimal frontier** of task completion rate vs token efficiency.

## Pricing
| Context | Input/1M | Output/1M |
|---|---|---|
| Up to 256K | $1 | $3 |
| 256K-1M | $2 | $6 |

> Cache Write temporarily free. Compare: Claude Sonnet 4.6 = $3/$15, Claude Opus 4.6 = $5/$25.

## Integrations
Official partnerships with: OpenClaw, OpenCode, KiloCode, Blackbox, Cline
