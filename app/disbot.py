import discord
from discord.ext import commands
import os

# トークンは環境変数から取得
TOKEN = os.environ.get("DISCORD_TOKEN")

# Botのプレフィックス（コマンドの頭文字）を指定
bot = commands.Bot(command_prefix="!")

# Botが準備完了したときに呼ばれるイベント
@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user.name} ({bot.user.id})")

# !ping と入力されたときに反応するコマンド
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

# Botを実行
if __name__ == "__main
