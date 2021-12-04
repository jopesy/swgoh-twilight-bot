import os

from discord import File
from discord.ext import commands
from dotenv import load_dotenv

from stats import get_gl_comparison, get_guild_gl_table

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
ALLYCODE = os.getenv("ALLYCODE", 143133382)

bot = commands.Bot(command_prefix="!", case_insensitive=True)

@bot.command(name="gl", help="GL roster of given guild (allycode). Defaults to Northern Twilight.")
async def guild_gl_table(ctx, allycode=None):
    await ctx.send("Fetching data from a galaxy far, far away...\n> _\"Patience you must have, my young padawan.\"_  –Yoda")
    allycode = allycode if allycode else ALLYCODE
    response = get_guild_gl_table(allycode)
    await ctx.send(response)

# @bot.command(name="tw", help="Responses with roster comparison between us and them")
# async def guild_comparison(ctx, guild_name=None):
#     await ctx.send("Fetching data from a galaxy far, far away...\n> _Patience you must have, my young padawan._  –Yoda")
#     allycode1 = ALLYCODE
#     allycode2 = ALLYCODE  # TODO
#     response = get_gl_comparison(allycode1, allycode2)
#     await ctx.send(response)

@bot.command(name="banaani", help="Voimabiisi (tm)")
async def banaania_poskeen(ctx):
    # video_url = "https://www.youtube.com/watch?v=fdMRX3XyD6U"
    # await ctx.send(video_url)
    await ctx.send("test")

@bot.command(name="vurski", help="Damn those geonosians!")
async def banaania_poskeen(ctx):
    await ctx.send(file=File("img/vurski.gif"))

bot.run(TOKEN)
