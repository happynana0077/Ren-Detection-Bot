import os
from threading import Thread
import discord
from flask import Flask

# Renderのウェブチェック（ポート検出）を通過させるための軽量Webサーバー
app = Flask("")


@app.route("/")
def home():
    return "Bot is alive!"


def run_http():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


# バックグラウンドでWebサーバーを起動
Thread(target=run_http).start()

# Discord Botの処理
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"ログインしました: {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    text = message.content

    if "レン" in text and "ヴァレンチーナ" not in text:
        await message.channel.send("文章からレンが検出されました‼️")


token = os.environ.get("DISCORD_TOKEN")
client.run(token)
