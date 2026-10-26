"""Customer Behavioral Baseline Profiling
Compares incoming transactions against personal historical distributions and travel advisories.
"""

from typing import Dict, Any
from datetime import datetime
from .data import SEED_USERS

def analyze_behavioral_profile(txn: Dict[str, Any]) -> Dict[str, Any]:
    user_id = txn.get("user_id")
    user = SEED_USERS.get(user_id)

    if not user:
        return {
            "user_id": user_id,
            "deviation_score": 45.0,
            "z_score": 0.0,
            "anomalies": ["Unprofiled customer: Default baseline applied"],
            "travel_notice_active": False
        }

    baseline = user["baseline"]
    amount = float(txn.get("amount", 0.0))
    avg_amt = baseline["avg_amount"]
    std_amt = max(baseline["std_amount"], 5.0)

    z_score = round((amount - avg_amt) / std_amt, 2)
    amount_ratio = round(amount / max(avg_amt, 1.0), 1)

    anomalies = []
    points = 0.0

    # 1. Amount Deviation
    if z_score > 3.0:
        points += 35.0
        anomalies.append(f"Extreme amount deviation: ${amount:,.2f} is {amount_ratio}x higher than customer average (${avg_amt:,.2f}, Z-score: {z_score})")
    elif z_score > 1.8:
        points += 15.0
        anomalies.append(f"Elevated amount: ${amount:,.2f} exceeds typical spend band (Z-score: {z_score})")

    # 2. Category Check
    cat = txn.get("merchant_category", "").lower()
    typical_cats = [c.lower() for c in baseline.get("typical_categories", [])]
    if cat and cat not in typical_cats:
        points += 20.0
        anomalies.append(f"Unprecedented merchant category: '{cat}' has never been used by customer")

    # 3. Off-Hours Check
    ts = txn.get("timestamp", "")
    hour = 12
    if "T" in ts:
        try:
            hour = int(ts.split("T")[1].split(":")[0])
        except Exception:
            hour = 12
    active_hours = baseline.get("active_hours", list(range(24)))
    if hour not in active_hours:
        points += 20.0
        anomalies.append(f"Off-hours activity: Initiated at {hour:02d}:00 UTC (Habitual active window: {min(active_hours):02d}:00 - {max(active_hours):02d}:00)")

    # 4. Device and IP Recognition
    dev_id = txn.get("device_id", "")
    ip_addr = txn.get("ip_address", "")
    if dev_id not in user.get("known_devices", []):
        points += 20.0
        anomalies.append(f"Unregistered hardware device: '{dev_id}' is not in trusted device list")
    if ip_addr not in user.get("known_ips", []):
        points += 10.0
        anomalies.append(f"New network connection IP: '{ip_addr}' ({txn.get('location_city', 'Unknown')})")

    # 5. Travel Notice Mitigation (False Positive Defense)
    travel_active = baseline.get("travel_notice_active", False)
    travel_dest = baseline.get("travel_destination", "")
    loc = txn.get("location_city", "")

    if travel_active and travel_dest.lower() in loc.lower():
        points = max(5.0, points - 35.0)
        anomalies.append(f"Legitimate Travel Corroboration: Customer filed travel advisory for '{travel_dest}', matching current transaction location")

    final_score = round(min(100.0, max(0.0, points)), 1)

    return {
        "user_id": user_id,
        "user_name": user["name"],
        "home_city": user["home_city"],
        "historical_avg": avg_amt,
        "z_score": z_score,
        "deviation_score": final_score,
        "travel_notice_active": travel_active,
        "anomalies": anomalies if anomalies else ["All attributes conform to customer historical baseline"]
    }
