"""FraudLens FastAPI Backend Application
Serves REST API and static frontend assets.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
import copy

from .config import APP_NAME, APP_SUBTITLE, APP_VERSION, STATIC_DIR, RISK_THRESHOLDS, ACTIONS
from .data import SEED_TRANSACTIONS, SEED_USERS
from .ml import EVALUATION_METRICS
from .graph import get_serialized_graph
from .agent import run_investigation

app = FastAPI(title=APP_NAME, description=APP_SUBTITLE, version=APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Database Repository
class TransactionStore:
    def __init__(self):
        self.transactions: Dict[str, Dict[str, Any]] = {
            t["id"]: copy.deepcopy(t) for t in SEED_TRANSACTIONS
        }
        self.cases: Dict[str, Dict[str, Any]] = {}
        self._init_cases()

    def _init_cases(self):
        for tid, t in self.transactions.items():
            case = run_investigation(t)
            self.cases[tid] = case
            self.transactions[tid]["risk_score"] = case["composite_risk_score"]
            self.transactions[tid]["severity"] = case["severity_band"]
            self.transactions[tid]["status"] = case["recommended_action_key"]

    def get_all(self) -> List[Dict[str, Any]]:
        return sorted(list(self.transactions.values()), key=lambda x: x.get("risk_score", 0), reverse=True)

    def get_case(self, tid: str) -> Optional[Dict[str, Any]]:
        if tid in self.cases:
            return self.cases[tid]
        if tid in self.transactions:
            case = run_investigation(self.transactions[tid])
            self.cases[tid] = case
            return case
        return None

    def add_transaction(self, t: Dict[str, Any]) -> Dict[str, Any]:
        tid = t.get("id") or f"TXN_{len(self.transactions) + 101}"
        t["id"] = tid
        self.transactions[tid] = t
        case = run_investigation(t)
        self.cases[tid] = case
        self.transactions[tid]["risk_score"] = case["composite_risk_score"]
        self.transactions[tid]["severity"] = case["severity_band"]
        self.transactions[tid]["status"] = case["recommended_action_key"]
        return {"transaction": self.transactions[tid], "case": case}

store = TransactionStore()

class SimulatePayload(BaseModel):
    user_id: str = "USR_101"
    amount: float = 250.0
    merchant: str = "Online Retail Store"
    merchant_category: str = "digital_goods"
    merchant_risk_score: float = 0.5
    device_id: str = "DEV_CUSTOM_DEVICE"
    device_trust_score: float = 0.6
    ip_address: str = "192.168.1.50"
    location_city: str = "Seattle, WA, USA"
    description: Optional[str] = "Simulated transaction"

@app.get("/", response_class=FileResponse)
async def serve_home():
    index_path = STATIC_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="index.html not found")
    return FileResponse(str(index_path))

@app.get("/api/transactions")
async def list_transactions():
    return store.get_all()

@app.get("/api/investigate/{txn_id}")
async def get_investigation(txn_id: str):
    case = store.get_case(txn_id)
    if not case:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return case

@app.post("/api/simulate")
async def simulate_transaction(payload: SimulatePayload):
    user = SEED_USERS.get(payload.user_id, {})
    new_txn = {
        "id": f"TXN_{len(store.transactions) + 101}",
        "user_id": payload.user_id,
        "user_name": user.get("name", "Custom Customer"),
        "account_id": user.get("account_id", f"ACC_{payload.user_id}"),
        "amount": payload.amount,
        "currency": "USD",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "merchant": payload.merchant,
        "merchant_category": payload.merchant_category,
        "merchant_risk_score": payload.merchant_risk_score,
        "device_id": payload.device_id,
        "device_trust_score": payload.device_trust_score,
        "ip_address": payload.ip_address,
        "location_city": payload.location_city,
        "scenario_type": "CUSTOM_SIMULATION",
        "scenario_title": f"Custom Simulation: {payload.merchant}",
        "description": payload.description
    }
    return store.add_transaction(new_txn)

@app.get("/api/graph")
async def get_graph():
    return get_serialized_graph()

@app.get("/api/metrics")
async def get_metrics():
    return EVALUATION_METRICS

@app.get("/api/report/{txn_id}/markdown", response_class=PlainTextResponse)
async def get_markdown_report(txn_id: str):
    case = store.get_case(txn_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    t = case["transaction"]
    md = f"""# FRAUDLENS CASE INVESTIGATION FILE
**Case ID:** {case['case_id']}
**Transaction ID:** {t['id']}
**Customer:** {t['user_name']} ({t['user_id']})
**Amount:** ${t['amount']:,.2f} {t['currency']}
**Merchant:** {t['merchant']} ({t['merchant_category']})
**Location:** {t['location_city']} | **IP:** {t['ip_address']}
**Device:** {t['device_id']}

---
## Executive Summary
{case['executive_summary']}

---
## Risk Assessment
- **Composite Score:** {case['composite_risk_score']}/100
- **Severity Band:** {case['severity_band']}
- **Mandated Action:** {case['action_detail']}

---
## Multi-Step Agent Reasoning Trace
"""
    for s in case["steps_trace"]:
        md += f"\n### Step {s['step_number']}: {s['node_name']}\n"
        md += f"- **Tool:** {s['tool_name']}\n"
        md += f"- **Thought:** {s['thought']}\n"
        md += "- **Findings:**\n"
        for f in s['findings']:
            md += f"  * {f}\n"

    md += "\n---\n*FraudLens: An Agentic AI System for Intelligent Fraud Investigation*\n"
    return md
