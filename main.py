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


token = os.environ.get("MTU0NjA3MTU2NDQ5MDEyMTI0Ng.G26dQJ.5JgTJGphHd4mzvPCiJaT-ZGgFVssj9BVKJ-IyM")
client.run(token)
