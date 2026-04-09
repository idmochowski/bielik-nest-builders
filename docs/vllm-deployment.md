# vLLM Deployment Guide for Beyond Infrastructure Team

This document describes how to deploy **Bielik-Minitron-7B-v3.0-Instruct** with tool calling support for the workshop.

## Requirements

- GPU: NVIDIA B200 (fractional GPU, 0.5 GPU sufficient for single instance)
- vLLM >= 0.8.x (recommended latest stable)
- Python 3.10+

## Step 1: Install vLLM

```bash
pip install vllm
```

## Step 2: Clone Bielik Tools (required for tool calling)

```bash
git clone https://github.com/speakleash/bielik-tools.git
```

This provides:
- `tools/bielik_advanced_chat_template.jinja` - Extended ChatML template with tool calling support
- `tools/bielik_vllm_tool_parser.py` - Custom tool call parser for vLLM

> **Note:** For vLLM 0.12.0 and earlier, use `bielik_vllm_tool_parser_v0.12.0.py` instead.

## Step 3: Launch vLLM Server

```bash
vllm serve speakleash/Bielik-Minitron-7B-v3.0-Instruct \
    --served-model-name bielik-minitron-7b \
    --enable-auto-tool-choice \
    --tool-parser-plugin ./bielik-tools/tools/bielik_vllm_tool_parser.py \
    --tool-call-parser bielik \
    --chat-template ./bielik-tools/tools/bielik_advanced_chat_template.jinja \
    --dtype bfloat16 \
    --max-model-len 8192 \
    --port 8000 \
    --host 0.0.0.0
```

### Parameter explanation

| Parameter | Value | Reason |
|-----------|-------|--------|
| `--served-model-name` | `bielik-minitron-7b` | Consistent model name for API calls |
| `--enable-auto-tool-choice` | (flag) | Enables function/tool calling |
| `--tool-parser-plugin` | `bielik_vllm_tool_parser.py` | Bielik-specific tool call parsing |
| `--tool-call-parser` | `bielik` | Registers the parser under this name |
| `--chat-template` | `bielik_advanced_chat_template.jinja` | Extended ChatML with tool support |
| `--dtype` | `bfloat16` | Native precision of the model |
| `--max-model-len` | `8192` | Sufficient for workshop tasks; saves VRAM. Can increase to 32768 if needed |
| `--port` | `8000` | OpenAI-compatible API on this port |
| `--host` | `0.0.0.0` | Accessible from Run:ai workspaces |

## Step 4: Verify

```bash
# Health check
curl http://localhost:8000/health

# Model list
curl http://localhost:8000/v1/models

# Test completion
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "bielik-minitron-7b",
    "messages": [{"role": "user", "content": "Cześć! Kim jesteś?"}],
    "temperature": 0.7,
    "max_tokens": 256
  }'

# Test tool calling
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "bielik-minitron-7b",
    "messages": [{"role": "user", "content": "Jaka jest pogoda w Warszawie?"}],
    "tools": [{
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Pobierz aktualną pogodę dla podanego miasta",
        "parameters": {
          "type": "object",
          "properties": {
            "city": {"type": "string", "description": "Nazwa miasta"}
          },
          "required": ["city"]
        }
      }
    }],
    "temperature": 0.7,
    "max_tokens": 256
  }'
```

## Endpoint URL for Participants

The workshop `.env` needs:

```
VLLM_BASE_URL=http://<vllm-service-address>:8000/v1
VLLM_MODEL_NAME=bielik-minitron-7b
```

Participants connect via NeMo Agent Toolkit using the OpenAI-compatible API.

## Capacity Planning: 40 Participants / 4x B200

**Model footprint:** ~15 GB VRAM (7.35B params in BF16)
**B200 capacity:** 192 GB HBM3e per GPU
**Measured throughput:** ~200-230 tokens/sec on 0.5 GPU B200

**Current setup:** Single instance on 0.5 GPU B200 - tested and working.

At ~200 tok/s with typical 500-token workshop outputs (~2.5s per request),
a single instance handles moderate concurrent load via vLLM's continuous batching.
For 40 simultaneous participants, consider 2 instances behind a load balancer
or NAT's built-in multi-endpoint round-robin:

```yaml
llms:
  bielik:
    _type: openai
    base_url:
      - "http://vllm-1:8000/v1"
      - "http://vllm-2:8001/v1"
```
