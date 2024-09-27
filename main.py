import discord
import os
from dotenv import load_dotenv
import asyncio
from discord.ext import commands, tasks
import settings
import subprocess
import threading
import colorama

logger = settings.logging.getLogger("bot")


intents = discord.Intents.all()  # default does not allow the functions i need lol
intents.message_content = True
intents.members = True


load_dotenv(".env")
TOKEN: str = os.getenv("TOKEN")

bot = commands.Bot(
    command_prefix="!", intents=intents
)  # TODO Initialise for hybrid commands later TBD


@bot.event
async def on_ready():
    # This isnt needed but it looks cool so im keeping it :)
    print(
        f"""{colorama.Fore.BLUE}

██████╗  ██████╗ ███╗   ██╗██╗  ██╗██████╗  ██████╗ ████████╗
██╔══██╗██╔═══██╗████╗  ██║██║ ██╔╝██╔══██╗██╔═══██╗╚══██╔══╝
██████╔╝██║   ██║██╔██╗ ██║█████╔╝ ██████╔╝██║   ██║   ██║   
██╔══██╗██║   ██║██║╚██╗██║██╔═██╗ ██╔══██╗██║   ██║   ██║   
██████╔╝╚██████╔╝██║ ╚████║██║  ██╗██████╔╝╚██████╔╝   ██║   
╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═════╝  ╚═════╝    ╚═╝  
{colorama.Fore.RESET}\n"""  # Actuall beginning for bot synchronisation and initialisation
    )
    logger.info(f"User: {bot.user} (ID: {bot.user.id})")
    try:
        synced_commands = await bot.tree.sync()
        logger.info(f"Successfully Synced {len(synced_commands)} Commands.")
    except Exception as e:
        logger.error("Error syncing App commands has occurred: ", exc_info=e)


def run_logger():
    subprocess.run(["python", "discordchatlogger.py"])


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


# Magic. Do not touch.
async def main():
    async with bot:
        await load()
        await bot.start(TOKEN)


if __name__ == "__main__":
    logger_thread = threading.Thread(target=run_logger)
    logger_thread.start()


asyncio.run(main())
