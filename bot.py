# bot.py - God++ Ultimate 2.0

import discord
from discord.ext import commands
from datetime import datetime, timedelta
import os
import requests

# ---------------- TOKENS ----------------
TOKEN = os.getenv("DISCORD_TOKEN")  # Discord
API_TOKEN = os.getenv("API_TOKEN")   # OpenAI ou autre API

# ---------------- INTENTS ----------------
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

# ---------------- EVENT : READY ----------------
@bot.event
async def on_ready():
    print(f"God++ Ultimate 2.0 connecté en tant que {bot.user}")

# ---------------- COMMANDES PERSONNELLES ----------------
@bot.command()
async def ping(ctx):
    await ctx.send("Pong ! ✅")

@bot.command()
async def dire(ctx, *, texte):
    await ctx.send(texte)

@bot.command()
async def salut(ctx):
    await ctx.send(f"Salut {ctx.author.mention} ! 👋")

@bot.command()
async def info(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    embed = discord.Embed(title=f"Info sur {member.name}", color=discord.Color.blue())
    embed.add_field(name="ID", value=member.id, inline=False)
    embed.add_field(name="Pseudo", value=member.display_name, inline=False)
    embed.add_field(name="Bot ?", value=member.bot, inline=False)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else "")
    await ctx.send(embed=embed)

@bot.command()
async def grade(ctx, member: discord.Member):
    roles = [role.name for role in member.roles if role.name != "@everyone"]
    await ctx.send(f"{member.mention} a les rôles : {', '.join(roles) if roles else 'Aucun'}")

@bot.command()
async def clear(ctx, nombre: int):
    await ctx.channel.purge(limit=nombre)
    await ctx.send(f"{nombre} messages supprimés.", delete_after=5)

# ---------------- COMMANDES IA ----------------
@bot.command()
async def ia(ctx, *, question):
    headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
    data = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": question}],
        "max_tokens": 200
    }
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)
        result = response.json()
        answer = result['choices'][0]['message']['content']
        await ctx.send(answer)
    except Exception as e:
        await ctx.send(f"Erreur IA: {e}")

# ---------------- COMMANDES AUDIT ----------------
@bot.command()
async def audit(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"Audit complet : {guild.name}", color=discord.Color.green())
    
    # Roles
    roles_info = "\n".join([f"{role.name} (ID:{role.id})" for role in guild.roles])
    embed.add_field(name=f"Rôles ({len(guild.roles)})", value=roles_info or "Aucun", inline=False)
    
    # Salons
    channels_info = "\n".join([f"{ch.name} ({str(ch.type)})" for ch in guild.channels])
    embed.add_field(name=f"Salons ({len(guild.channels)})", value=channels_info or "Aucun", inline=False)
    
    # Membres
    members_info = "\n".join([f"{m.name}#{m.discriminator} - {', '.join([r.name for r in m.roles if r.name != '@everyone'])}" for m in guild.members])
    if len(members_info) > 1000:
        members_info = members_info[:1000] + "\n[Liste tronquée]"
    embed.add_field(name=f"Membres ({len(guild.members)})", value=members_info or "Aucun", inline=False)
    
    await ctx.send(embed=embed)

@bot.command()
async def permcheck(ctx, member: discord.Member):
    perms = member.guild_permissions
    perm_list = [perm.replace("_"," ").title() for perm,value in perms if value]
    await ctx.send(f"Permissions de {member.mention} : {', '.join(perm_list) if perm_list else 'Aucune'}")

@bot.command()
async def inactive(ctx, jours: int = 30):
    guild = ctx.guild
    cutoff = datetime.utcnow() - timedelta(days=jours)
    inactive_members = []
    for member in guild.members:
        if member.bot:
            continue
        last_msg = None
        for channel in guild.text_channels:
            try:
                async for msg in channel.history(limit=100):
                    if msg.author == member:
                        last_msg = msg.created_at
                        break
            except:
                continue
        if not last_msg or last_msg < cutoff:
            inactive_members.append(f"{member.name} ({last_msg.strftime('%Y-%m-%d') if last_msg else 'Jamais'})")
    await ctx.send(f"Membres inactifs depuis {jours} jours ({len(inactive_members)}):\n" + (", ".join(inactive_members) if inactive_members else "Aucun"))

@bot.command()
async def messagecount(ctx):
    guild = ctx.guild
    msg_counts = {}
    for ch in guild.text_channels:
        count = 0
        try:
            async for _ in ch.history(limit=100):
                count += 1
        except:
            continue
        msg_counts[ch.name] = count
    msg_summary = "\n".join([f"{name}: {count}" for name,count in msg_counts.items()])
    await ctx.send(f"📨 Messages par salon (100 derniers) :\n{msg_summary}")

# ---------------- COMMANDES PANEL ----------------
@bot.command()
async def panel(ctx, titre: str, description: str, couleur: str = "blue", footer: str = None):
    try:
        couleur_embed = getattr(discord.Color, couleur.lower(), discord.Color.blue())
        embed = discord.Embed(title=titre, description=description, color=couleur_embed)
        if footer:
            embed.set_footer(text=footer)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"Erreur lors de la création du panel: {e}")

@bot.command()
async def panelia(ctx, *, description):
    headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
    data = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": f"Crée un panel Discord embed pour : {description}"}],
        "max_tokens": 250
    }
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)
        result = response.json()
        embed_data = result['choices'][0]['message']['content']
        embed = discord.Embed(title="Panel IA", description=embed_data, color=discord.Color.blue())
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"Erreur IA panel: {e}")

# ---------------- COMMANDES CLEARALL ----------------
@bot.command()
async def clearall(ctx):
    try:
        await ctx.channel.purge(limit=None)
        await ctx.send("✅ Tous les messages du salon ont été supprimés.", delete_after=5)
    except Exception as e:
        await ctx.send(f"Erreur lors de la suppression : {e}")

# ---------------- LANCEMENT DU BOT ----------------
bot.run(TOKEN)