import discord
import os
from discord.ext import commands
#define the intents ythe bot will use
intents = discord.Intents.default()
intents.message_content = True #enables access to message content



from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()


#import Bot Tokens
from apikeys import *
client = commands.Bot(command_prefix = '/', intents=intents)

#event triggered when bot is ready to start working
@client.event
async def on_ready():
    print("The Bot is ready for usage")
    print("--------------------------")

#command triggered to test if bots working 
@client.command()
async def hello(ctx):
   await ctx.send("Hello i am basic bot")



#Trigger goodbye message if a user uses the goodbye command
@client.command()
async def goodbye(ctx):
   await ctx.send(f"bye bye {ctx.author.mention}")

client.run(os.getenv('TOKEN'))