import discord
import os
from dotenv import load_dotenv
import asyncio
from discord.ext import commands, tasks
import settings
import subprocess
import threading

logger = settings.logging.getLogger("bot")

#defining the intents the bot will use
intents = discord.Intents.all() #default does not allow the functions i needed lol
intents.message_content = True 
intents.members = True


load_dotenv(".env")
TOKEN: str = os.getenv("TOKEN")

bot = commands.Bot(command_prefix='!', intents=intents) #Initialise for hybrid commands  TBD

# event trigger
@bot.event
async def on_ready():
    #await bot.change_presence(status=discord.Status.do_not_disturb) REDUNDANT
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

async def main():
    async with bot:
        await load()
        await bot.start(TOKEN)
        
if __name__ == "__main__":
    logger_thread = threading.Thread(target=run_logger)
    logger_thread.start()

#run
asyncio.run(main())