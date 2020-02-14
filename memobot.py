# Needed for basic bot function
import dotenv, asyncio, aiohttp, os
from discord.ext import commands
from discord import Embed

# Actual usable stuffs
import requests
import random

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
async def top(context, country="us", page="1"):
    if country is None or len(country) != 2:
        await context.send("[error country_code_bad_length]")
        return None
    if page is None or not page.isdigit():
        await context.send("[error bad_page_num]")
        return None

    if int(page) < 1:
        page = 1
    page = int(page)
    topList = []
    start = (page - 1) * 8
    end = 8 + (page - 1) * 8
    count = 0

    endpoint = NEWSAPI_URL+"top-headlines?" + "country=" + country
    res = requests.get(endpoint, headers=AUTH_HEAD)
    res = res.json()
    for article in res["articles"]:
        if start <= count:
            topList.append(article)
        if count >= end:
            break
        count += 1

    embed = Embed(
        color=344703,
        title="Top News in "+country  #TODO: Map country code to country name
    )
    embed.set_footer(text="Powered by newsapi.org")

    # Actually put the news in
    for article in topList:
        embed.add_field(name=article.get("description", "[error desc_not_found]")[:255],
            value="[" + article.get("title", "[error title_not_found]") + "](" + article.get("url", "[error url_not_found]") + ")")

    embed.add_field(name="Note", value="To view next page, please use "+BOT_PREFIX+"top "+country+" "+str(page+1), inline=True)
    await context.send(embed=embed) #"\n".join(topList))


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
