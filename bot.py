import discord
from discord.ext import commands
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from flask import Flask, request
import asyncio
import signal

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("スラッシュコマンドを同期しました。")


intents = discord.Intents.default()
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def send_log_to_all_guilds(message: str):
    for guild in bot.guilds:
        log_channel = discord.utils.get(guild.text_channels, name="ログ")
        if log_channel:
            try:
                await log_channel.send(message)
            except Exception as e:
                print(f"{guild.name}のログチャンネルへの送信に失敗: {e}")

@bot.event
async def on_ready():
    print(f"Bot {bot.user} としてログインしました。")
    await send_log_to_all_guilds("✅ Botが起動しました。")

# 安全なシャットダウン処理
def shutdown():
    loop = asyncio.get_event_loop()
    loop.create_task(send_log_to_all_guilds("🛑 Botが終了します。"))
    loop.create_task(bot.close())

def handle_exit(*args):
    shutdown()

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)


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

app = Flask(__name__)

@app.route("/", methods=["GET", "HEAD"])
def index():
    if request.method == "HEAD":
        return "", 200
    return "OK", 200

@bot.tree.command(name="ping", description="Pong を返します")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!")


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
