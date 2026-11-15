import os
import discord
from discord import app_commands
import docker
from dotenv import load_dotenv

load_dotenv()
client = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(client)

@tree.command(name="pouf", description="ping the bot")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong")

@client.event
async def on_ready():
    synced = await tree.sync()
    print(f"✅ Connecté : {client.user} — commandes synchronisées {[cmd.name for cmd in synced]}")

if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    if not TOKEN:
        raise SystemExit("DISCORD_TOKEN environment variable not set.")
    client.run(TOKEN)    