# Retail Insights Architecture

## Current State (Part 1)
- **API Engine**: FastAPI (`src/api/routes.py`) dynamically parsing JSON configurations matching structured or raw queries.
- **Orchestration**: Static, deterministic routing isolated entirely within `src/services/analyzer_service.py`.
- **Query Resolution**: Rules engine mappings executing strictly verified parameterized local SQLite extractions (`src/data/db.py`, `src/data/query_runner.py`).
- **Intelligence**: Gemini GenAI (`src/agents/llm_analyzer.py`) safely walled utilizing local rules engine boundaries, with explicit safety wrappers natively falling backward onto hardcoded Python metric analysis if the `.env` fails or the API hallucinates keys.

## Future Architecture Roadmap (Part 2)

We have stubbed exact file module directories representing scalable bounds:

### 1. LangGraph Orchestration (`src/graph/`)
- Will organically replace the linear logic bounds found heavily within `analyzer_service.py`.
- Dynamic nodes (`nodes.py`), state objects (`state.py`), and conditional routing (`router.py`) will allow complex cyclical backtracking if SQL parameters mismatch natively.

### 2. RAG Pipelines (`src/rag/`)
- Embeddings (`indexer.py`) and knowledge base matching (`retriever.py`) will retrieve brand definitions, marketing constraints, and strict compliance limitations explicitly before feeding GenAI.

### 3. Deep Memory Integration (`src/memory/`)
- Separated explicitly between semantic profiling (`semantic.py` to identify behavioral patterns) and episodic chat queues (`episodic.py` enabling short term continuity bridging missing conversational parameters).

### 4. Safety & Observability Defaults
- `src/guardrails/hooks.py`: Validating API input structures explicitly verifying injection mitigation algorithms natively natively restricting SQL mappings securely.
- `src/observability/tracer.py`: Recording and tracking dynamic execution traces effectively generating profound audit trails.

## Future Part 3 Extensions (DevOps & Guardrails)
- **Dockerization**: We will bundle the API, ChromaDB local vectors, and SQLite matrices into unified `docker-compose.yml` images targeting immutable builds natively.
- **CI/CD Triggers**: GitHub Actions will automatically hook `pytest` running boundary evaluations against `src/graph` natively validating State objects locally.
- **Active Guardrails**: The `hooks.py` modules will be attached directly to LangGraph as pre-evaluation Nodes catching explicit SQL hallucination variables natively cleanly reliably accurately optimally securely.
