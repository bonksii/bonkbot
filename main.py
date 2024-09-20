import discord
import os
from dotenv import load_dotenv
import asyncio
from discord.ext import commands, tasks
from itertools import cycle
from discord import app_commands

#import logging
#import logging.handlers

#defines the intents the bot will use
intents = discord.Intents.all()
intents.message_content = True #enables access to message content
intents.members = True


load_dotenv(".env")
TOKEN: str = os.getenv("TOKEN")

bot = commands.Bot(command_prefix='!', intents=intents)

# event trigger
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.do_not_disturb)
    print("The Bot is ready for usage")
    print("--------------------------")
    bot.loop.create_task(change_status())
    try:
        synced_commands = await bot.tree.sync()
        print(f"Synced {len(synced_commands)} commands.")
    except Exception as e:
        print("An error with syncing application commands has occured: ", e)

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

activities = [
    discord.Game("bonksii.com"),
    discord.Game("bonk.io"),
    discord.Activity(type=discord.ActivityType.listening, name="PinkPantheress"),
    discord.Activity(type=discord.ActivityType.watching, name="bonksii on Youtube")
]

# Bot status cycler
async def change_status():
    await bot.wait_until_ready()
    while not bot.is_closed():
        for activity in activities:
            await bot.change_presence(activity=activity)
            await asyncio.sleep(120)

async def main():
    async with bot:
        await load()
        await bot.start(TOKEN)

# Grab token id from the environment field 
asyncio.run(main())