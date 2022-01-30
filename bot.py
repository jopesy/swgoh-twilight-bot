import os
import csv
import xlsxwriter

from discord import File
from discord.ext import commands
from dotenv import load_dotenv

from stats import get_gl_comparison, get_guild_gl_table, get_guild_player_table

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
    video_url = "https://www.youtube.com/watch?v=fdMRX3XyD6U"
    await ctx.send(video_url)

@bot.command(name="vurski", help="Damn those geonosians!")
async def send_vurski_gif(ctx):
    await ctx.send(file=File("img/vurski.gif"))

# @bot.command(name="csv", help="Killan GP-listaus CSV-muodossa")
# async def guild_gp_table_as_csv(ctx):
#     allycode = ALLYCODE
#     file_path = "csv/guild_gp_table.csv"
#     player_data, gp_median = get_guild_player_table(allycode)
#     for player in player_data:
#         print("player_data:", player)
#     with open(file_path, "w") as f:
#         writer = csv.writer(f)
#         header = ["name", "GP"]
#         writer.writerow(header)
#         writer.writerows(player_data)
#     await ctx.channel.send(file=File(file_path))

@bot.command(name="excel", help="Killan GP-listaus XLSX-muodossa")
async def guild_gp_table_as_xlsx(ctx, total_slots=None):
    allycode = ALLYCODE
    if total_slots:
        total_slots = int(total_slots) if total_slots.isdigit() else None
    file_path = "xlsx/guild_gp_table.xlsx"
    player_data, gp_median = get_guild_player_table(allycode)
    num_teams_median = None

    print("GP median:", gp_median)

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet()

    # Write the header row
    worksheet.write(0, 0, "Name")
    worksheet.write(0, 1, "GP")
    if total_slots:
        worksheet.write(0, 2, "TW defence")

    row = 1
    col = 0

    if total_slots:
        num_players = len(player_data)
        num_teams_median = total_slots/num_players

        print("TEAMS per median:", num_teams_median)

    # Iterate over the data and write it out row by row.
    for name, gp in (player_data):
        gp_rounded = round(gp / 1000000, 2)
        worksheet.write(row, col,     name)
        worksheet.write(row, col + 1, gp_rounded)
        if total_slots and num_teams_median:
            if gp == gp_median:
                worksheet.write(row, col + 2, num_teams_median)
        row += 1

    workbook.close()
    await ctx.channel.send(file=File(file_path))

bot.run(TOKEN)
