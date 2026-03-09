#!/usr/bin/env python3
"""GPU monitoring script — logs metrics to file and optionally alerts."""
import time
import subprocess
import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("/var/log/gpu_monitor.log")
ALERT_TEMP_C = 85
ALERT_MEMORY_PCT = 95

def get_gpu_stats():
    """Query nvidia-smi for GPU metrics."""
    result = subprocess.run(
        [
            "nvidia-smi",
            "--query-gpu=timestamp,name,temperature.gpu,utilization.gpu,"
            "utilization.memory,memory.used,memory.total,power.draw",
            "--format=csv,noheader,nounits",
        ],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()

def check_alerts(stats_line):
    """Check if any GPU metrics exceed thresholds."""
    parts = [p.strip() for p in stats_line.split(",")]
    if len(parts) >= 7:
        temp = float(parts[2])
        mem_used = float(parts[5])
        mem_total = float(parts[6])
        mem_pct = (mem_used / mem_total) * 100 if mem_total > 0 else 0

        alerts = []
        if temp >= ALERT_TEMP_C:
            alerts.append(f"HIGH TEMP: {temp}C (threshold: {ALERT_TEMP_C}C)")
        if mem_pct >= ALERT_MEMORY_PCT:
            alerts.append(f"HIGH MEMORY: {mem_pct:.1f}% (threshold: {ALERT_MEMORY_PCT}%)")
        return alerts
    return []

if __name__ == "__main__":
    while True:
        stats = get_gpu_stats()
        timestamp = datetime.now().isoformat()
        log_line = f"{stats}\n"

        with open(LOG_FILE, "a") as f:
            f.write(log_line)

        for line in stats.split("\n"):
            alerts = check_alerts(line)
            for alert in alerts:
                with open(LOG_FILE, "a") as f:
                    f.write(f"ALERT [{timestamp}]: {alert}\n")

        time.sleep(30)
