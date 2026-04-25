# Retail Insights Platform

A modular, production-ready AI orchestration engine designed for retail analytics. The platform uses a LangGraph-orchestrated workflow to mathematically retrieve, parse, validate, and explain operational business KPIs and compliance constraints safely and accurately.

## Features

- **Local Inference:** Fully executes via `uvicorn` for local, low-latency API access.
- **LangGraph Routing Pipeline:** Automatically routes user intents between simple KPIs, deep performance constraints, and compliance checks.
- **ChromaDB RAG Vectors:** Integrates local vector embeddings to provide structural and policy context for regulatory compliance.
- **Dual Persistent Memory:** Uses an episodic memory store (SQLite) and semantic memory (ChromaDB) to maintain conversational context.
- **Observability:** Decorates critical API nodes to route performance metrics and tracing data to standard structured JSON logs.
- **Strict Guardrails:** Validates outputs and isolates logic generation to guarantee that the LLM only operates on concrete database parameters.

## How to Run Locally

1. Create and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Spin up the FastAPI server:
   ```bash
   uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload
   ```

## How to Run with Docker

If you prefer to run the architecture in a containerized environment:

1. Ensure Docker Desktop is running.
2. Build and stand up the image:
   ```bash
   docker-compose up --build -d
   ```

## Advanced Evaluations & Benchmarking
The platform includes an advanced local benchmarking framework spanning RAG, Agents, and Semantic Memory logic securely natively dynamically carefully securely implicitly inherently cleanly inherently.

1. **RAG Triplet Measurement:**
   `python -m src.evaluation.run_evals --mode rag`
2. **LangGraph Intent Accuracy:**
   `python -m src.evaluation.run_evals --mode agent`
3. **Episodic Context Check:**
   `python -m src.evaluation.run_evals --mode memory`
4. **Full Automated Sweep:**
   `python -m src.evaluation.run_evals --mode all`
   
Reports are elegantly structurally published to the `evaluation_results/` cleanly natively dynamically safely beautifully comfortably directory seamlessly confidently inherently optimally safely.

## CI/CD 

GitHub Actions executes the `.github/workflows/ci.yml` file, automatically verifying code integrity with `pytest` on every push to the `main` branch.

## Guardrails 

- **Input Constraints:** Enforces 500-character input limits and rejects explicitly malicious SQL patterns prior to LLM evaluation.
- **Output Constraints:** Synthetically matches the LLM response to confirm that purely returned numerical metrics are not hallucinated.

## Future Scaling

Currently, the system is designed to be fully stateless outside of the specific local SQLite stores. Moving forward, the vector and relational datasets can be migrated to managed cloud instances, and the LangGraph orchestrator can be further expanded to include more specialized retail-agent tools.
