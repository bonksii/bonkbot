import discord
import os
from dotenv import load_dotenv
import asyncio
from discord.ext import commands
import subprocess
import threading
import colorama
import signal
from discordchatlogger import connect_to_discord
import cogs.settings as settings

logger = settings.logging.getLogger("bot")

intents = discord.Intents.all()
intents.message_content = True
intents.members = True

load_dotenv(".env")
TOKEN: str = os.getenv("TOKEN")

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"""{colorama.Fore.BLUE}
    ██████╗  ██████╗ ███╗   ██╗██╗  ██╗██████╗  ██████╗ ████████╗
    ██╔══██╗██╔═══██╗████╗  ██║██║ ██╔╝██╔══██╗██╔═══██╗╚══██╔══╝
    ██████╔╝██║   ██║██╔██╗ ██║█████╔╝ ██████╔╝██║   ██║   ██║   
    ██╔══██╗██║   ██║██║╚██╗██║██╔═██╗ ██╔══██╗██║   ██║   ██║   
    ██████╔╝╚██████╔╝██║ ╚████║██║  ██╗██████╔╝╚██████╔╝   ██║   
    ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═════╝  ╚═════╝    ╚═╝  
          {colorama.Fore.RESET}\n""")

    logger.info(f"User: {bot.user} (ID: {bot.user.id})")
    try:
        synced_commands = await bot.tree.sync()
        logger.info(f"Successfully Synced {len(synced_commands)} Commands.")
    except Exception as e:
        logger.error("Error syncing App commands has occurred: ", exc_info=e)

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
    await bot.load_extension('jishaku')

def start_logger():  
    connect_to_discord()

# Magic. Do not touch.
async def main():
    async with bot:
        await load()
        logger_thread = threading.Thread(target=connect_to_discord, daemon=True)
        logger_thread.start()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
