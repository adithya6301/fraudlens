"""RAG Precedent Knowledge Base & Semantic Search Engine
Indexes historical fraud precedents, typologies, and institutional protocols.
"""

from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

HISTORICAL_CASES = [
    {
        "case_id": "CASE-HIST-089",
        "title": "Account Takeover & Sudden Crypto Off-Ramp Drain",
        "category": "ACCOUNT_TAKEOVER",
        "indicators": "off-hours midnight crypto emulator foreign proxy sudden drain",
        "summary": "Attacker leveraged leaked credentials and SIM swap to compromise account, executing maximum wire transfer to offshore crypto exchange at 3:15 AM from an African proxy IP.",
        "outcome": "Confirmed Fraud. $45,000 loss mitigated by automated 15-minute rail freeze.",
        "protocol": "Execute immediate transaction hold. Revoke active auth tokens. Require out-of-band biometric or voice step-up verification."
    },
    {
        "case_id": "CASE-HIST-142",
        "title": "Syndicate Botnet Mule Ring with Shared Hardware ID",
        "category": "MULE_NETWORK",
        "indicators": "shared emulator hardware Nox Bluestacks p2p wire mule vault concurrent proxy",
        "summary": "Criminal syndicate operated dummy accounts using an Android emulator farm in Eastern Europe, funneling compromised funds into a central cashout hub.",
        "outcome": "Multi-jurisdictional syndicate identified. Graph analysis detected 6 linked accounts, halting $180,000 in transit.",
        "protocol": "Traverse relationship graph 2-degrees out. Place collective hold on all accounts sharing device and IP fingerprint. Escalate directly to Financial Crimes Unit."
    },
    {
        "case_id": "CASE-HIST-019",
        "title": "Automated Micro-Deposit Card Testing Burst via Tor",
        "category": "CARD_TESTING",
        "indicators": "Tor exit node rapid micro test burst digital goods gift cards velocity spike",
        "summary": "Automated bot performed 3 micro-transactions on compromised card credentials before attempting an $890 digital gaming key purchase through a Tor exit node.",
        "outcome": "Card testing detected at micro-phase. Final large purchase declined automatically.",
        "protocol": "Temporary lock on card. Enforce mandatory 3D-Secure / OTP step-up verification. Flag merchant category for velocity rate-limiting."
    },
    {
        "case_id": "CASE-HIST-055",
        "title": "Legitimate International Traveler Anomaly (False Positive Defense)",
        "category": "LEGITIMATE_TRAVEL",
        "indicators": "travel notice abroad international bakery hotel dining trusted phone chip NFC",
        "summary": "Customer traveled from Dublin to Lisbon. Physical POS transaction at bakery flagged as anomaly purely due to geolocation change. Agent correlated travel advisory and cleared false alert.",
        "outcome": "Legitimate transaction approved without customer friction. Zero false-positive escalation.",
        "protocol": "Verify EMV/NFC cryptogram and registered device token. Cross-reference internal travel notification records. Approve transaction without disruptive hold."
    }
]

class PrecedentRAG:
    def __init__(self):
        self.cases = HISTORICAL_CASES
        self.corpus = [
            f"{c['title']} {c['category']} {c['indicators']} {c['summary']} {c['protocol']}"
            for c in self.cases
        ]
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.matrix = self.vectorizer.fit_transform(self.corpus)

    def search(self, query: str, top_k: int = 1) -> List[Dict[str, Any]]:
        query_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(query_vec, self.matrix).flatten()
        ranked = sims.argsort()[::-1][:top_k]

        results = []
        for idx in ranked:
            c = self.cases[idx]
            results.append({
                "case_id": c["case_id"],
                "title": c["title"],
                "category": c["category"],
                "similarity_score": round(float(sims[idx]) * 100, 1),
                "summary": c["summary"],
                "outcome": c["outcome"],
                "protocol": c["protocol"]
            })
        return results

rag_engine = PrecedentRAG()

def retrieve_precedent(query: str) -> Dict[str, Any]:
    res = rag_engine.search(query, top_k=1)
    return res[0] if res else None
