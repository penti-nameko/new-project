import discord
from discord.ext import commands
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# ==========================
# HTTPサーバー（ヘルスチェック用）
# ==========================

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def start_health_server():
    port = int(os.environ.get("PORT", 8080))  # KoyebはPORT環境変数を使う
    server = HTTPServer(("", port), HealthCheckHandler)
    print(f"Health check server running on port {port}")
    server.serve_forever()

# 別スレッドで起動
threading.Thread(target=start_health_server, daemon=True).start()

# ==========================
# Discord Bot部分
# ==========================

TOKEN = os.env
