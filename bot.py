importer discorde
à partir des commandes d'importation discord.ext
importation os

# Créer le bot avec les intentions nécessaires
intentions = discorde.Intents.default()
intentions.message_content = Vrai

bot = commandes.Bot (command_prefix="/", intents=intents)

@bot.événement
async def on_ready():
    imprimer(f'{bot.user} est connecté !')
    essayer:
        synchronisé = attendre bot.tree.sync()
        print (f « Synchronisé {len (synchronisé)} réquisition (s) »)
    sauf exception comme e :
        imprimer(e)

# Corde barre oblique : /ping
@bot.tree.command(name="ping", description="Affiche la latence du bot")
async def ping (interaction : discord.Interaction) :
    latence = bot.latence * 1000
    attendez interaction.response.send_message(f"Pong! 🏓 Latence: {latence:.2f}ms")

# Commande slash : /bonjour
@bot.tree.command(name="hello", description="Salue l'utilisateur")
async def hello(interaction : discord.Interaction) :
    attendez interaction.response.send_message(f"Salut {interaction.user.mention} ! 👋")

# Corde barre oblique : /info
@bot.tree.command(name="info", description="Affiche les infos du service")
async def info (interaction : discord.Interaction) :
    guilde = interaction.guild
    intégrer = discorde. Intégré (
        titre=f"Infos de {guild.name}",
        couleur=discord.Color.blue()
    )
    embed.add_field(name="Membres", value=guild.member_count, inline=False)
    embed.add_field(name="Créé le", value=guild.created_at.strftime(« %d/%m/%Y »), inline=False)
    attendre interaction.response.send_message(embed=embed)

# Corde slash : /utilisateur
@bot.tree.command(name="user", description="Affiche les infos d'un utilisateur")
async def user (interaction : discord.Interaction, membre : discord.User = None) :
    si le membre est Aucun :
        membre = interaction.utilisateur
    
    intégrer = discorde. Intégré (
        titre=f"Infos de {member.name}",
        couleur=discord.Color.green()
    )
    embed.set_thumbnail(url=member.avatar.url si member.avatar else None)
    embed.add_field(name="ID", value=member.id, inline=False)
    embed.add_field(nom="Créé le", value=member.created_at.strftime(« %d/%m/%Y »), inline=Faux)
    attendre interaction.response.send_message(embed=embed)

# Lancer le bot
jeton = os.getenv(« DISCORD_TOKEN »)
si ce n'est pas un jeton :
    augmenter la valeurError(« DISCORD_TOKEN non défini ! »)

bot.run (jeton)