# This code is based on the following example:
# https://discordpy.readthedocs.io/en/stable/quickstart.html#a-minimal-bot

import os
import asyncio
from requests import get

import discord
import random
from discord.ext import commands
from dotenv import load_env
from keep_alive import keep_alive

load_env()

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.guild_reactions = True

emojis = ["<:java:1238884814728462386>", "<:bedrock:1238884916230488215>", "<:roblox:1238885038175686688>"]
message_id = None

JOKE_URL = "https://icanhazdadjoke.com/"
HEADERS = {
    "Accept": "application/json",
    "User-Agent": "No Website pocketmonsterlogin@gmail.com"
}

client = commands.Bot(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#Custom join message
@client.event
async def on_member_join(member):
    # Define the channel where you want the bot to send the greeting message
    channel = member.guild.system_channel
    
    # Check if the channel exists and the bot has permission to send messages
    if channel is not None and channel.permissions_for(member.guild.me).send_messages:
        # Customize the greeting message
        print("Sending message")
        greeting_message = f"Welcome to Good Ol' Kinda Vanilla, {member.mention}! We're glad you joined us!"
        
        # Send the greeting message
        await channel.send(greeting_message)


@client.event
async def on_reaction_add(reaction, user):
    global message_id
    
    if user == client.user:
        return

    
    message = reaction.message
    guild = message.guild
    member = guild.get_member(user.id)
    print("Checking the message and reaction")
    # Check if the reaction is on a specific message and from a specific emoji
    if message.id == message_id and str(reaction.emoji) == emojis[2]:
        role = discord.utils.get(guild.roles, name="Roblox")
        if role:
            await member.add_roles(role)
            await member.send(f"You have been given the role, {role.name}, in {guild.name}")
            print("Role added")
        else:
            print(f"Role not found {role.name}")
    elif message.id == message_id and str(reaction.emoji) == emojis[1]:
        role = discord.utils.get(guild.roles, name="Bedrock Edition")
        if role:
            await member.add_roles(role)
            await member.send(f"You have been given the role, {role.name}, in {guild.name}")
            print("Role added")
        else:
            print(f"Role not found {role.name}")
    elif message.id == message_id and str(reaction.emoji) == emojis[0]:
        role = discord.utils.get(guild.roles, name="Java Edition")
        if role:
            await member.add_roles(role)
            await member.send(f"You have been given the role, {role.name}, in {guild.name}")
            print("Role added")
        else:
            print(f"Role not found {role.name}")
    else:
        print(str(reaction.emoji) + " " + str(message_id))

@client.event
async def on_reaction_remove(reaction, user):
    global message_id
    
    if user == client.user:
        return
    message = reaction.message
    guild = message.guild
    member = guild.get_member(user.id)
    print("Checking the message and reaction")
    
    if message.id == message_id and str(reaction.emoji) == emojis[2]:
        role = discord.utils.get(guild.roles, name="Roblox Edition")
        if role:
            await member.remove_roles(role)
            await member.send(f"Your role, {role.name}, has been removed in {guild.name}")
            print("Role removed")
        else:
            print(f"Role not found {role.name}")
    elif message.id == message_id and str(reaction.emoji) == emojis[1]:
        role = discord.utils.get(guild.roles, name="Bedrock Edition")
        if role:
            await member.remove_roles(role)
            await member.send(f"Your role, {role.name}, has been removed in {guild.name}")
            print("Role removed")
        else:
            print(f"Role not found {role.name}")
    elif message.id == message_id and str(reaction.emoji) == emojis[0]:
        role = discord.utils.get(guild.roles, name="Java Edition")
        if role:
            await member.remove_roles(role)
            await member.send(f"Your role, {role.name}, has been removed in {guild.name}")
            print("Role removed")
        else:
            print(f"Role not found {role.name}")
    else:
        print(str(reaction.emoji) + " " + str(message_id))

#Sends ip of the server
@client.command()
async def ip(ctx):
    # Send a response when the !ip command is invoked
    embed = discord.Embed(
        title="**General Info**",
        description=f"**Server Info**\nThe server IP is: try-demonstrate.gl.joinmc.link\nThe version is 1.20.4\nThe server restarts everyday at 12 AM EST and every 3 days will shut down at 8 PM EST to backup the server\nYou don't need any modpack to play on the server, though client-side mods are nice but I would recommend you to enable resource packs on the server for some of the custom items from some mods.\n\n**Donating**\nIf you feel as if you want to donate to help pay for the server, then you can do that using the server's new [Patreon page](https://www.patreon.com/kindavanilla/about)\n\n**Map**\nYou can view a map of the server thanks to the mod squaremap, though it updates a little slow so it looks like dots on the screen for areas that people travel through quick. [Click here](http://rentals-union.gl.at.ply.gg:18847) to view the map!\n\n**Bot Commands**\nYou can use all of these inside of the bot-commands channel\n!guess will start a guessing game between 1 and 100 | !joke will give you a neat dad joke thanks to the [icanhazdadjoke API](https://icanhazdadjoke.com)",
        color=discord.Color(0x0C730F)
    )
    await ctx.send(embed=embed)

@client.command()
@commands.is_owner()
async def shutdown(ctx):
	client.close()
    
#Guessing game
@client.command()
async def guess(ctx):
    # Create a new text channel for the private thread
    guild = ctx.guild
    author = ctx.author
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        author: discord.PermissionOverwrite(read_messages=True),
        ctx.guild.me: discord.PermissionOverwrite(read_messages=True)
    }
    # Find the "text channels" category
    category = discord.utils.get(guild.categories, name="Text Channels")
    guessnumber = random.randint(0,10000)
    
    # Create the channel within the category
    channel = await guild.create_text_channel(f'{author.name}-guess{guessnumber}', overwrites=overwrites, category=category)

    # Send a message to the user in the new private thread
    await channel.send(f'Welcome to the guessing game, {author.mention}! Please guess a number between 1 and 100.')

    def check(message):
        return message.author == author and message.channel == channel

    
    randomNumber = random.randint(0,100)
    while True:
        try:
            msg = await client.wait_for('message', check=check, timeout=60.0)
            try:
                if msg.content:
                    guess = int(msg.content)
                    if guess < 1 or guess > 100:
                        await channel.send('Please enter a number between 1 and 100.')
                    else:
                        if randomNumber == guess:
                            await channel.send(f'Congratulations, {author.mention}! You guessed the correct number')
                            await channel.delete()
                            break
                        elif randomNumber < guess:
                            await channel.send("The number is lower than your guess")
                        elif randomNumber > guess:
                            await channel.send("The number is higher than your guess")
                else:
                    await channel.send(f'You guessed: {msg.content}')
            except asyncio.TimeoutError:
                await channel.delete()
        except ValueError:
            await channel.send('Please enter a valid number.')

@client.command()
async def joke(ctx):
    r = get(JOKE_URL, headers=HEADERS)
    data = {}
    data = r.json()
    if r.status_code == 200:
        if "?" in data["joke"]:
            joke = data["joke"].replace("? ", "?\n")
            joke = joke.split("\n")
            print(joke)
            await ctx.channel.send(f"{joke[0]}\n||{joke[1]}||")
        else:
            await ctx.channel.send(data["joke"])

@client.command()
async def roles_list(ctx):
    global message_id
    roles = ctx.author.roles
    if roles:
        role_names = [role.name for role in roles]
        if "Owner" in role_names:
            message = await ctx.send("Please react to the bot's message for the role that you want\n\nEach role gives you access to the channels that people who play those games can talk about them\n\n**Java: This role means you play Minecraft Java**\n\n**Bedrock: This role means you play Minecraft Bedrock**\n\n**Roblox: This role means you play Roblox**")
            message_id = message.id
            for role in emojis:
                await message.add_reaction(role)
            
        
try:
  token = os.getenv("TOKEN") or ""
  if token == "":
    raise Exception("Please add your token to the Secrets pane.")
  client.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print(
            "The Discord servers denied the connection for making too many requests"
        )
        print(
            "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
        )
    else:
        raise e
