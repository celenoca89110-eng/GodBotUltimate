import discord
from discord.ext import commands
import os

# Create bot with necessary intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} is connected!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

# Slash command: /ping
@bot.tree.command(name="ping", description="Shows bot latency")
async def ping(interaction: discord.Interaction):
    latency = bot.latency * 1000
    await interaction.response.send_message(f"Pong! 🏓 Latency: {latency:.2f}ms")

# Slash command: /hello
@bot.tree.command(name="hello", description="Greets the user")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hi {interaction.user.mention}! 👋")

# Slash command: /info
@bot.tree.command(name="info", description="Shows server info")
async def info(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(
        title=f"Info of {guild.name}",
        color=discord.Color.blue()
    )
    embed.add_field(name="Members", value=guild.member_count, inline=False)
    embed.add_field(name="Created", value=guild.created_at.strftime("%d/%m/%Y"), inline=False)
    await interaction.response.send_message(embed=embed)

# Slash command: /user
@bot.tree.command(name="user", description="Shows user info")
async def user(interaction: discord.Interaction, member: discord.User = None):
    if member is None:
        member = interaction.user
    
    embed = discord.Embed(
        title=f"Info of {member.name}",
        color=discord.Color.green()
    )
    embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
    embed.add_field(name="ID", value=member.id, inline=False)
    embed.add_field(name="Created", value=member.created_at.strftime("%d/%m/%Y"), inline=False)
    await interaction.response.send_message(embed=embed)

# Run bot
token = os.getenv("DISCORD_TOKEN")
if not token:
    raise ValueError("DISCORD_TOKEN not set!")
bot.run(token)