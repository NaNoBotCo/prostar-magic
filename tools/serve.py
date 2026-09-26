#!/usr/bin/env python3
"""serve.py — docs/ over HTTP for a local look. PORT from argv or the environment."""
import functools, http.server, os, socketserver, sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "docs"
PORT = int(os.environ.get("PORT") or (sys.argv[1] if len(sys.argv) > 1 else 8852))
socketserver.TCPServer.allow_reuse_address = True
print(f"http://localhost:{PORT}/", flush=True)
socketserver.TCPServer(("", PORT), functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(SITE))).serve_forever()
