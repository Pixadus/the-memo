import dotenv, asyncio, aiohttp, os
from discord.ext import commands

dotenv.load_dotenv()

# In .env, put BOT_TOKEN="<memobot bot token>"
TOKEN = os.getenv("BOT_TOKEN")

BOT_PREFIX = ("~")
client = commands.Bot(command_prefix=BOT_PREFIX)

@client.event
async def on_ready():
    print("Logged in as " + client.user.name)

@client.command(pass_context=True)
async def test(context): #~test
    await context.send("test")
async def pull(context): #~pull
    await context.send("not yet implemented") #TODO: Add stuff from news aggregator i can't spell

client.run(TOKEN)
