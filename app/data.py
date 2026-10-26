"""Seed Data for FraudLens
Provides realistic transactions, customer behavioral profiles, and relationship graph entities.
"""

SEED_USERS = {
    "USR_101": {
        "user_id": "USR_101",
        "name": "Sarah Jenkins",
        "account_id": "ACC_88101",
        "home_city": "Seattle, WA, USA",
        "primary_device": "DEV_SARAH_IPHONE",
        "primary_ip": "73.189.44.12",
        "known_devices": ["DEV_SARAH_IPHONE", "DEV_SARAH_MACBOOK"],
        "known_ips": ["73.189.44.12"],
        "baseline": {
            "avg_amount": 78.50,
            "std_amount": 42.00,
            "max_historical_amount": 650.00,
            "typical_categories": ["groceries", "dining", "travel", "utilities"],
            "active_hours": [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
            "travel_notice_active": False,
        }
    },
    "USR_102": {
        "user_id": "USR_102",
        "name": "Liam O'Connor",
        "account_id": "ACC_88102",
        "home_city": "Dublin, Ireland",
        "primary_device": "DEV_LIAM_PIXEL",
        "primary_ip": "89.101.44.77",
        "known_devices": ["DEV_LIAM_PIXEL", "DEV_LIAM_IPAD"],
        "known_ips": ["89.101.44.77", "185.220.10.4"],
        "baseline": {
            "avg_amount": 115.00,
            "std_amount": 65.00,
            "max_historical_amount": 1200.00,
            "typical_categories": ["travel", "software", "dining", "lodging"],
            "active_hours": [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
            "travel_notice_active": True,
            "travel_destination": "Lisbon, Portugal",
        }
    },
    "USR_103": {
        "user_id": "USR_103",
        "name": "Marcus Vance",
        "account_id": "ACC_88103",
        "home_city": "Miami, FL, USA",
        "primary_device": "DEV_UNKNOWN_SAMSUNG",
        "primary_ip": "194.26.29.112",
        "known_devices": ["DEV_UNKNOWN_SAMSUNG", "DEV_BOT_EMU_77"],
        "known_ips": ["194.26.29.112"],
        "baseline": {
            "avg_amount": 45.00,
            "std_amount": 25.00,
            "max_historical_amount": 180.00,
            "typical_categories": ["convenience", "fuel"],
            "active_hours": [12, 13, 14, 18, 19, 20],
            "travel_notice_active": False,
        }
    },
    "USR_104": {
        "user_id": "USR_104",
        "name": "Elena Rostova",
        "account_id": "ACC_88104",
        "home_city": "Chicago, IL, USA",
        "primary_device": "DEV_ELENA_GALAXY",
        "primary_ip": "67.164.21.90",
        "known_devices": ["DEV_ELENA_GALAXY", "DEV_BOT_EMU_77"],
        "known_ips": ["67.164.21.90", "194.26.29.112"],
        "baseline": {
            "avg_amount": 62.00,
            "std_amount": 30.00,
            "max_historical_amount": 350.00,
            "typical_categories": ["groceries", "pharmacy", "retail"],
            "active_hours": [9, 10, 11, 14, 15, 17, 18, 19],
            "travel_notice_active": False,
        }
    },
    "USR_105": {
        "user_id": "USR_105",
        "name": "David Chen",
        "account_id": "ACC_88105",
        "home_city": "San Francisco, CA, USA",
        "primary_device": "DEV_DAVID_IPHONE",
        "primary_ip": "98.210.15.44",
        "known_devices": ["DEV_DAVID_IPHONE", "DEV_DAVID_MAC"],
        "known_ips": ["98.210.15.44"],
        "baseline": {
            "avg_amount": 88.00,
            "std_amount": 40.00,
            "max_historical_amount": 900.00,
            "typical_categories": ["dining", "groceries", "tech", "travel"],
            "active_hours": [8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 20],
            "travel_notice_active": False,
        }
    },
    "USR_106": {
        "user_id": "USR_106",
        "name": "Amina Al-Mansoor",
        "account_id": "ACC_88106",
        "home_city": "Dubai, UAE",
        "primary_device": "DEV_AMINA_IPHONE",
        "primary_ip": "94.200.12.5",
        "known_devices": ["DEV_AMINA_IPHONE"],
        "known_ips": ["94.200.12.5"],
        "baseline": {
            "avg_amount": 320.00,
            "std_amount": 150.00,
            "max_historical_amount": 3500.00,
            "typical_categories": ["luxury", "dining", "travel"],
            "active_hours": [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
            "travel_notice_active": False,
        }
    }
}

SEED_TRANSACTIONS = [
    {
        "id": "TXN_101",
        "user_id": "USR_101",
        "user_name": "Sarah Jenkins",
        "account_id": "ACC_88101",
        "amount": 4850.00,
        "currency": "USD",
        "timestamp": "2026-10-24T03:14:22Z",
        "merchant": "Apex Crypto Exchange",
        "merchant_category": "cryptocurrency",
        "merchant_risk_score": 0.92,
        "device_id": "DEV_UNKNOWN_LINUX_EMU",
        "device_trust_score": 0.15,
        "ip_address": "102.89.23.4",
        "location_city": "Lagos, Nigeria",
        "scenario_type": "ACCOUNT_TAKEOVER_BURST",
        "scenario_title": "Account Takeover & Sudden Crypto Drain",
        "description": "Sudden $4,850 transfer at 3:14 AM from Lagos IP on an unrecognized Linux emulator."
    },
    {
        "id": "TXN_102",
        "user_id": "USR_102",
        "user_name": "Liam O'Connor",
        "account_id": "ACC_88102",
        "amount": 320.00,
        "currency": "EUR",
        "timestamp": "2026-10-24T11:42:10Z",
        "merchant": "Pasteis de Belem Lisbon",
        "merchant_category": "dining",
        "merchant_risk_score": 0.12,
        "device_id": "DEV_LIAM_PIXEL",
        "device_trust_score": 0.95,
        "ip_address": "185.220.10.4",
        "location_city": "Lisbon, Portugal",
        "scenario_type": "TRAVEL_FALSE_POSITIVE_CHECK",
        "scenario_title": "International Travel Outlier (False Positive Test)",
        "description": "In-person dining in Lisbon on registered Pixel phone. Prior travel notice was filed."
    },
    {
        "id": "TXN_103",
        "user_id": "USR_103",
        "user_name": "Marcus Vance",
        "account_id": "ACC_88103",
        "amount": 1450.00,
        "currency": "USD",
        "timestamp": "2026-10-24T08:20:15Z",
        "merchant": "Mule Vault PeerTransfer",
        "merchant_category": "p2p_wire",
        "merchant_risk_score": 0.88,
        "device_id": "DEV_BOT_EMU_77",
        "device_trust_score": 0.20,
        "ip_address": "194.26.29.112",
        "location_city": "Bucharest, Romania",
        "scenario_type": "ORGANIZED_MULE_RING",
        "scenario_title": "Syndicate Mule Ring Funneling",
        "description": "P2P transfer originating from shared bot emulator DEV_BOT_EMU_77 linked to multiple accounts."
    },
    {
        "id": "TXN_104",
        "user_id": "USR_104",
        "user_name": "Elena Rostova",
        "account_id": "ACC_88104",
        "amount": 1380.00,
        "currency": "USD",
        "timestamp": "2026-10-24T08:32:00Z",
        "merchant": "Mule Vault PeerTransfer",
        "merchant_category": "p2p_wire",
        "merchant_risk_score": 0.88,
        "device_id": "DEV_BOT_EMU_77",
        "device_trust_score": 0.20,
        "ip_address": "194.26.29.112",
        "location_city": "Bucharest, Romania",
        "scenario_type": "ORGANIZED_MULE_RING",
        "scenario_title": "Syndicate Mule Ring Linked Account",
        "description": "Second linked account using identical bot emulator and Romanian proxy to the same recipient."
    },
    {
        "id": "TXN_105",
        "user_id": "USR_106",
        "user_name": "Amina Al-Mansoor",
        "account_id": "ACC_88106",
        "amount": 890.00,
        "currency": "USD",
        "timestamp": "2026-10-24T02:04:12Z",
        "merchant": "Global Key Digital Store",
        "merchant_category": "digital_goods",
        "merchant_risk_score": 0.85,
        "device_id": "DEV_TOR_BROWSER",
        "device_trust_score": 0.10,
        "ip_address": "185.220.101.5",
        "location_city": "Frankfurt, Germany",
        "scenario_type": "CARD_TESTING_BURST",
        "scenario_title": "Automated Tor Card Testing Burst",
        "description": "Tor exit node card testing attempt followed by high-value instant digital key purchase."
    },
    {
        "id": "TXN_106",
        "user_id": "USR_105",
        "user_name": "David Chen",
        "account_id": "ACC_88105",
        "amount": 48.75,
        "currency": "USD",
        "timestamp": "2026-10-24T09:15:33Z",
        "merchant": "Blue Bottle Coffee",
        "merchant_category": "dining",
        "merchant_risk_score": 0.05,
        "device_id": "DEV_DAVID_IPHONE",
        "device_trust_score": 0.98,
        "ip_address": "98.210.15.44",
        "location_city": "San Francisco, CA, USA",
        "scenario_type": "NORMAL_BASELINE",
        "scenario_title": "Routine Baseline Purchase",
        "description": "Morning coffee purchase on trusted iPhone matching customer historical habit."
    }
]

# Network Topology Entities
SEED_GRAPH_NODES = [
    {"id": "USR_101", "label": "Sarah Jenkins", "type": "USER", "risk": "HIGH", "detail": "Customer user. Primary account holder targeted in sudden off-hours account takeover."},
    {"id": "USR_102", "label": "Liam O'Connor", "type": "USER", "risk": "LOW", "detail": "Customer user traveling internationally in Lisbon with pre-authorized travel advisory."},
    {"id": "USR_103", "label": "Marcus Vance", "type": "USER", "risk": "CRITICAL", "detail": "Syndicate mule recruiter operating dummy accounts via a centralized bot emulator."},
    {"id": "USR_104", "label": "Elena Rostova", "type": "USER", "risk": "CRITICAL", "detail": "Compromised mule account linked to identical bot emulator hardware fingerprint."},
    {"id": "USR_105", "label": "David Chen", "type": "USER", "risk": "LOW", "detail": "Verified customer with regular corporate business baseline in San Francisco."},
    {"id": "USR_106", "label": "Amina Al-Mansoor", "type": "USER", "risk": "HIGH", "detail": "High net-worth e-commerce customer targeted in automated card testing burst."},

    {"id": "ACC_88101", "label": "Account ..8101", "type": "ACCOUNT", "risk": "HIGH", "detail": "Checking account owned by Sarah Jenkins. Subject to unauthorized transfer request."},
    {"id": "ACC_88102", "label": "Account ..8102", "type": "ACCOUNT", "risk": "LOW", "detail": "Premier account owned by Liam O'Connor. Legitimate POS physical dining swipe."},
    {"id": "ACC_88103", "label": "Account ..8103", "type": "ACCOUNT", "risk": "CRITICAL", "detail": "Mule account owned by Marcus Vance. Funneling rapid P2P cashout transfers."},
    {"id": "ACC_88104", "label": "Account ..8104", "type": "ACCOUNT", "risk": "CRITICAL", "detail": "Mule account owned by Elena Rostova. Funneling funds to common cashout wallet."},
    {"id": "ACC_88105", "label": "Account ..8105", "type": "ACCOUNT", "risk": "LOW", "detail": "Primary checking account owned by David Chen. Normal routine payments."},
    {"id": "ACC_88106", "label": "Account ..8106", "type": "ACCOUNT", "risk": "HIGH", "detail": "Platinum card account owned by Amina Al-Mansoor. Target of card testing micro-burst."},

    {"id": "DEV_SARAH_IPHONE", "label": "Sarah iPhone", "type": "DEVICE", "risk": "LOW", "detail": "Trusted customer mobile phone (iPhone 14 Pro, Trust Score: 0.97)."},
    {"id": "DEV_LIAM_PIXEL", "label": "Liam Pixel", "type": "DEVICE", "risk": "LOW", "detail": "Trusted customer mobile device (Google Pixel 8, Trust Score: 0.95)."},
    {"id": "DEV_DAVID_IPHONE", "label": "David iPhone", "type": "DEVICE", "risk": "LOW", "detail": "Trusted customer smartphone (iPhone 15, Trust Score: 0.98)."},
    {"id": "DEV_UNKNOWN_LINUX_EMU", "label": "Linux Emulator", "type": "DEVICE", "risk": "CRITICAL", "detail": "Headless Linux QEMU virtual machine spoofing browser headers (Trust: 0.15)."},
    {"id": "DEV_BOT_EMU_77", "label": "Bot Emulator #77 (Shared)", "type": "DEVICE", "risk": "CRITICAL", "detail": "CRITICAL SYNDICATE ANOMALY: Nox Android emulator fingerprint concurrently shared by ACC_88103 and ACC_88104!"},
    {"id": "DEV_TOR_BROWSER", "label": "Tor Browser", "type": "DEVICE", "risk": "CRITICAL", "detail": "Tor anonymized browser bundle with blocked HTML5 canvas fingerprinting (Trust: 0.10)."},

    {"id": "IP_73_189", "label": "73.189.44.12 (Seattle)", "type": "IP", "risk": "LOW", "detail": "Comcast residential ISP connection located in Seattle, WA."},
    {"id": "IP_98_210", "label": "98.210.15.44 (SF)", "type": "IP", "risk": "LOW", "detail": "AT&T Fiber residential broadband connection in San Francisco, CA."},
    {"id": "IP_102_89", "label": "102.89.23.4 (Lagos)", "type": "IP", "risk": "CRITICAL", "detail": "Commercial hosting/datacenter proxy ASN located in Lagos, Nigeria."},
    {"id": "IP_194_26", "label": "194.26.29.112 (Bucharest)", "type": "IP", "risk": "CRITICAL", "detail": "M247 bulletproof VPN tunnel used by multi-account bot emulator cluster."},
    {"id": "IP_185_220", "label": "185.220.101.5 (Frankfurt)", "type": "IP", "risk": "CRITICAL", "detail": "Known high-risk Tor relay exit node in Frankfurt, Germany."},

    {"id": "MERCH_APEX", "label": "Apex Crypto", "type": "MERCHANT", "risk": "CRITICAL", "detail": "High-risk offshore cryptocurrency exchange and instant liquid off-ramp."},
    {"id": "MERCH_MULE_VAULT", "label": "Mule Vault P2P", "type": "MERCHANT", "risk": "CRITICAL", "detail": "Unlicensed peer-to-peer escrow cashout hub utilized by syndicate mules."},
    {"id": "MERCH_BLUEBOTTLE", "label": "Blue Bottle Coffee", "type": "MERCHANT", "risk": "LOW", "detail": "Verified merchant (Dining/Coffee shop in San Francisco)."},
    {"id": "MERCH_DIGITAL_KEYS", "label": "Digital Key Store", "type": "MERCHANT", "risk": "HIGH", "detail": "Instant digital vouchers and gaming product keys, common target of card testing."}
]

SEED_GRAPH_EDGES = [
    # Sarah Jenkins ATO
    {"source": "USR_101", "target": "ACC_88101", "relation": "OWNS"},
    {"source": "ACC_88101", "target": "DEV_UNKNOWN_LINUX_EMU", "relation": "SUSPICIOUS_LOGIN", "alert": True},
    {"source": "DEV_UNKNOWN_LINUX_EMU", "target": "IP_102_89", "relation": "CONNECTED_FROM", "alert": True},
    {"source": "DEV_UNKNOWN_LINUX_EMU", "target": "MERCH_APEX", "relation": "TRANSFER_TO", "alert": True},

    # Liam Travel
    {"source": "USR_102", "target": "ACC_88102", "relation": "OWNS"},
    {"source": "USR_102", "target": "DEV_LIAM_PIXEL", "relation": "OWNS_DEVICE"},

    # Syndicate Mule Ring: Shared device DEV_BOT_EMU_77 between USR_103 and USR_104!
    {"source": "USR_103", "target": "ACC_88103", "relation": "OWNS"},
    {"source": "USR_104", "target": "ACC_88104", "relation": "OWNS"},
    {"source": "ACC_88103", "target": "DEV_BOT_EMU_77", "relation": "SHARED_HARDWARE", "alert": True},
    {"source": "ACC_88104", "target": "DEV_BOT_EMU_77", "relation": "SHARED_HARDWARE", "alert": True},
    {"source": "DEV_BOT_EMU_77", "target": "IP_194_26", "relation": "PROXY_TUNNEL", "alert": True},
    {"source": "ACC_88103", "target": "MERCH_MULE_VAULT", "relation": "CASH_OUT", "alert": True},
    {"source": "ACC_88104", "target": "MERCH_MULE_VAULT", "relation": "CASH_OUT", "alert": True},

    # David Chen Normal
    {"source": "USR_105", "target": "ACC_88105", "relation": "OWNS"},
    {"source": "ACC_88105", "target": "DEV_DAVID_IPHONE", "relation": "TRUSTED_DEVICE"},
    {"source": "DEV_DAVID_IPHONE", "target": "IP_98_210", "relation": "RESIDENTIAL_IP"},
    {"source": "ACC_88105", "target": "MERCH_BLUEBOTTLE", "relation": "AUTHORIZED_PAYMENT"},

    # Amina Tor Card Testing
    {"source": "USR_106", "target": "ACC_88106", "relation": "OWNS"},
    {"source": "ACC_88106", "target": "DEV_TOR_BROWSER", "relation": "TOR_SESSION", "alert": True},
    {"source": "DEV_TOR_BROWSER", "target": "IP_185_220", "relation": "TOR_EXIT_RELAY", "alert": True},
    {"source": "DEV_TOR_BROWSER", "target": "MERCH_DIGITAL_KEYS", "relation": "CARD_TESTING", "alert": True}
]
