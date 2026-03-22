import os
import time
import random
from datetime import datetime, timezone
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

THREAT_TYPES = [
    "SQL Injection", "XSS Attempt", "Brute Force", "Port Scan",
    "DDoS Probe", "Path Traversal", "SSRF Attempt", "RCE Attempt",
    "CSRF Bypass", "Token Theft",
]

REGIONS = [
    ("Russia", "RU", 55.75, 37.62), ("China", "CN", 39.91, 116.39),
    ("Iran", "IR", 35.69, 51.42), ("North Korea", "KP", 39.02, 125.75),
    ("Brazil", "BR", -23.55, -46.63), ("Nigeria", "NG", 6.52, 3.38),
    ("Germany", "DE", 52.52, 13.41), ("United States", "US", 37.09, -95.71),
    ("India", "IN", 20.59, 78.96), ("Romania", "RO", 45.94, 24.97),
]

SEVERITY = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
SEVERITY_WEIGHTS = [0.35, 0.30, 0.20, 0.15]
START_TIME = time.time()


def generate_threat():
    region = random.choice(REGIONS)
    return {
        "id": f"THR-{random.randint(10000, 99999)}",
        "type": random.choice(THREAT_TYPES),
        "severity": random.choices(SEVERITY, weights=SEVERITY_WEIGHTS, k=1)[0],
        "country": region[0],
        "country_code": region[1],
        "lat": region[2] + random.uniform(-2, 2),
        "lon": region[3] + random.uniform(-2, 2),
        "ip": f"{random.randint(1,254)}.{random.randint(0,254)}.{random.randint(0,254)}.{random.randint(1,254)}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "blocked": random.choice([True, True, True, False]),
        "confidence": random.randint(60, 99),
    }


def generate_stats():
    uptime_s = int(time.time() - START_TIME)
    h, m, s = uptime_s // 3600, (uptime_s % 3600) // 60, uptime_s % 60
    return {
        "threats_blocked": random.randint(14820, 14900),
        "active_sessions": random.randint(1200, 1800),
        "requests_per_second": round(random.uniform(340, 420), 1),
        "threat_score": random.randint(62, 78),
        "uptime": f"{h:02d}:{m:02d}:{s:02d}",
        "nodes_protected": 47,
        "rules_active": 2341,
        "avg_block_time_ms": round(random.uniform(0.8, 2.1), 2),
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/threats")
def api_threats():
    count = min(int(request.args.get("count", 12)), 50)
    return jsonify([generate_threat() for _ in range(count)])


@app.route("/api/stats")
def api_stats():
    return jsonify(generate_stats())


@app.route("/api/timeline")
def api_timeline():
    now = int(time.time())
    return jsonify([{
        "t": now - (i * 10),
        "critical": random.randint(0, 4),
        "high": random.randint(2, 12),
        "medium": random.randint(5, 25),
        "low": random.randint(10, 40),
    } for i in range(60, 0, -1)])


@app.route("/health")
def health():
    return jsonify({"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}), 200


@app.route("/ready")
def ready():
    return jsonify({"status": "ready"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
