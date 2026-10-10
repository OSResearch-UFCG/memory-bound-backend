import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

PORT = int(os.environ.get("PORT", "8080"))
DEFAULT_MB = 200
PAGE_SIZE = 4096


def allocate_and_touch(size_mb):
    size = size_mb * 1024 * 1024
    buffer = bytearray(size)

    # bytearray(size) pode vir de páginas ainda não mapeadas; escrever em cada
    # página força o SO a alocar memória física de verdade.
    for position in range(0, size, PAGE_SIZE):
        buffer[position] = 1

    total = 0
    for position in range(0, size, PAGE_SIZE):
        total += buffer[position]
    return total


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        mb = int(query.get("mb", [DEFAULT_MB])[0])

        pages_touched = allocate_and_touch(mb)

        body = json.dumps({"mb": mb, "pages_touched": pages_touched}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)


print(f"memory-bound-backend ouvindo na porta {PORT}")
HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
