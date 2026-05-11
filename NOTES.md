# 📘 LangChain Learning Notes — Phase 1

# 🎯 Goal of Phase 1
Understand:
- What an AI agent is
- How tools work
- How LangChain agents execute internally
- What `agent.invoke()` actually does

---

# 🧠 Core Mental Model

```text
User → LLM (Brain) → decides → Tool OR direct answer → Final response
```

---

# 🔧 What We Built in `main.py`

## LLM Setup
- Used **Groq** as the LLM provider via `langchain_groq.ChatGroq`
- Model: `llama-3.3-70b-versatile`
- API key loaded from `.env` using `python-dotenv` (`GROQ_API_KEY`)

## Defining a Tool
- Tools are defined with the `@tool` decorator from `langchain.tools`
- The docstring is **critical** — the LLM reads it to decide when to call the tool
- Example tool:
  ```python
  @tool
  def multiply(a: int, b: int) -> int:
      """Multiply two numbers."""
      return a * b
  ```

## Creating the Agent
- Used `create_agent(model=llm, tools=[multiply])` from `langchain.agents`
- The agent is given the LLM (brain) and a list of tools it can use

## Running the Agent (REPL Loop)
- A `while True` loop prompts the user for input
- Exit on `"exit"` or `"quit"`
- Agent is invoked with:
  ```python
  agent.invoke({"messages": [{"role": "user", "content": query}]})
  ```
- Response is a dict with a `"messages"` key — a list of message objects
- The final answer is always at `response["messages"][-1].content`

## Key Insight: `response["messages"]`
- The response contains the **full message chain**, not just the final answer
- Each entry is a typed message object (e.g. `HumanMessage`, `AIMessage`, `ToolMessage`)
- Inspecting all messages shows the step-by-step reasoning: LLM thought → tool call → tool result → final answer