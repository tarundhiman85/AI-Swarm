# 🤖 Local AI Swarm & Self-Healing Patcher (`AI-Swarm`)

An autonomous, fully offline multi-agent software engineering framework powered by local LLMs via **Ollama**. This project orchestrates collaborative agents (Coder and Test Engineer) within an iterative self-healing loop to generate, validate, and repair Python modules and test suites without relying on paid cloud APIs.

---

## 🏗️ Architecture & Workflow

The swarm operates in a closed-loop development cycle:
1. **Agent 1 (Coder - `qwen2.5-coder:7b`):** Generates robust, thread-safe Python implementations based on natural language task descriptions.
2. **Agent 2 (Test Engineer - `llama3.1:8b`):** Scaffolds comprehensive `pytest` unit test suites targeting the generated module.
3. **Validator (`subprocess` + `sys.executable`):** Executes the local test suite programmatically in a secure virtual environment.
4. **Self-Healing Loop (`swarm_healer.py`):** If tests fail, exact error tracebacks and code context are fed back to the Coder agent for automatic debugging and iteration until all tests pass successfully.

---

## 🛠️ Tech Stack & Prerequisites

* **Runtime:** Python 3.10+ (tested on Python 3.14)
* **Local LLM Engine:** [Ollama](https://ollama.com/) running local models:
  * `qwen2.5-coder:7b` (Code generation & bug repair)
  * `llama3.1:8b` (Test engineering & validation)
* **Testing Framework:** `pytest`
* **Concurrency:** Python `threading.RLock` for thread-safe data structures.

---

## 🚀 Getting Started

### 1. Clone & Set Up Virtual Environment
```bash
git clone [https://github.com/your-username/AI-Swarm.git](https://github.com/your-username/AI-Swarm.git)
cd AI-Swarm
python -m venv venv
