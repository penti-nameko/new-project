import discord
from discord.ext import commands
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# ヘルスチェック用のHTTPサーバー
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def start_health_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("", port), HealthCheckHandler)
    print(f"Health server running on port {port}")
    server.serve_forever()

threading.Thread(target=start_health_server, daemon=True).start()

# ✅ Intents の設定（ここが追加点）
intents = discord.Intents.default()
intents.message_content = True  # メッセージ内容の取得を許可

# Discord Bot 本体
TOKEN = os.environ.get("DISCORD_TOKEN")
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user.name} ({bot.user.id})")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

if __name__ == "__main__":
    if TOKEN is None:
        print("DISCORD_TOKEN not set.")
    else:
        bot.run(TOKEN)
