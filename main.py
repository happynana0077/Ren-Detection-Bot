import os
import discord

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


# トークンはコードに直書きせず環境変数から読み込む
token = os.environ.get("DISCORD_TOKEN")
client.run(token)
