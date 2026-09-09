from typing import Dict, Any, List


AI_REFERENCE_PDFS: List[Dict[str, str]] = [
    {
        "id": "week1_llm_foundations",
        "week": "Week 1",
        "title": "LLM Foundations Master Guide",
        "filename": "llm-foundations-master-guide.pdf",
        "path": r"C:\Users\supra\Downloads\llm-foundations-master-guide.pdf",
    },
    {
        "id": "week2_prompt_engineering",
        "week": "Week 2",
        "title": "Prompt Engineering & Structured Outputs",
        "filename": "prompt-engineering-structured-outputs.pdf",
        "path": r"C:\Users\supra\Downloads\prompt-engineering-structured-outputs.pdf",
    },
    {
        "id": "week3_rag",
        "week": "Week 3",
        "title": "Embeddings, Vector Databases & RAG",
        "filename": "embeddings-vector-databases-rag.pdf",
        "path": r"C:\Users\supra\Downloads\embeddings-vector-databases-rag.pdf",
    },
    {
        "id": "week4_agents",
        "week": "Week 4",
        "title": "Autonomous Agents & Multi-Agent Architectures",
        "filename": "agent-architectures-master-guide.pdf",
        "path": r"C:\Users\supra\Downloads\agent-architectures-master-guide.pdf",
    },
    {
        "id": "week5_mcp_frameworks",
        "week": "Week 5",
        "title": "MCP & AI Frameworks Master Guide",
        "filename": "mcp-ai-frameworks-master-guide.pdf",
        "path": r"C:\Users\supra\Downloads\mcp-ai-frameworks-master-guide.pdf",
    },
    {
        "id": "week6_inference_serving",
        "week": "Week 6",
        "title": "Inference & Serving Master Guide",
        "filename": "inference-serving-master-guide.pdf",
        "path": r"C:\Users\supra\Downloads\inference-serving-master-guide.pdf",
    },
    {
        "id": "week7_finetuning_quantization",
        "week": "Week 7",
        "title": "Fine-Tuning & Quantization Master Guide",
        "filename": "fine-tuning-quantization-master-guide.pdf",
        "path": r"C:\Users\supra\Downloads\fine-tuning-quantization-master-guide.pdf",
    },
    {
        "id": "week8_distillation_evaluation",
        "week": "Week 8",
        "title": "Distillation & Evaluation Master Guide",
        "filename": "distillation-evaluation-master-guide.pdf",
        "path": r"C:\Users\supra\Downloads\distillation-evaluation-master-guide.pdf",
    },
    {
        "id": "week9_production_backend",
        "week": "Week 9",
        "title": "Production AI Backend",
        "filename": "production-ai-backend.pdf",
        "path": r"C:\Users\supra\Downloads\production-ai-backend.pdf",
    },
    {
        "id": "week10_capstone",
        "week": "Week 10",
        "title": "Capstone Project Blueprints",
        "filename": "capstone-project-blueprints.pdf",
        "path": r"C:\Users\supra\Downloads\capstone-project-blueprints.pdf",
    },
]


AI_CHAPTERS: Dict[str, Any] = {
    "week_01_foundations": {
        "title": "Week 1 - LLM Foundations & Transformer Math",
        "reference_ids": ["week1_llm_foundations"],
        "content": """
### Learning Details
This week covers the fundamentals from the **LLM Foundations Master Guide**:
- Why Transformer architecture replaced RNN/LSTM pipelines.
- Tokenization flow, embedding matrices, positional encoding.
- Scaled dot-product attention mathematics and multi-head attention.
- Decoding strategies: greedy, beam, temperature sampling, top-k/top-p.

Core equation:
$$Attention(Q, K, V)=softmax((QK^T)/sqrt(d_k))V$$

### Week Plan
**Day 1:** RNN bottlenecks and transformer mental model.  
**Day 2:** Tokenization, BPE, and embedding space behavior.  
**Day 3:** Attention math walkthrough with matrix dimensions.  
**Day 4:** Decoding algorithms and hallucination trade-offs.  
**Day 5:** Build a minimal async chat endpoint with streaming.

### Topics Diagram
```text
Input Text
  -> Tokenizer (BPE)
  -> Token IDs
  -> Embedding + Positional Encoding
  -> Transformer Blocks
      |- Multi-Head Attention
      |- Feed Forward
  -> Logits
  -> Decoder (top-k / top-p / temperature)
  -> Final Response
```

### Example
Given prompt: "Explain ACID in 3 bullets", compare outputs with:
- temperature=0.1 (deterministic)
- temperature=0.8 (more creative, less stable)
""",
    },
    "week_02_prompting_structured_outputs": {
        "title": "Week 2 - Prompt Engineering & Structured Outputs",
        "reference_ids": ["week2_prompt_engineering"],
        "content": """
### Learning Details
This week follows **Prompt Engineering & Structured Outputs**:
- Zero-shot vs few-shot prompting under production constraints.
- ReAct (Reason + Act) loop and tool orchestration boundaries.
- JSON Mode vs grammar-constrained structured outputs.
- Guardrails for prompt injection and malformed output containment.

### Week Plan
**Day 1:** Prompt templates and instruction hierarchy.  
**Day 2:** Few-shot retrieval strategy and failure analysis.  
**Day 3:** ReAct traces with tool-call retries and stop conditions.  
**Day 4:** JSON schema constrained decoding and response validation.  
**Day 5:** Build policy guardrails (input + output filters).

### Topics Diagram
```text
User Request
  -> Prompt Builder
      |- System Rules
      |- Few-Shot Context
      |- Tool Contracts
  -> LLM
  -> Structured Output Validator (JSON Schema)
      |- pass -> business logic
      |- fail -> auto-repair / retry
```

### Example
Restaurant assistant output contract:
- fields: intent, dish_name, allergens, confidence
- reject responses that violate schema or contain unknown keys.
""",
    },
    "week_03_embeddings_vector_rag": {
        "title": "Week 3 - Embeddings, Vector Databases & RAG",
        "reference_ids": ["week3_rag"],
        "content": """
### Learning Details
From **Embeddings, Vector Databases & RAG**:
- Similarity metrics: cosine, dot product, euclidean distance.
- Chunking patterns: recursive, semantic, parent-child retrieval.
- Vector stores and indexes: Flat, HNSW, IVFFlat, pgvector.
- Hybrid retrieval: BM25 + dense vectors + rank fusion + reranker.

### Week Plan
**Day 1:** Embedding geometry and distance metrics.  
**Day 2:** Chunking benchmark on same document corpus.  
**Day 3:** Build vector index and compare retrieval latency/recall.  
**Day 4:** Add reranker and context compression pipeline.  
**Day 5:** End-to-end RAG API with citations and eval hooks.

### Topics Diagram
```text
Raw Docs
  -> Chunking Pipeline
      |- Recursive Splitter
      |- Semantic Splitter
  -> Embedding Model
  -> Vector DB (HNSW / IVFFlat / pgvector)
Query
  -> Dense + BM25 Hybrid Retrieval
  -> Reranker
  -> Context Pack
  -> LLM Answer + Citations
```

### Example
Use k=20 retrieval + cross-encoder rerank to top-5 before final generation.
Compare groundedness with and without reranking.
""",
    },
    "week_04_autonomous_agents": {
        "title": "Week 4 - Autonomous Agents & Multi-Agent Systems",
        "reference_ids": ["week4_agents"],
        "content": """
### Learning Details
Aligned to **Autonomous Agents & Multi-Agent Architectures**:
- Chatbot pipeline vs stateful autonomous control loop.
- Memory tiers: short-term, episodic, semantic.
- Planning via DAG decomposition and self-critique cycles.
- Reflexion framework and iterative policy improvement.

### Week Plan
**Day 1:** Agent lifecycle and control-plane primitives.  
**Day 2:** Build memory abstractions with retrieval policies.  
**Day 3:** Planner + executor graph with dependency tracking.  
**Day 4:** Reflexion and failure-recovery loop.  
**Day 5:** Multi-agent collaboration for decomposition + verification.

### Topics Diagram
```text
Goal
  -> Planner (task graph)
  -> Executor (tool calls)
  -> Observer (state updates)
  -> Critic (self-reflection)
  -> Memory Store
      |- Working
      |- Episodic
      |- Semantic
  -> Re-plan / Final Output
```

### Example
Debugging agent:
1. Generate patch
2. Run tests
3. Critique failures
4. Patch again with bounded retry budget.
""",
    },
    "week_05_mcp_frameworks": {
        "title": "Week 5 - MCP Protocol & AI Agent Frameworks",
        "reference_ids": ["week5_mcp_frameworks"],
        "content": """
### Learning Details
From **MCP & AI Frameworks Master Guide**:
- MCP host/server/tool role boundaries and JSON-RPC primitives.
- MCP transports: stdio vs SSE and production trade-offs.
- Framework patterns: LangGraph, PydanticAI, LlamaIndex workflows, Semantic Kernel/Crew-style orchestration.
- Type-safe tool contracts and dependency injection for agent safety.

### Week Plan
**Day 1:** MCP primitives (resources, prompts, tools).  
**Day 2:** Build stdio MCP server and validate protocol frames.  
**Day 3:** Add SSE transport and auth boundaries.  
**Day 4:** Integrate one framework with type-safe tools.  
**Day 5:** Compare orchestration models under retry/failure load.

### Topics Diagram
```text
MCP Host (IDE/App)
  <-> Transport (stdio | SSE)
  <-> MCP Server
      |- Resources
      |- Prompts
      |- Tools
  -> Agent Framework Runtime
      |- Planning Nodes
      |- Tool Executor
      |- State Store
```

### Example
Expose tools: `search_docs`, `create_ticket`, `run_eval`.
Enforce strict JSON schema for arguments and result payloads.
""",
    },
    "week_06_inference_serving": {
        "title": "Week 6 - Inference & Model Serving Architectures",
        "reference_ids": ["week6_inference_serving"],
        "content": """
### Learning Details
Using **Inference & Model Serving Master Guide**:
- Runtime options: vLLM, llama.cpp, Ollama deployment profiles.
- Continuous batching and KV cache optimization.
- Speculative decoding for throughput acceleration.
- VRAM sizing math for weights + KV cache + concurrency planning.

### Week Plan
**Day 1:** Serving runtime selection matrix by workload.  
**Day 2:** Continuous batching and scheduler tuning.  
**Day 3:** KV cache pressure tests under long context windows.  
**Day 4:** Speculative decoding and acceptance-rate telemetry.  
**Day 5:** Capacity model: tokens/sec, p95 latency, memory budget.

### Topics Diagram
```text
API Gateway
  -> Scheduler
      |- Continuous Batch Builder
      |- Priority Queue
  -> Inference Runtime (vLLM / llama.cpp)
  -> KV Cache Manager
  -> Token Stream (SSE/WebSocket)
  -> Metrics (latency, tps, cache hit)
```

### Example
Measure p95 latency at 50/100/200 concurrent sessions with and without speculative decoding.
""",
    },
    "week_07_finetuning_quantization": {
        "title": "Week 7 - Fine-Tuning, PEFT & Quantization",
        "reference_ids": ["week7_finetuning_quantization"],
        "content": """
### Learning Details
From **Fine-Tuning & Quantization Master Guide**:
- Continued pre-training vs supervised fine-tuning (SFT).
- LoRA and QLoRA internals, rank selection, adapter composition.
- Precision ladder: FP16, BF16, INT8, INT4.
- PTQ families: GPTQ, AWQ, GGUF export and serving implications.

### Week Plan
**Day 1:** Data curation and SFT objective setup.  
**Day 2:** LoRA/QLoRA training run with rank and alpha sweeps.  
**Day 3:** Quantization experiments across 16/8/4-bit profiles.  
**Day 4:** Accuracy-cost comparison and failure slices.  
**Day 5:** Deploy adapter + quantized model and evaluate regressions.

### Topics Diagram
```text
Domain Dataset
  -> SFT / PEFT Trainer
      |- LoRA Adapters
      |- QLoRA (4-bit base + LoRA)
  -> Checkpoints
  -> Quantization (GPTQ/AWQ/GGUF)
  -> Serving Runtime
  -> Eval Dashboard (quality vs cost)
```

### Example
Train LoRA rank 8 vs 16, then quantize to INT4.
Compare quality drop and throughput gain on same benchmark set.
""",
    },
    "week_08_distillation_evaluation": {
        "title": "Week 8 - Distillation & Evaluation Pipelines",
        "reference_ids": ["week8_distillation_evaluation"],
        "content": """
### Learning Details
Mapped from **Distillation & Evaluation Master Guide**:
- Teacher-student distillation and softened logits transfer.
- Combined objective: hard target CE + KL divergence distillation term.
- Synthetic data evolution (Evol-Instruct style) for coverage expansion.
- LLM-as-a-judge, G-Eval, groundedness and relevancy checks.

### Week Plan
**Day 1:** Distillation math and temperature tuning.  
**Day 2:** Build synthetic dataset mutation loop.  
**Day 3:** Train compact student model on mixed objective.  
**Day 4:** Build evaluation harness with judge rubric traces.  
**Day 5:** Reliability report: hallucination, groundedness, factuality.

### Topics Diagram
```text
Teacher Model
  -> Logits + Rationales
  -> Synthetic Data Generator
      -> Student Training Set
Student Model
  -> Distillation Training
  -> Eval Harness
      |- LLM Judge (G-Eval)
      |- Groundedness
      |- Relevancy
      |- Safety
```

### Example
Use alpha blend for loss:
`loss = alpha * CE(student, labels) + (1-alpha) * KL(student_T, teacher_T)`.
Tune alpha for best quality-latency balance.
""",
    },
    "week_09_production_ai_backend": {
        "title": "Week 9 - Production AI Backend Design",
        "reference_ids": ["week9_production_backend"],
        "content": """
### Learning Details
From **Production AI Backend**:
- Stateless FastAPI core with Redis, PostgreSQL, and async workers.
- Prompt registry/versioning and deployment governance.
- Token-cost optimization: semantic cache + request shaping.
- SSE streaming, backpressure management, and secure secrets lifecycle.

### Week Plan
**Day 1:** Design stateless service boundaries and contracts.  
**Day 2:** Implement Redis cache/rate-limiter middleware.  
**Day 3:** Build prompt registry with version pinning.  
**Day 4:** Add SSE streaming + cancellation + backpressure handling.  
**Day 5:** Security hardening (secret injection, audit logs, key rotation).

### Topics Diagram
```text
Client
  -> API Gateway
  -> FastAPI Service
      |- Auth + Rate Limiter (Redis)
      |- Prompt Registry
      |- Orchestrator
      |- Retrieval Layer
      |- LLM Provider Adapters
  -> PostgreSQL (history/metadata)
  -> Observability Stack
```

### Example
Implement semantic cache key:
`hash(normalized_prompt + model + policy_version + retrieval_signature)`.
""",
    },
    "week_10_capstone_blueprints": {
        "title": "Week 10 - Capstone Project Blueprints",
        "reference_ids": ["week10_capstone"],
        "content": """
### Learning Details
Based on **Capstone Project Blueprints**:
- Option 1: AI SOC analyst pipeline with event ingestion + enrichment.
- Option 2: Enterprise knowledge assistant with production RAG.
- Option 3: Durable coding agent with human-in-the-loop checkpoints.
- Full integration of infra, evaluation, observability, security, and reliability.

### Week Plan
**Day 1:** Choose capstone option and define acceptance criteria.  
**Day 2:** Build architecture skeleton and interface contracts.  
**Day 3:** Implement core async execution paths.  
**Day 4:** Add evaluation + monitoring + chaos tests.  
**Day 5:** Demo review, trade-off report, and production checklist.

### Topics Diagram
```text
Capstone Scope
  -> System Design (HLD)
  -> Module Design (LLD)
  -> Build Phase
      |- APIs
      |- Retrieval/Agents
      |- Data + Queue
  -> Eval + Observability
  -> Security + Reliability
  -> Final Demo + Runbook
```

### Example
For the SOC Analyst project:
Webhook -> Queue -> Enrichment tools -> Policy evaluator -> Alert summarizer -> SIEM write-back.
""",
    },
}


AI_QUIZ: Dict[str, Any] = {
    "title": "AI & Large Language Models Assessment",
    "questions": [
        {
            "id": "ai_q1",
            "question": "What is the most accurate difference between JSON mode and schema-constrained structured outputs?",
            "options": [
                "JSON mode validates field semantics automatically",
                "Structured outputs enforce grammar/schema validity at decoding time",
                "Both are equivalent and only differ in token cost",
                "JSON mode is more strict than grammar decoding"
            ],
            "correct_option": 1,
            "explanation": "JSON mode usually enforces JSON shape, while grammar-constrained decoding enforces the exact allowed token paths for the target schema."
        },
        {
            "id": "ai_q2",
            "question": "Why does parent-child chunk retrieval improve RAG quality for long documents?",
            "options": [
                "It avoids embeddings entirely",
                "It retrieves small precise chunks but expands context from larger parent documents",
                "It only works with BM25, not vectors",
                "It guarantees zero hallucinations without evaluation"
            ],
            "correct_option": 1,
            "explanation": "Child chunks improve retrieval precision; parent expansion gives enough context for synthesis, balancing precision and recall."
        },
        {
            "id": "ai_q3",
            "question": "In knowledge distillation, what is the main role of softened teacher logits?",
            "options": [
                "They hide class relationships to reduce overfitting",
                "They provide richer inter-class similarity signals to the student",
                "They replace all supervised labels permanently",
                "They remove the need for evaluation"
            ],
            "correct_option": 1,
            "explanation": "Soft logits encode relative class probabilities, transferring nuanced similarity knowledge that hard one-hot labels cannot carry."
        }
    ]
}

