# Importation des modules nécessaires
import os
import discord
from discord.ext import commands
import config
import time
import asyncio


int_to_emoji = {
    0: "😀",
    1: "😁",
    2: "😂",
    3: "🤣",
    4: "😃",
    5: "😄",
    6: "😅",
    7: "😆",
    8: "😉",
    9: "😊",
    10: "😋",
    11: "😎",
    12: "😍",
    13: "😘",
    14: "🥰",
    15: "😗",
    16: "😙",
    17: "😚",
    18: "🙂",
    19: "🤗",
    20: "🤩",
    21: "🤔",
    22: "🤨",
    23: "😐",
    24: "😑",
    25: "😶",
    26: "🙄",
    27: "😏",
    28: "😣",
    29: "😥",
    30: "😮",
    31: "🤐",
    32: "😯",
    33: "😪",
    34: "😫",
    35: "🥱",
    36: "😴",
    37: "😌",
    38: "😛",
    39: "😜",
    40: "😝",
    41: "🤤",
    42: "😒",
    43: "😓",
    44: "😔",
    45: "😕",
    46: "🙃",
    47: "🤑",
    48: "😲",
    49: "☹️",
    50: "🙁",
    51: "😖",
    52: "😞",
    53: "😟",
    54: "😤",
    55: "😢",
    56: "😭",
    57: "😦",
    58: "😧",
    59: "😨",
    60: "😩",
    61: "🤯",
    62: "😬",
    63: "😰",
    64: "😱",
    65: "🥵",
    66: "🥶",
    67: "😳",
    68: "🤪",
    69: "😵",
    70: "🥴",
    71: "😠",
    72: "😡",
    73: "🤬",
    74: "🤢",
    75: "🤮",
    76: "🤧",
    77: "😇",
    78: "🥳",
    79: "🥺",
    80: "🤠",
    81: "🥸",
    82: "🤡",
    83: "🤥",
    84: "🤫",
    85: "🤭",
    86: "🧐",
    87: "🤓",
    88: "😈",
    89: "👿",
    90: "👹",
    91: "👺",
    92: "💀",
    93: "☠️",
    94: "👻",
    95: "👽",
    96: "👾",
    97: "🤖",
    98: "😺",
    99: "😸",
    100: "😹"
}



# Récupération du TOKEN depuis config.py
TOKEN = config.TOKEN

# Création de l'instance du bot avec un préfixe de commande
intents = discord.Intents.default()
intents.messages = True
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!',intents=intents)


Maison = {}
Liste_emplacements = {}
Liste_item = {}

# Définition de l'événement on_ready
@bot.event
async def on_ready():
    print("Le Bot est prêt !")
    fichier_maison = open("maison.csv", "r")
    fichier_emplacement = open("emplacement.csv", "r")
    fichier_item = open("object.csv", "r")
    
    for ligne in fichier_maison:
        nom_piece, description, couleur = ligne.strip().split(",")
        piece = Piece(nom_piece, description, couleur)
        Maison[piece.name] = piece
        
    for ligne in fichier_emplacement:
        name, description, piece = ligne.strip().split(",")
        emplacement = Emplacement(name, description, piece)
        Liste_emplacements[emplacement.name] = emplacement
        
    for ligne in fichier_item:
        name, description, gen_code, number, CC, color, price, date = ligne.strip().split(",")
        item = Item(name, description, gen_code, number, CC, color, price, date)
        Liste_item[item.name] = item
    

# Création des classes
class Piece:
    def __init__(self, name, description, color="black"):
        self.name = name
        self.description = description
        self.emplacement = []
        self.color = color
        self.image = ''
        
    def add_emplacement(self, emplacement):
        self.emplacement.append(emplacement)
        emplacement.set_piece(self.name)
        
    async def see_piece(self, ctx):
        embed = discord.Embed(title="Emplacement de la Pièce", description=self.name, color=self.color)
        for empl in self.emplacement:
            value = ""
            for it in empl.item:
                value += it.name + "\n"
            embed.add_field(name=empl.name, value=value)
        await ctx.send(embed=embed)
    
    def remove_emplacement(self, emplacement):
        self.emplacement.remove(emplacement)
        emplacement.set_piece("")
        
    def rename_piece(self, name):
        self.name = name
        for empl in self.emplacement:
            empl.set_piece(name)
        
    def rename_piece_description(self, description):
        self.description = description
        
    def rename_piece_color(self, color):
        self.color = color
        
    def add_image(self, image):
        self.image = image
        
class Emplacement:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.piece = ''
        self.item = []
        
    def set_piece(self, piece):
        self.piece = piece
        
    def rename_emplacement(self, name):
        self.name = name
        for item in self.item:
            item.set_emplacement(name)
        
    def rename_emplacement_description(self, description):
        self.description = description
        
    def add_item(self, item):
        self.item.append(item)
        
    def remove_item(self, item):
        self.item.remove(item)
        item.set_emplacement("")
        
    async def see_emplacement(self, ctx):
        embed = discord.Embed(title="Emplacement", description=self.name, color=0x00ff00)
        value = ""
        for item in self.item:
            value += item.name + "\n"
        embed.add_field(name="Contenu", value=value)
        await ctx.send(embed=embed)
    
class Item:
    def __init__(self, name, description="", gen_code="", number='1', CC="", color='', price='', date=""):
        self.name = name
        self.description = description
        self.gen_code = gen_code
        self.number = number
        self.CC = CC
        self.color = color
        self.price = price
        self.date = date
        self.emplacement = ""
        
    def set_emplacement(self, emplacement):
        self.emplacement = emplacement
        emplacement.add_item(self)
        
    def rename_item(self, name):
        self.name = name
    
    def rename_item_description(self, description):
        self.description = description
        
    def add_gen_code(self, gen_code):
        self.gen_code = gen_code
        
    def edit_number(self, number):
        self.number = number
        
    def add_CC(self, CC):
        self.CC = CC
        
    def add_price(self, price):
        self.price = price
        
    def add_date(self, date):
        self.date = date
        
    async def see_item(self, ctx):
        embed = discord.Embed(title="Item", description=self.name)
        if self.description:
            embed.add_field(name="Description", value=self.description)
        if self.gen_code:
            embed.add_field(name="Code Barre", value=self.gen_code)
        embed.add_field(name="Nombre", value=self.number)
        if self.CC:
            embed.add_field(name="CC", value=self.CC)
        if self.color:
            embed.add_field(name="Couleur", value=self.color)
        if self.price:
            embed.add_field(name="Prix", value=self.price)
        if self.date:
            embed.add_field(name="Date d'achat", value=self.date)
        await ctx.send(embed=embed)

# Commandes Discord

@bot.command()
async def stop(ctx):
    print("Arrêt du bot")
    await bot.close()
    print("Bot stoppé")
    
# Commande concernant les pièces
    
@bot.command()
async def create_piece(ctx, name, color, description):
    try:
        name = str(name)
        color = str(color)
        description = str(description)
    except ValueError:
        embed = discord.Embed(title="Erreur", description="Veuillez renseigner des informations valides.")
        color = discord.Colour.red()
        embed.color = color
        await ctx.send(embed=embed)
        return
    
    if name not in [Maison[piece].name for piece in Maison]:
        #envoie de l'embed
        embed = discord.Embed(title="Création d'une Pièce")
        embed.add_field(name="Nom", value=name)
        embed.add_field(name="Description", value=description)
        embed.add_field(name="Couleur", value=color)
        try:
            embed_color = discord.Colour(int(color.lstrip('#'), 16))
        except TypeError:
            embed_color = discord.Colour.green()
        embed.color = embed_color
        await ctx.send(embed=embed)
        
        #Modification du fichier csv
        piece = Piece(name, description, color)
        Maison[piece.name] = piece
        fichier = open("maison.csv", "a")
        fichier.write(f"{name},{description},{color}\n")
        
        #Création de la catégorie
        guild = ctx.message.guild
        await ctx.guild.create_category(name)
        
        
    else:
        embed = discord.Embed(title="Erreur", description="Une pièce portant ce nom existe déjà.")
        color = discord.Colour.red()
        embed.color = color
        await ctx.send(embed=embed)

@bot.command()        
async def remove_piece(ctx, name):
    if name in [Maison[piece].name for piece in Maison]:
        embed = discord.Embed(title="Suppression d'une Pièce", description="Voulez-vous vraiment supprimer la pièce : " + name)
        color = discord.Colour.red()
        embed.color = color
        message = await ctx.send(embed=embed)
        
        def check(reaction, user):
            return user == ctx.author 
            
        await message.add_reaction("\u2714")
        await message.add_reaction("\u274C")
        
        
        try: 
            reaction = await bot.wait_for("reaction_add", check=check, timeout = 30)
            if reaction[0].emoji == "\u2714":
                embed = discord.Embed(title="Suppression d'une Pièce", description="La pièce " + name + " a été supprimée avec succès.")
                embed.color = discord.Colour.green()
                await message.edit(embed=embed)
                
                # Suppression des emplacements de la pièce
                piece = [piece for piece in Maison if piece.name == name][0]
                #Suppression de la pièce dans le fichier csv
                with open("maison.csv", "r") as file:
                    lines = file.readlines()
                with open("maison.csv", "w") as file:
                    for line in lines:
                        if line.strip().split(",")[0]!= name:
                            file.write(line)
                
                #Suppression de la pièce dans la liste
                Maison.remove(piece)
                
                #Suppression de la catégorie
                guild = ctx.message.guild
                category = discord.utils.get(guild.categories, name=name)
                await category.delete()
                
            else:
                embed = discord.Embed(title="Suppression d'une Pièce", description="La suppression de la pièce " + name + " a été annulée.")
                embed.color = discord.Colour.red()
                await message.edit(embed=embed)
                
                
        except asyncio.TimeoutError:
            embed = discord.Embed(title="Suppression d'une Pièce", description="La suppression de la pièce " + name + " a été annulée car vous n'avez pas réagis.")
            embed.color = discord.Colour.red()
            await message.edit(embed=embed)
            
            
        
                
                
            
            
            

    else:
        embed = discord.Embed(title="Erreur", description="Une pièce portant ce nom n'existe pas.")
        color = discord.Colour.red()
        embed.color = color
        await ctx.send(embed=embed)
        
        
@bot.command()
async def rename_piece(ctx, name, new_name):
    if name in [piece.name for piece in Maison]:
        embed = discord.Embed(title="Renommage d'une Pièce", description=f"La pièce {name} va être renommée en {new_name}.")
        embed.color = discord.Colour.gold()
        embed = await ctx.send(embed=embed)
        
        # Modification du nom dans le fichier csv
        with open("maison.csv", "r") as file:
            lines = file.readlines()
        with open("maison.csv", "w") as file:
            for line in lines:
                if line.strip().split(",")[0] == name:
                    file.write(f"{new_name},{line.strip().split(',')[1]},{line.strip().split(',')[2]}\n")
                else:
                    file.write(line)
        
        # Modification du nom dans la liste
        piece = [piece for piece in Maison if piece.name == name][0]
        piece.name = new_name
        
        # Modification du nom dans la catégorie
        guild = ctx.message.guild
        category = discord.utils.get(guild.categories, name=name)
        await category.edit(name=new_name)
        
    else:
        embed = discord.Embed(title="Erreur", description="Une pièce portant ce nom n'existe pas.")
        color = discord.Colour.red()
        embed.color = color
        await ctx.send(embed=embed)
        
        
        
# Commande concernant les emplacements

@bot.command()
async def create_emplacement(ctx, name, description):
    if name not in [emplacement.name for emplacement in Liste_emplacements]:
        #envoie de l'embed
        embed = discord.Embed(title="Création d'un Emplacement")
        embed.add_field(name="Nom", value=name)
        embed.add_field(name="Description", value=description)
        embed.color = discord.Colour.green()
        
        value = []
        c=0
        d_c = {}
        for piece in Maison:
            if c < 10:
                unicode = str(c) + "\u20e3"
            else: 
                unicode = int_to_emoji[c-10]
            c+=1
            value.append(unicode+str(Maison[piece].name))
            d_c[unicode] = Maison[piece].name
        embed.add_field(name="Piece", value="Choisier la pièce dans laquelle se trouve l'emplacement. \n"+'\n'.join(value))
        message = await ctx.send(embed=embed)
        
        
        for c in range(len(Maison)):
            if c < 10:
                unicode = str(c) + "\u20e3"
                
            else: 
                unicode = int_to_emoji[c-10]
            await message.add_reaction(unicode)
        
        
        def check(reaction, user):
            return user == ctx.author
        
        try:
            reaction = await bot.wait_for('reaction_add', check=check,timeout=30)
            piece = d_c[reaction[0].emoji]
            
        except asyncio.TimeoutError:
            embed = discord.Embed(title="Création d'un Emplacement", description="Création de l'emplacement annulée car vous n'avez pas réagis.")
            embed.color = discord.Colour.red()
            await message.edit(embed=embed)
            return
            
        #Modification du fichier csv
        emplacement = (name, description, piece)
        print(piece, "--------------------")
        Liste_emplacements[name] =  emplacement
        open("emplacement.csv", "a").write(f"{name},{description},{piece}\n")

# Démarrage du bot
bot.run(TOKEN)
