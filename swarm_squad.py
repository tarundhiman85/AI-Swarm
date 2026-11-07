import os
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def ask_agent(model_name, prompt):
  payload = {"model": model_name, "prompt": prompt, "stream": False}
  response = requests.post(OLLAMA_URL, json=payload)
  if response.status_code == 200:
    return response.json().get("response", "")
  else:
    raise Exception(f"Ollama error: {response.text}")


def run_feature_squad(feature_description):
  os.makedirs("output_squad", exist_ok=True)
  print(f"\n[Squad Lead] Initializing 4-Agent Squad for: {feature_description}\n")

  # 1. Architect Agent
  print("[Agent 1: Architect] Designing system blueprint...")
  arch_prompt = (
      "You are a Lead Software Architect. Design a clean component and"
      " file structure blueprint for the following requirement:"
      f" {feature_description}. Provide the architectural plan."
  )
  architecture = ask_agent("qwen2.5-coder:7b", arch_prompt)
  with open("output_squad/architecture.md", "w", encoding="utf-8") as f:
    f.write(architecture)

  # 2. Coder Agent
  print("[Agent 2: Coder] Writing implementation code...")
  coder_prompt = (
      "You are an expert Python developer. Based on this architectural"
      f" blueprint:\n{architecture}\n\nWrite the complete, production-ready"
      " Python code. Return only the code block."
  )
  code = ask_agent("qwen2.5-coder:7b", coder_prompt)
  with open("output_squad/solution.py", "w", encoding="utf-8") as f:
    f.write(code)

  # 3. Test Engineer Agent
  print("[Agent 3: Test Engineer] Writing unit tests...")
  tester_prompt = (
      "You are a QA automation engineer. Write a robust pytest unit test"
      f" suite for the following Python code:\n{code}\nReturn only the test"
      " code block."
  )
  tests = ask_agent("llama3.1:8b", tester_prompt)
  with open("output_squad/test_solution.py", "w", encoding="utf-8") as f:
    f.write(tests)

  # 4. Documenter Agent
  print("[Agent 4: Documenter] Creating documentation...")
  doc_prompt = (
      "You are a technical writer. Write a comprehensive README.md file"
      " explaining how to use and test the implementation based on this"
      f" code:\n{code}"
  )
  readme = ask_agent("llama3.1:8b", doc_prompt)
  with open("output_squad/README.md", "w", encoding="utf-8") as f:
    f.write(readme)

  print(
      "\n[Squad Lead] All squad members completed tasks! Artifacts saved to"
      " 'output_squad/' folder."
  )


if __name__ == "__main__":
  task = (
      "A high-performance thread-safe in-memory cache with TTL (Time To Live)"
      " expiration."
  )
  run_feature_squad(task)