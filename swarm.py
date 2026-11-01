import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def ask_agent(model_name, prompt):
  payload = {"model": model_name, "prompt": prompt, "stream": False}
  response = requests.post(OLLAMA_URL, json=payload)
  if response.status_code == 200:
    return response.json().get("response", "")
  else:
    raise Exception(f"Ollama error: {response.text}")


def run_local_swarm(feature_request):
  print(f"\n[Orchestrator] Starting swarm for task: {feature_request}\n")

  # Step 1: Developer Agent writes the code
  dev_prompt = (
      f"You are an expert software engineer. Write clean, production-ready"
      f" Python code for the following requirement: {feature_request}. Return"
      " only the code block."
  )
  print("[Agent 1: Coder] Writing code using qwen2.5-coder:7b...")
  code_output = ask_agent("qwen2.5-coder:7b", dev_prompt)
  print(f"\n--- Generated Code ---\n{code_output}\n----------------------\n")

  # Step 2: Reviewer Agent critiques the code
  reviewer_prompt = (
      "You are a strict security and architecture reviewer. Analyze the"
      f" following code for bugs, missing edge cases, or security risks, and"
      f" suggest improvements:\n\n{code_output}"
  )
  print("[Agent 2: Reviewer] Analyzing code using llama3.1:8b...")
  review_output = ask_agent("llama3.1:8b", reviewer_prompt)
  print(f"\n--- Code Review ---\n{review_output}\n-------------------\n")

  # Step 3: Save results locally
  with open("swarm_output.md", "w") as f:
    f.write(f"# Task: {feature_request}\n\n## Code\n{code_output}\n\n## Review\n{review_output}")
  print("[Orchestrator] Swarm execution complete. Results saved to swarm_output.md")


if __name__ == "__main__":
  task = "Write a robust Python script to asynchronously read logs and parse error metrics."
  run_local_swarm(task)