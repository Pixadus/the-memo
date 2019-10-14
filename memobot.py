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
async def test(context):
    await context.send("test")

client.run(TOKEN)
