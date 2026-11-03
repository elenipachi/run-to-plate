"""Run-to-Plate web server.

Serves index.html and exposes a small, whitelisted set of environment
variables at /config.json so the browser app can read them.
Only standard library, no dependencies to install.
"""
import json
import os
import sys
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", "3000"))

# Only these variables are ever sent to the browser. Never add secrets here.
PUBLIC_VARS = ["APP_ENV", "APP_MESSAGE"]


def log(msg):
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"[{stamp}] {msg}", flush=True)


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.split("?")[0] == "/config.json":
            body = json.dumps({k: os.environ.get(k, "") for k in PUBLIC_VARS}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def log_message(self, fmt, *args):
        log(f"{self.address_string()} {fmt % args}")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    log("Run-to-Plate is starting")
    log(f"Python {sys.version.split()[0]}")
    for name in PUBLIC_VARS:
        value = os.environ.get(name)
        log(f"{name} = {value!r}" if value else f"{name} is not set")
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    log(f"Listening on http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log("Shutting down")
