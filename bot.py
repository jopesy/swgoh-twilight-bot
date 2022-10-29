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

@bot.command(name="banaani", help="Voimabiisi (tm)")
async def banaania_poskeen(ctx):
    video_url = "https://www.youtube.com/watch?v=fdMRX3XyD6U"
    await ctx.send(video_url)

@bot.command(name="vurski", help="Damn those geonosians!")
async def send_vurski_gif(ctx):
    await ctx.send(file=File("img/vurski.gif"))

@bot.command(name="excel", help="Killan TW-puolustus XLSX-muodossa")
async def tw_defence_allocation_as_xlsx(ctx, slots_per_sector=None):
    await ctx.send("Calculating...\n> _\"Beep boop.\"_  –R2D2")
    allycode = ALLYCODE
    if slots_per_sector:
        slots_per_sector = int(slots_per_sector) if slots_per_sector.isdigit() else None
    file_path = "xlsx/tw_defence.xlsx"
    player_data, gp_median = get_guild_player_table(allycode)

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(file_path, {'use_future_functions': True})
    worksheet = workbook.add_worksheet()

    # Write the slot info
    worksheet.write(0, 0, "Slots per sector:")
    worksheet.write(0, 1, slots_per_sector or 0)
    worksheet.write(1, 0, "Total slots:")
    worksheet.write_formula(1, 1, "IF(B1,B1*8,0)")

    # Write the table header row
    worksheet.write(3, 0, "Name")
    worksheet.write(3, 1, "GP")
    worksheet.write(3, 2, "Teams")

    row = 4

    # Iterate over the data and write it out row by row.
    for name, gp in (player_data):
        # Player name
        col = 0
        worksheet.write(row, col,     name)

        # Player GP
        col = 1
        gp_rounded = round(gp / 1000000, 2)
        worksheet.write(row, col, gp_rounded)

        # Number of teams to place
        col = 2
        formula = f"IF($B{row+1},ROUND(($B{row+1}+2)/(SUM($B$5:$B$54)+2*COUNT($B$5:$B$54))*8*$B$1,0),0)"
        worksheet.write_formula(row, col, formula)

        # Player=X (used for generated string that can be copied to game chat)
        col = 4
        formula = f'=CONCAT(A${row+1}, "=", C${row+1})'
        worksheet.write_formula(row, col, formula)
        row += 1

    # Write totals
    row = 54
    worksheet.write_formula(row, 1, f"=SUM($B5:$B{row})")
    worksheet.write_formula(row, 2, f"=SUM($C5:$C{row})")

    # String that can be copied to game chat
    row = 56
    formula = f'=TEXTJOIN(", ", TRUE, E5:E53)'
    worksheet.write_formula(row, 1, formula)

    workbook.close()
    await ctx.channel.send(file=File(file_path))

bot.run(TOKEN)
