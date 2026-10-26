"""FraudLens Configuration and Project Constants
"""

from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

# Application Metadata
APP_NAME = "FraudLens"
APP_SUBTITLE = "An Agentic AI System for Intelligent Fraud Investigation"
APP_VERSION = "2.0.0"

# Composite Risk Severity Bands (0 - 100)
RISK_THRESHOLDS = {
    "LOW": (0, 29),
    "MEDIUM": (30, 59),
    "HIGH": (60, 84),
    "CRITICAL": (85, 100),
}

# Mandated Safety Actions
ACTIONS = {
    "APPROVE": "Approve Transaction (Legitimate / Baseline Verified)",
    "VERIFY_2FA": "Request Additional Verification (Step-up 2FA/Biometric)",
    "HOLD": "Temporary Hold on Funds (Analyst Review Required)",
    "FLAG_ACCOUNT": "Flag Account & Restrict High-Risk Outbound Transfers",
    "ESCALATE_HUMAN": "Immediate Escalation to Financial Crimes Investigation Unit",
}
