import json
import time
import urllib.request
from statistics import mean
from pathlib import Path

URLS = [
    "http://127.0.0.1:8010/healthz",
    "http://127.0.0.1:8010/benchmark/latest",
    "http://127.0.0.1:8010/gate/latest",
]

latencies = []
errors = 0
requests = 30

for i in range(requests):
    url = URLS[i % len(URLS)]
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(url, timeout=3) as resp:
            resp.read()
            if resp.status >= 400:
                errors += 1
    except Exception:
        errors += 1
    latencies.append(time.perf_counter() - start)

result = {
    "requests": requests,
    "errors": errors,
    "avg_latency_ms": round(mean(latencies) * 1000, 2),
    "max_latency_ms": round(max(latencies) * 1000, 2),
    "note": "Local smoke-load test only; not production-scale performance validation.",
}

Path("load_tests/local_api_smoke_load_results.json").write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2))
