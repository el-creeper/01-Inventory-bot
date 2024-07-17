import discord
import config
import asyncio

TOKEN = config.TOKEN
CHANNEL_ID = 1262755796723171421  # Remplacez par votre ID de canal

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Le Bot est prêt !")
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("Le bot fonctionne !")

    # Attendre 10 secondes
    await asyncio.sleep(10)

    # Éteindre le bot
    await channel.send("Le bot va maintenant s'éteindre.")
    await client.close()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    print(f"{message.author}: {message.content}")

client.run(TOKEN)
