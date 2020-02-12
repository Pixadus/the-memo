import dotenv, asyncio, aiohttp, os
from discord.ext import commands

# Actual fun stuffs
import random

dotenv.load_dotenv()

# In .env, put BOT_TOKEN="<memobot bot token>"
TOKEN = os.getenv("BOT_TOKEN")

BOT_PREFIX = ("~")
client = commands.Bot(command_prefix=BOT_PREFIX)

@client.event
async def on_ready():
    print("Logged in as " + client.user.name)

@client.command(pass_context=True, name="test")
async def test(context): #~test
    await context.send("test")

@client.command(pass_context=True, name="pull", help="Updates news from sources")
async def pull(context): #~pull
    await context.send("not yet implemented") #TODO: Add stuff from news aggregator i can't spell


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
