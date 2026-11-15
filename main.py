import os
import discord
from discord import app_commands
import docker
from dotenv import load_dotenv

load_dotenv()
client = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(client)
dkclient = docker.from_env()
CONTAINERS_ALLOWED = os.getenv("CONTAINERS_ALLOWED").split(",")

@tree.command(name="pouf", description="ping the bot")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong")
    
@tree.command(name="list_containers", description="List all Docker containers")
async def list_containers(interaction: discord.Interaction):
    containers_recovered = []
    for container_allowed in CONTAINERS_ALLOWED:
        container = dkclient.containers.get(container_allowed)
        containers_recovered.append(container) 
    containers_lines = "\n".join(f"- {container.name} : {container.status}" for container in containers_recovered)
    message = f"Here is the list of the containers : \n{containers_lines}"
    await interaction.response.send_message(message)

@tree.command(name="docker_start", description="Start a container from the allowed list")
async def docker_start(interaction: discord.Interaction, container_name: str):
    container = dkclient.containers.get(container_name)
    await container.start()
    await interaction.response.send_message(f"Container {container_name} successfully started !")

@tree.command(name="docker_stop", description="Stop a container from the allowed list")
async def docker_stop(interaction: discord.Interaction, container_name: str):
    await interaction.response.send_message("Container successfully stoped !")

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