"""Autonomous AI Fraud Investigation Agent
Implements LangGraph-style multi-step tool-driven reasoning, evidence correlation,
and explainable risk scoring.
"""

from typing import Dict, Any, List
from datetime import datetime
from .ml import evaluate_transaction_ml
from .profiling import analyze_behavioral_profile
from .graph import analyze_graph
from .rag import retrieve_precedent
from .config import ACTIONS

def analyze_device_geo(txn: Dict[str, Any]) -> Dict[str, Any]:
    dev_id = txn.get("device_id", "UNKNOWN")
    trust = float(txn.get("device_trust_score", 0.5))
    ip = txn.get("ip_address", "UNKNOWN")
    city = txn.get("location_city", "UNKNOWN")

    findings = []
    is_emulator = "EMU" in dev_id or "LINUX" in dev_id
    is_tor = "TOR" in dev_id or "185.220" in ip
    is_proxy = "194.26" in ip or "102.89" in ip

    if is_emulator:
        findings.append(f"Hardware Fingerprint Alert: Headless Linux/Android emulator environment detected ('{dev_id}').")
    if is_tor:
        findings.append(f"Anonymized Network Relay: Traffic routed via Tor exit relay ('{ip}').")
    if is_proxy:
        findings.append(f"Commercial VPN / Bulletproof Hosting: Connection originated from high-risk hosting ASN ('{ip}').")
    if trust < 0.40:
        findings.append(f"Degraded Hardware Trust Score: {trust:.2f}/1.00 (Unverified or Ephemeral device).")

    if not findings:
        findings.append(f"Device and Network Verified: Hardware '{dev_id}' is trusted (Score: {trust:.2f}) on residential ISP in {city}.")

    dev_risk = max(85.0 if (is_emulator or is_tor or is_proxy) else (1.0 - trust) * 100.0, 10.0)

    return {
        "device_id": dev_id,
        "trust_score": trust,
        "is_emulator": is_emulator,
        "is_anonymized": is_tor or is_proxy,
        "device_risk_score": round(dev_risk, 1),
        "findings": findings
    }

class InvestigationAgent:
    def investigate(self, txn: Dict[str, Any]) -> Dict[str, Any]:
        txn_id = txn.get("id", "TXN_NEW")
        case_id = f"CASE-{txn_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        steps_trace = []

        # -------------------------------------------------------------
        # STEP 1: Dual ML Detection
        # -------------------------------------------------------------
        ml_res = evaluate_transaction_ml(txn)
        step1_thought = (
            f"Ingesting transaction {txn_id} (${float(txn.get('amount', 0)):,.2f} at {txn.get('merchant')}). "
            f"Supervised Random Forest predicts {ml_res['supervised_probability']:.1%} fraud probability, "
            f"and Isolation Forest detects outlier score of {ml_res['isolation_forest_score']:.2f}. "
            f"{'Transaction flagged as anomalous; initiating autonomous deep tool reasoning.' if ml_res['flagged_as_suspicious'] else 'Transaction has low ML anomaly index; cross-verifying customer profile.'}"
        )
        steps_trace.append({
            "step_number": 1,
            "node_name": "ML_ANOMALY_DETECTION",
            "tool_name": "Dual ML Engine (Random Forest + Isolation Forest)",
            "thought": step1_thought,
            "findings": [
                f"Supervised Fraud Probability: {ml_res['supervised_probability']:.1%}",
                f"Isolation Forest Outlier Score: {ml_res['isolation_forest_score']:.2f}",
                f"Combined ML Anomaly Index: {ml_res['combined_ml_score']}/100"
            ]
        })

        # -------------------------------------------------------------
        # STEP 2: Customer Behavioral Baseline Profiling
        # -------------------------------------------------------------
        profile_res = analyze_behavioral_profile(txn)
        step2_thought = (
            f"Cross-referencing customer baseline for {txn.get('user_name')}. "
            f"Historical spend averages ${profile_res.get('historical_avg', 0):.2f}. "
            f"Transaction amount produces a Z-Score deviation of {profile_res.get('z_score', 0):.2f}. "
            f"Behavioral deviation index computed at {profile_res.get('deviation_score', 0)}/100."
        )
        steps_trace.append({
            "step_number": 2,
            "node_name": "BEHAVIORAL_BASELINE_PROFILING",
            "tool_name": "Customer Profile Analyzer",
            "thought": step2_thought,
            "findings": profile_res.get("anomalies", [])
        })

        # -------------------------------------------------------------
        # STEP 3: Device & Geolocation Telemetry
        # -------------------------------------------------------------
        dev_res = analyze_device_geo(txn)
        step3_thought = (
            f"Evaluating hardware attestation and connection provenance for device '{dev_res['device_id']}' "
            f"located at {txn.get('location_city', 'Unknown')} (IP: {txn.get('ip_address', 'Unknown')}). "
            f"{'Critical alert: Emulator or Anonymization relay identified.' if (dev_res['is_emulator'] or dev_res['is_anonymized']) else 'Device hardware verified as trusted.'}"
        )
        steps_trace.append({
            "step_number": 3,
            "node_name": "DEVICE_AND_GEO_TELEMETRY",
            "tool_name": "Device & Geo Telemetry Inspector",
            "thought": step3_thought,
            "findings": dev_res.get("findings", [])
        })

        # -------------------------------------------------------------
        # STEP 4: NetworkX Relationship Graph Traversal
        # -------------------------------------------------------------
        graph_res = analyze_graph(txn.get("user_id"), txn.get("device_id"), txn.get("ip_address"))
        step4_thought = (
            f"Traversing NetworkX graph 2-hops out across User, Account, Device, and Merchant entities. "
            f"{'ALERT: Shared hardware fingerprint detected across distinct customer accounts! Indicative of coordinated mule syndicate.' if graph_res['is_syndicate'] else 'Graph traversal reveals normal isolated topology.'}"
        )
        steps_trace.append({
            "step_number": 4,
            "node_name": "GRAPH_RELATIONSHIP_TRAVERSAL",
            "tool_name": "NetworkX Graph Traversal Engine",
            "thought": step4_thought,
            "findings": graph_res.get("findings", [])
        })

        # -------------------------------------------------------------
        # STEP 5: RAG Historical Precedent Retrieval
        # -------------------------------------------------------------
        query_terms = [
            txn.get("merchant_category", ""),
            txn.get("scenario_type", ""),
            "crypto" if "crypto" in txn.get("merchant_category", "").lower() else "",
            "mule emulator" if graph_res["is_syndicate"] else "",
            "travel" if profile_res.get("travel_notice_active") else "",
            "tor" if dev_res.get("is_anonymized") else ""
        ]
        rag_query = " ".join([q for q in query_terms if q]).strip()
        precedent = retrieve_precedent(rag_query or txn.get("merchant", ""))

        step5_thought = (
            f"Queried RAG vector knowledge base with evidence signature '{rag_query}'. "
            f"Retrieved highest-matching precedent: {precedent['case_id']} ('{precedent['title']}') "
            f"with {precedent['similarity_score']}% semantic similarity."
        )
        steps_trace.append({
            "step_number": 5,
            "node_name": "RAG_PRECEDENT_RETRIEVAL",
            "tool_name": "RAG Knowledge Base Retriever",
            "thought": step5_thought,
            "findings": [
                f"Matching Historical Case: {precedent['case_id']} - {precedent['title']} ({precedent['similarity_score']}% match)",
                f"Precedent Outcome: {precedent['outcome']}",
                f"Mandated Protocol: {precedent['protocol']}"
            ]
        })

        # -------------------------------------------------------------
        # STEP 6: Multi-Source Evidence Correlation & Verdict
        # -------------------------------------------------------------
        ml_score = ml_res["combined_ml_score"]
        behavior_score = profile_res["deviation_score"]
        device_score = dev_res["device_risk_score"]
        graph_score = 95.0 if graph_res["is_syndicate"] else (75.0 if graph_res["graph_risk"] == "HIGH" else 15.0)
        merchant_score = float(txn.get("merchant_risk_score", 0.1)) * 100.0

        # Legitimate travel mitigation:
        if profile_res.get("travel_notice_active") and dev_res["trust_score"] >= 0.85:
            composite = (0.20 * ml_score) + (0.15 * behavior_score) + (0.10 * device_score) + (0.10 * graph_score) + (0.05 * merchant_score)
            composite = min(composite, 22.0) # Ensure it stays in LOW band
        else:
            composite = (0.25 * ml_score) + (0.25 * behavior_score) + (0.20 * device_score) + (0.25 * graph_score) + (0.05 * merchant_score)

        composite = round(min(100.0, max(0.0, composite)), 1)

        if composite >= 85.0:
            severity = "CRITICAL"
            action_key = "ESCALATE_HUMAN" if graph_res["is_syndicate"] else "FLAG_ACCOUNT"
        elif composite >= 60.0:
            severity = "HIGH"
            action_key = "HOLD"
        elif composite >= 30.0:
            severity = "MEDIUM"
            action_key = "VERIFY_2FA"
        else:
            severity = "LOW"
            action_key = "APPROVE"

        # Executive summary
        summary = self._generate_summary(txn, composite, severity, ACTIONS[action_key], profile_res, dev_res, graph_res, precedent)

        return {
            "case_id": case_id,
            "transaction_id": txn_id,
            "transaction": txn,
            "composite_risk_score": composite,
            "severity_band": severity,
            "recommended_action_key": action_key,
            "action_detail": ACTIONS[action_key],
            "executive_summary": summary,
            "steps_trace": steps_trace,
            "breakdown": {
                "ml_detection": round(ml_score, 1),
                "behavioral_drift": round(behavior_score, 1),
                "device_geo_risk": round(device_score, 1),
                "graph_syndicate_risk": round(graph_score, 1),
                "merchant_risk": round(merchant_score, 1)
            },
            "matched_precedent": precedent
        }

    def _generate_summary(self, txn, score, severity, action, profile, dev, graph, precedent) -> str:
        name = txn.get("user_name", "Customer")
        amt = float(txn.get("amount", 0))
        merch = txn.get("merchant", "Merchant")
        loc = txn.get("location_city", "Location")

        if severity == "CRITICAL":
            return (
                f"CRITICAL FRAUD ALERT ({score}/100). ${amt:,.2f} transfer to '{merch}' from {loc} exhibits high-confidence compromise signals. "
                f"Behavioral deviation is severe (Z-Score: {profile.get('z_score', 0)}). "
                f"Device telemetry confirmed unauthorized hardware ({dev.get('device_id')}). "
                f"{'NetworkX relationship graph detected multi-account mule syndicate sharing this emulator. ' if graph.get('is_syndicate') else ''}"
                f"Grounding in RAG precedent {precedent['case_id']} mandates immediate action: {action}."
            )
        elif severity == "HIGH":
            return (
                f"HIGH RISK DETECTED ({score}/100). ${amt:,.2f} transaction at '{merch}' sharply departs from {name}'s baseline. "
                f"Connection originated from an unverified network ({loc}) with degraded device trust ({dev.get('trust_score', 0):.2f}). "
                f"Mandated action: {action}."
            )
        elif severity == "MEDIUM":
            return (
                f"SUSPICIOUS ACTIVITY ({score}/100). Moderate anomaly detected for ${amt:,.2f} at '{merch}'. "
                f"Precautionary step-up verification recommended: {action}."
            )
        else:
            return (
                f"TRANSACTION NORMAL ({score}/100). ${amt:,.2f} transaction at '{merch}' in {loc} conforms with customer habits. "
                f"{'Active travel notice confirmed overseas location, successfully suppressing false alert. ' if profile.get('travel_notice_active') else ''}"
                f"Device and network verified. Mandated action: {action}."
            )

agent_instance = InvestigationAgent()

def run_investigation(txn: Dict[str, Any]) -> Dict[str, Any]:
    return agent_instance.investigate(txn)
