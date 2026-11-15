import os
import discord
from discord import app_commands
import docker
from dotenv import load_dotenv

load_dotenv()
client = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(client)
dkclient = docker.from_env()

@tree.command(name="pouf", description="ping the bot")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong")
    
@tree.command(name="list_containers", description="List all Docker containers")
async def list_containers(interaction: discord.Interaction):
    containers = dkclient.containers.list(all=True)
    for container in containers:
        print(container.name, container.status)
        
    await interaction.response.send_message(f"Container: {containers}, Status: {containers}")

@client.event
async def on_ready():
    guild = discord.Object(id=os.getenv("GUILD_ID"))
    synced = await tree.sync(guild=guild)
    print(f"✅ Connecté : {client.user} — commandes synchronisées {[cmd.name for cmd in synced]}")

if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    if not TOKEN:
        raise SystemExit("DISCORD_TOKEN environment variable not set.")
    client.run(TOKEN)    