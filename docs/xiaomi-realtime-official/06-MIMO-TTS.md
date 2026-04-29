# MiMo TTS — Voice Synthesis Models

> Source: Xiaomi MiMo Platform, mimo.mi.com

## Overview
The MiMo-V2.5-TTS series provides voice synthesis capabilities built for the Agent era.

---

## Capabilities

### 1. Premium TTS Voices
- Built-in high-quality voices
- Strong style-instruction following
- Fine-grained control over **speed**, **emotion**, **tone**
- Suitable for any scenario

### 2. Voice Design
- Define and generate **entirely new voices** from a single text prompt
- Fast, intuitive, and creative
- No need for existing voice samples

### 3. Voice Cloning
- **High-fidelity** voice replication from minimal audio samples
- Consistent timbre
- Strong generalization
- Robust stability

---

## Access via API

TTS is accessible through the MiMo API platform. Token Plan users get **free TTS access** for a limited time.

```python
from openai import OpenAI

client = OpenAI(
    api_key="tp-YOUR_TOKEN_PLAN_KEY",
    base_url="https://token-plan-ams.xiaomimimo.com/v1"
)

# Text-to-speech (check platform for exact TTS endpoint/model names)
# The platform supports TTS through dedicated endpoints
```

---

## Token Plan Coverage
- TTS models are **free across all Token Plan tiers** for a limited time
- Covers all TTS model variants
- Available through Token Plan endpoints (`token-plan-ams.xiaomimimo.com/v1`)

---

## MiMo V2.5 Omni-Modal Integration

Since MiMo-V2.5 natively supports **audio understanding** (via its 261M-param audio encoder), the TTS system can work alongside the main model for:
- Audio analysis → TTS response
- Voice-based agent interactions
- Multi-modal conversations with voice output

---

## Note
For detailed TTS API parameters and voice lists, check the Xiaomi MiMo Platform documentation at [platform.xiaomimimo.com](https://platform.xiaomimimo.com) as these endpoints are being actively updated alongside the V2.5 release.
