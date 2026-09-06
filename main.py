from collections import deque
import os
import random
import time
from threading import Thread
import discord
from flask import Flask

# Renderのポート検出を通過させるための軽量Webサーバー
app = Flask(__name__)


@app.route("/")
def home():
    return "Bot is alive!", 200


def run_http():
    # Renderが指定するPORT環境変数を確実に取得（デフォルトは10000）
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


# バックグラウンドでWebサーバーを起動
Thread(target=run_http, daemon=True).start()

# Discord Botの処理
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# 呼び出された時刻を記録するリスト（チャンネルごと）
call_timestamps = {}


@client.event
async def on_ready():
    print(f"ログインしました: {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    text = message.content

    # 文章から「ヴァレンチーナ」を一時的に除去する
    text_without_valentina = text.replace("ヴァレンチーナ", "")

    # キーワード定義
    ren_keywords = ["レン", "れん", "ﾚﾝ"]
    reso_keywords = ["レソ", "れそ", "ﾚｿ"]

    # 1. まず「レン」が含まれているかを最優先で判定
    if any(keyword in text_without_valentina for keyword in ren_keywords):
        now = time.time()
        channel_id = message.channel.id

        if channel_id not in call_timestamps:
            call_timestamps[channel_id] = deque()

        timestamps = call_timestamps[channel_id]

        # 30秒より古い記録を削除
        while timestamps and now - timestamps[0] > 30:
            timestamps.popleft()

        # 今回の呼び出し時刻を記録
        timestamps.append(now)

        # 30秒以内に5回以上呼び出された場合
        if len(timestamps) >= 5:
            await message.channel.send(
                "……何度もお呼びにならずとも、聞こえております。"
            )
        else:
            # 5%の確率でレアメッセージ
            if random.random() < 0.05:
                await message.channel.send(
                    "主様、お呼びでございましょうか。ご用件がございましたら、何なりとお申し付けくださいませ。"
                )
            else:
                await message.channel.send("小生をお呼びでございましょうか？")

    # 2. 「レン」が含まれておらず、「レソ」が含まれている場合の判定
    elif any(keyword in text_without_valentina for keyword in reso_keywords):
        await message.channel.send(
            "小生をお呼びに…ああ、違いましたか。失礼いたしました。"
        )


token = os.environ.get("DISCORD_TOKEN")
if token:
    client.run(token)
