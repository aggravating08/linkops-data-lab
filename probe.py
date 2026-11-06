"""Visible, non-destructive check of the sandbox boundary."""

import json
import os
import socket

report = {"network": "blocked", "rootfs_write": "denied", "inference_key_visible": False}
try:
    connection = socket.create_connection(("1.1.1.1", 443), timeout=1.5)
    connection.close()
    report["network"] = "reachable"
except OSError:
    pass
try:
    with open("/host-root-proof.txt", "w", encoding="utf-8") as handle:
        handle.write("probe")
    report["rootfs_write"] = "allowed"
except OSError:
    pass
report["inference_key_visible"] = bool(os.environ.get("VULTR_INFERENCE_API_KEY"))
print(json.dumps(report, separators=(",", ":")))
