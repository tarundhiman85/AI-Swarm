import os
import subprocess
import sys
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def ask_agent(model_name, prompt):
  payload = {"model": model_name, "prompt": prompt, "stream": False}
  response = requests.post(OLLAMA_URL, json=payload)
  if response.status_code == 200:
    return response.json().get("response", "")
  else:
    raise Exception(f"Ollama error: {response.text}")


def extract_code(raw_output):
  """Extracts clean python code from markdown code blocks."""
  if "```python" in raw_output:
    return raw_output.split("```python")[1].split("```")[0].strip()
  elif "```" in raw_output:
    return raw_output.split("```")[1].split("```")[0].strip()
  return raw_output.strip()


def run_self_healing_swarm(task_description, max_retries=3):
  print(f"\n[Self-Healing Swarm] Starting task: {task_description}\n")

  module_path = "ttl_cache.py"
  test_path = "test_ttl_cache.py"

  # 1. Initial Generation
  print("[Agent 1: Coder] Writing module implementation...")
  code_prompt = (
      "You are an elite backend engineer. Write a robust, production-ready"
      f" Python module for this requirement: {task_description}. CRITICAL:"
      " 1. Do NOT use background threads, loops, or timers.\n 2. Use 'lazy"
      " eviction' (checking expiration timestamps inside methods).\n 3. You"
      " MUST use `threading.RLock()` to prevent deadlocks.\n 4. Return ONLY valid"
      " Python code inside a markdown code block."
  )
  clean_code = extract_code(ask_agent("qwen2.5-coder:7b", code_prompt))
  with open(module_path, "w", encoding="utf-8") as f:
    f.write(clean_code)

  print("[Agent 2: Test Engineer] Writing pytest unit tests...")
  test_prompt = (
      "You are a QA automation engineer. Write a complete pytest test suite for"
      f" the following Python module:\n\n{clean_code}\n\nCRITICAL INSTRUCTION:"
      " 1. Include `import pytest`, `import time`, and `import"
      " threading`.\n 2. Import the cache using `from ttl_cache import"
      " TTLCache`.\n 3. For expiration tests, set a short TTL (e.g. `ttl=1`) and"
      " sleep longer than the TTL (e.g. `time.sleep(1.5)`) before asserting"
      " `None`. Return ONLY valid Python code inside a markdown code block."
  )
  clean_tests = extract_code(ask_agent("llama3.1:8b", test_prompt))
  with open(test_path, "w", encoding="utf-8") as f:
    f.write(clean_tests)

  # 2. Iterative Self-Healing Loop (Fixing the Code, not just the tests)
  for attempt in range(1, max_retries + 1):
    print(
        f"\n[Validator] Running test suite (Attempt {attempt}/{max_retries})..."
    )
    result = subprocess.run(
        [sys.executable, "-m", "pytest", test_path],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
      print("\n--- Pytest Output ---")
      print(result.stdout)
      print("---------------------")
      print(
          f"[Success] All tests passed cleanly on attempt {attempt}! Swarm"
          " mission accomplished."
      )
      return

    print(
        f"\n[Warning] Tests failed on attempt {attempt}. Feeding traceback"
        " back to Coder agent for implementation repairs..."
    )
    error_output = result.stdout + "\n" + result.stderr

    fix_prompt = (
        "You are an elite backend engineer. Your implementation code caused the"
        f" following pytest failure traceback:\n\n{error_output}\n\nHere is your"
        f" current implementation code in ttl_cache.py:\n{clean_code}\n\nFix"
        " the logical bugs, missing methods, or thread lock issues in"
        " `ttl_cache.py` so that all unit tests pass. Return ONLY the corrected"
        " Python module implementation inside a markdown code block."
    )

    clean_code = extract_code(ask_agent("qwen2.5-coder:7b", fix_prompt))
    with open(module_path, "w", encoding="utf-8") as f:
      f.write(clean_code)
    print("[File System] Updated ttl_cache.py with Coder agent bugfix.")

  print(
      f"\n[Failure] Swarm exhausted all {max_retries} retry attempts without"
      " achieving passing tests."
  )


if __name__ == "__main__":
  run_self_healing_swarm(
      "Implement a thread-safe TTLCache class using threading.RLock with get,"
      " set, and lazy eviction of expired keys."
  )