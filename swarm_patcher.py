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


def run_patch_agent(task_description):
  print(f"\n[Patch Agent] Starting task: {task_description}\n")

  # 1. Generate implementation code
  print("[Agent 1: Coder] Writing module implementation...")
  code_prompt = (
      "You are an elite backend engineer. Write a robust, production-ready"
      f" Python module for this requirement: {task_description}. Return ONLY"
      " valid Python code inside a markdown code block."
  )
  raw_code = ask_agent("qwen2.5-coder:7b", code_prompt)
  clean_code = extract_code(raw_code)

  module_path = "ttl_cache.py"
  print(f"[File System] Writing code directly to {module_path}...")
  with open(module_path, "w", encoding="utf-8") as f:
    f.write(clean_code)

  # 2. Generate unit tests
  print("[Agent 2: Test Engineer] Writing pytest unit tests...")
  test_prompt = (
      "You are a QA automation engineer. Write a complete pytest test suite for"
      f" the following Python module:\n\n{clean_code}\n\nReturn ONLY valid Python"
      " code inside a markdown code block."
  )
  raw_tests = ask_agent("llama3.1:8b", test_prompt)
  clean_tests = extract_code(raw_tests)

  test_path = "test_ttl_cache.py"
  print(f"[File System] Writing unit tests to {test_path}...")
  with open(test_path, "w", encoding="utf-8") as f:
    f.write(clean_tests)

  # 3. Execute local validation via subprocess
  print("[Validator] Executing local test suite via subprocess...")
  result = subprocess.run(
      [sys.executable, "-m", "pytest", test_path],
      capture_output=True,
      text=True,
  )

  print("\n--- Pytest Execution Output ---")
  print(result.stdout)
  if result.stderr:
    print("Stderr:", result.stderr)
  print("-------------------------------")

  if result.returncode == 0:
    print(
        "[Success] Local swarm successfully generated code and passed all"
        " tests!"
    )
  else:
    print(
        "[Attention] Tests failed. The agent will need an iterative fix loop"
        " (Level 4)."
    )


if __name__ == "__main__":
  run_patch_agent(
      "Implement a thread-safe TTLCache class using threading.Lock with get,"
      " set, and background/lazy eviction of expired keys."
  )