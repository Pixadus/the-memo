# Needed for basic bot function
import dotenv, asyncio, aiohttp, os
from discord.ext import commands

# Actual usable stuffs
import requests
from random import randint

# NewsAPI Endpoint URL
NEWSAPI_URL = "https://newsapi.org/v2/"

dotenv.load_dotenv()
# In .env, put BOT_TOKEN="<memobot bot token>"
TOKEN = os.getenv("BOT_TOKEN")
# In .env, put NEWSAPI_TOKEN="<token>"
NEWSAPI_TOKEN = os.getenv("NEWSAPI_TOKEN")
AUTH_HEAD = {"Authorization": "Bearer "+NEWSAPI_TOKEN}

BOT_PREFIX = ("~")
client = commands.Bot(command_prefix=BOT_PREFIX)

@client.event
async def on_ready():
    print("Logged in as " + client.user.name)

@client.command(pass_context=True, name="test")
async def test(context): #~test
    endpoint = NEWSAPI_URL+"top-headlines?" + "country=us"
    res = requests.get(endpoint, headers=AUTH_HEAD)
    res = str(res.json())[0:1000]
    await context.send(res)

@client.command(pass_context=True, name="pull", help="Updates news from sources and cache it")
async def pull(context): #~pull
    await context.send("not yet implemented") #TODO: Add stuff from news aggregator i can't spell


@client.command(pass_context=True, name="top", help="Looks for the top headlines and lists them. Takes optional parameter <country>, defaults to \"us\"")
async def top(context, country="us"):
    if len(country) != 2:
        await context.send("[error country_code_bad_length]")
    endpoint = NEWSAPI_URL+"top-headlines?" + "country=" + country
    res = requests.get(endpoint, headers=AUTH_HEAD)
    res = str(res.json())[0:1000]
    await context.send(res)


@client.command(pass_context=True, name='roll', help='Simulates rolling dice.')
async def roll(context, dice=None): #~roll
    if dice is None:
        await context.send("No dice specified")
        return None
    #else:
    #    await context.send("raw: `"+dice+"`")
    #    pass
    res = []
    dice = dice.split()
    for die in dice:
        if die.isdigit():
            res.append(random.randint(1, int(die)))
        elif "d" in die:
            die = die.split("d")
            if len(die) == 2 and die[0] == "" and die[1].isdigit():
                res.append(random.randint(1, int(die[1])))
            elif len(die) == 2 and die[0].isdigit() and die[1].isdigit():
                for i in range(0, int(die[0])):
                    res.append(random.randint(1, int(die[1])))
            else:
                res.append("[error bad_format_single]")
        else:
            res.append("[error bad_format_total]")
    # Because I'm a lazy shit
    total = 0
    for die in res:
        total += die
    for i in range(len(res)):
        res[i] = str(res[i])
    await context.send(", ".join(res) + " (Total: "+str(total)+")")

client.run(TOKEN)
