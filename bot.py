@bot.event
async def on_ready():
    print(f"[INFO] Bot Online: {bot.user}")

    # ステータス表示
    await bot.change_presence(activity=discord.Game(name="/help_me でコマンドを見る"))

    # スラッシュコマンドを毎回同期
    try:
        synced = await bot.tree.sync()
        print(f"✅ スラッシュコマンド同期完了: {len(synced)} 件")
    except Exception as e:
        print(f"❌ スラッシュコマンド同期失敗: {e}")

    # 各サーバーにログメッセージ送信
    for guild in bot.guilds:
        log_channel = discord.utils.find(
            lambda c: c.name == "ログ" and c.permissions_for(guild.me).send_messages,
            guild.text_channels
        )
        if log_channel:
            try:
                await send_content(log_channel, message="おはよ...ムニャ")
                await send_content(log_channel, message=f"🔁 スラッシュコマンド {len(synced)} 件を同期しました")
                print(f"✅ 起動ログ送信: {guild.name} → #{log_channel.name}")
            except Exception as e:
                print(f"❌ 起動ログ送信失敗: {guild.name}: {e}")
        else:
            print(f"⚠️ ログチャンネルが見つからない: {guild.name}")
