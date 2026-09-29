# 🦜🕸️ LangGraph — Hands-On Learning Journey

A day-by-day practice repository for learning **LangGraph**: from basic state graphs to parallel, conditional, and iterative workflows, and finally to persistent, streaming chatbots with a Streamlit UI and SQLite-backed memory.

Each `DayN` folder builds on the previous one, so the repo reads as a progressive tutorial.

---

## 📚 Roadmap

| Day | Topic | File | What it covers |
|-----|-------|------|----------------|
| 1 | Sequential workflows | `Day1/bmi_workflow.ipynb` | `StateGraph`, `TypedDict` state, nodes, edges, `START`/`END`, graph visualization |
| 1 | First LLM workflow | `Day1/simple_llm_workflow.ipynb` | Question → LLM (Gemini) → answer |
| 2 | Parallel workflows | `Day2/batsman_workflow.ipynb` | Fan-out / fan-in: strike rate, balls-per-boundary, boundary % computed in parallel |
| 2 | Parallel LLM workflow | `Day2/PPSC_essay_workflow.ipynb` | Essay evaluation (language, analysis, clarity) in parallel, structured output, `operator.add` reducer, averaged score |
| 3 | Conditional workflows | `Day3/conditional_workflow.ipynb` | Sentiment classification → conditional edges → positive reply or diagnosis + empathetic reply |
| 4 | Iterative workflows | `Day4/X_post_generator.ipynb` | Generate → evaluate → optimize loop with an iteration cap (tweet generator) |
| 5 | Chatbot + memory | `Day5/simple_chatbot.ipynb` | `add_messages`, `InMemorySaver`, `thread_id`, streaming responses |
| 6 | Persistence | `Day6/persistence.ipynb` | *(placeholder — work in progress)* |
| 7 | Streamlit chatbot | `Day7/` | Backend graph + Streamlit chat UI with history restored via `get_state` |
| 8 | SQLite persistence | `Day8/sqlite_chatbot.py` | `SqliteSaver` so conversations survive restarts, stored in `chatbot.db` |

---

## 🧠 Key Concepts Practiced

- **State management** with `TypedDict` and `Annotated` reducers (`operator.add`, `add_messages`)
- **Workflow patterns:** sequential, parallel, conditional routing, and iterative loops
- **Structured output** with Pydantic schemas (`with_structured_output`)
- **Memory & checkpointing** with `InMemorySaver` and `SqliteSaver`
- **Threads** — the same `thread_id` continues the same conversation
- **Token streaming** with `stream_mode="messages"`
- **Frontend integration** using Streamlit's chat components

---

## 🗂️ Project Structure

```
LangGraph/
├── Day1/   bmi_workflow.ipynb, simple_llm_workflow.ipynb
├── Day2/   batsman_workflow.ipynb, PPSC_essay_workflow.ipynb
├── Day3/   conditional_workflow.ipynb
├── Day4/   X_post_generator.ipynb
├── Day5/   simple_chatbot.ipynb
├── Day6/   persistence.ipynb
├── Day7/   langgraph_backend.py, streamlit_frontend.py
├── Day8/   sqlite_chatbot.py
├── .gitignore
└── README.md
```

---

## 🛠️ Tech Stack

- **Python 3.13**
- **LangGraph** / **LangChain**
- **LLM providers:** OpenRouter (via `langchain-openai`), Google Gemini, Groq
- **Streamlit** — chat UI
- **SQLite** — conversation persistence
- **Jupyter** — interactive experiments

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd LangGraph
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install langgraph langchain langchain-core langchain-openai \
            langchain-google-genai langchain-groq langchain-huggingface \
            langgraph-checkpoint-sqlite streamlit python-dotenv pydantic \
            jupyter ipykernel
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
# Used with OpenRouter (base URL is set to https://openrouter.ai/api/v1 in the code)
OPENAI_API_KEY=your_openrouter_api_key

# Only needed for Day 1–2 notebooks
GOOGLE_API_KEY=your_google_api_key
GROQ_API_KEY=your_groq_api_key
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token
```

> ⚠️ Never commit your `.env` file. It's already listed in `.gitignore`.

---

## ▶️ Running the Examples

**Notebooks (Day 1–5):**

```bash
jupyter notebook
```

**Streamlit chatbot (Day 7):**

```bash
cd Day7
streamlit run streamlit_frontend.py
```

**SQLite persistent chatbot (Day 8):**

```bash
python Day8/sqlite_chatbot.py
```

Type `exit`, `quit`, or `bye` to end the session. Run it again with the same `thread_id` and the previous conversation is restored from `chatbot.db`.

---

## 🔍 Workflow Patterns at a Glance

```
Sequential   START → A → B → END

Parallel     START → A ─┐
             START → B ─┼→ Summary → END
             START → C ─┘

Conditional  START → Classify ─┬─(positive)→ Thank-you → END
                               └─(negative)→ Diagnose → Reply → END

Iterative    START → Generate → Evaluate ─┬─(approved)→ END
                                          └─(needs work)→ Optimize ─┐
                                                 ▲──────────────────┘
```

---

## 📝 Notes

- Day 7 uses `InMemorySaver`, so chat history resets when the app restarts. Day 8 fixes this with `SqliteSaver`.
- Model names in the notebooks (e.g. `openrouter/free`) can be swapped for any OpenRouter-compatible model.
- `Day6/persistence.ipynb` is currently empty.

---

## 🎯 Next Steps

- [ ] Tool calling & ReAct agents
- [ ] Human-in-the-loop with interrupts
- [ ] Multi-thread chat sidebar in Streamlit backed by SQLite
- [ ] Retrieval (RAG) integrated into a LangGraph workflow
- [ ] Multi-agent systems