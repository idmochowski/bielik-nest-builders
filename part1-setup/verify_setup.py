"""
Verify that the workshop environment is correctly configured.
Run this after setting up your .env file.
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("VLLM_BASE_URL", "http://localhost:8000/v1")
MODEL_NAME = os.getenv("VLLM_MODEL_NAME", "speakleash/Bielik-Minitron-7B-v3.0-Instruct")
API_KEY = os.getenv("VLLM_API_KEY", "EMPTY")

checks_passed = 0
checks_total = 4


def check(name, passed, detail=""):
    global checks_passed
    status = "PASS" if passed else "FAIL"
    print(f"  [{status}] {name}")
    if detail:
        print(f"         {detail}")
    if passed:
        checks_passed += 1


print("=" * 60)
print("Bielik Nest Builders - Environment Verification")
print("=" * 60)
print(f"\nEndpoint: {BASE_URL}")
print(f"Model:    {MODEL_NAME}\n")

# --- Check 1: OpenAI package ---
try:
    from openai import OpenAI
    check("OpenAI Python package installed", True)
except ImportError:
    check("OpenAI Python package installed", False, "Run: pip install openai")

# --- Check 2: NeMo Agent Toolkit ---
try:
    import nat
    from importlib.metadata import version as pkg_version
    check("NeMo Agent Toolkit installed", True, f"Version: {pkg_version('nvidia-nat')}")
except ImportError:
    check("NeMo Agent Toolkit installed", False, "Run: pip install nvidia-nat")

# --- Check 3: Connect to vLLM ---
try:
    client = OpenAI(base_url=BASE_URL, api_key=API_KEY)
    models = client.models.list()
    model_ids = [m.id for m in models.data]
    check("vLLM endpoint reachable", True, f"Available models: {model_ids}")
except Exception as e:
    check("vLLM endpoint reachable", False, str(e))

# --- Check 4: Chat completion with tool calling ---
try:
    client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

    tools = [{
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Pobierz pogodę dla danego miasta",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "Nazwa miasta"}
                },
                "required": ["city"]
            }
        }
    }]

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "Jesteś pomocnym asystentem. Używaj narzędzi gdy to potrzebne."},
            {"role": "user", "content": "Jaka jest pogoda w Warszawie?"}
        ],
        tools=tools,
        temperature=0.7,
        max_tokens=256,
    )

    msg = response.choices[0].message
    has_tool_call = msg.tool_calls is not None and len(msg.tool_calls) > 0
    has_content = msg.content is not None

    if has_tool_call:
        tc = msg.tool_calls[0]
        check("Tool calling works", True, f"Called: {tc.function.name}({tc.function.arguments})")
    elif has_content:
        check("Tool calling works", False, f"Model responded with text instead of tool call: {msg.content[:100]}")
    else:
        check("Tool calling works", False, "Empty response")

except Exception as e:
    check("Tool calling works", False, str(e))

# --- Summary ---
print(f"\n{'=' * 60}")
print(f"Results: {checks_passed}/{checks_total} checks passed")
if checks_passed == checks_total:
    print("All good! You're ready for the workshop.")
else:
    print("Some checks failed. Ask a workshop assistant for help.")
print("=" * 60)

sys.exit(0 if checks_passed == checks_total else 1)
