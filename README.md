# FraudLens: An Agentic AI System for Intelligent Fraud Investigation

FraudLens is an autonomous, evidence-driven fraud investigation system that transforms financial crime triage from a static, black-box classification task into a transparent, explainable investigation process.

---

## 1. Core Architecture & Workflow

```
[ Financial Transaction Ingestion ]
                 │
                 ▼
     [ Dual ML Detection Layer ]
  ├── Supervised Random Forest Classifier (Known fraud probability)
  └── Unsupervised Isolation Forest (Zero-day outlier scoring)
                 │
                 ▼
 [ Autonomous AI Investigation Agent (LangGraph Stepper) ]
                 │
                 ├── Step 1: Ingest Transaction & Run Dual ML
                 ├── Step 2: Customer Behavioral Baseline Profiling (Z-Score & Travel check)
                 ├── Step 3: Device & Geolocation Telemetry (Hardware & Proxy verification)
                 ├── Step 4: NetworkX Graph Traversal (Shared hardware & Mule ring detection)
                 └── Step 5: RAG Precedent Retrieval (Historical cases & institutional protocols)
                 │
                 ▼
 [ Cross-Source Evidence Correlation & Composite Risk Engine (0 - 100) ]
                 │
                 ▼
   [ Mandated Action Recommendation & Plain-English Rationale ]
 (APPROVE | VERIFY_2FA | HOLD | FLAG_ACCOUNT | ESCALATE_HUMAN)
                 │
                 ▼
     [ Simplified Interactive Web Dashboard ]
```

---

## 2. Key Components

- **Dual ML Detection Layer (`app/ml.py`):** Combines Random Forest classification with Isolation Forest anomaly detection to catch both supervised patterns and novel zero-day attacks.
- **Behavioral Profiler (`app/profiling.py`):** Compares transactions against customer historical baselines ($Z$-score, typical spend, active hours, travel notices) to eliminate false positives for travelers.
- **NetworkX Relationship Graph (`app/graph.py`):** Traverses entities (Users, Accounts, Devices, IPs, Merchants) to uncover multi-account fraud rings sharing emulator hardware (`DEV_BOT_EMU_77`).
- **RAG Precedent Knowledge Base (`app/rag.py`):** Vector TF-IDF and cosine similarity search against historical fraud cases to ground agent decisions in institutional precedents.
- **Autonomous Agent Orchestrator (`app/agent.py`):** Implements stateful multi-step reasoning, dynamic tool calls, and evidence synthesis into a composite 0–100 score.

---

## 3. How to Run

1. Navigate to the project directory:
   ```bash
   cd "C:\Users\Kundan Reddy\.gemini\antigravity\scratch\fraudlens"
   ```
2. Start the application:
   ```bash
   python run.py
   ```
3. Open your browser:
   **`http://127.0.0.1:8000`**

*(Note: `run.py` includes automated port conflict detection. If port 8000 is occupied, it automatically selects an available alternative port).*
