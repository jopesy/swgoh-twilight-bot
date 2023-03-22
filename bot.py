import os
import csv
import xlsxwriter
import asyncio

import discord
from discord import File, Embed, Intents
from discord.ext import commands
from discord.ui import Button, Select, View
from dotenv import load_dotenv
from textwrap import wrap

from errors import APIError
from stats import get_gl_comparison, get_guild_gl_table, get_guild_player_table
from tw import get_guild_members, get_tw_defence

from ui import GuildMemberSelect

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
ALLYCODE = os.getenv("ALLYCODE", 143133382)

bot = commands.Bot(command_prefix="!", case_insensitive=True, intents=Intents.all())

@bot.command(name="gl", help="GL roster of given guild (allycode). Defaults to Northern Twilight. NOTE: Might not work correctly!")
async def guild_gl_table(ctx, allycode=None):
    await ctx.send("Fetching data from a galaxy far, far away...\n> _\"Patience you must have, my young padawan.\"_  –Yoda")
    allycode = allycode if allycode else ALLYCODE
    response = get_guild_gl_table(allycode)
    await ctx.send(response)


@bot.command(name="banaani", help="Voimabiisi (tm)")
async def banaania_poskeen(ctx):
    video_url = "https://www.youtube.com/watch?v=fdMRX3XyD6U"
    await ctx.send(video_url)


@bot.command(name="vurski", help="Damn geos!")
async def send_vurski_gif(ctx):
    await ctx.send(file=File("img/vurski.gif"))


@bot.command(name="tw", help="TW-puolustuskiintiöt (v2.0)")
async def get_tw_quotas(ctx, slots_per_sector):
    await ctx.send("Haetaan killan tietoja... :rocket:")

    guild_members = get_guild_members(ALLYCODE)
    guild_members_sorted = sorted(guild_members, key=lambda x: x["name"].lower())

    # Create a list of `SelectOption` objects representing the fruit options
    options = [discord.SelectOption(label=member["name"]) for member in guild_members_sorted]

    # Create the `Select` components with the guild member options.
    # We need multiple because the Discord API doesn't allow more than 25 options.
    select1_options = options[:25]
    select = GuildMemberSelect(options=select1_options, min_values=0, max_values=25)

    if len(options) > 25:
        select2_options = options[25:]
        select_2 = GuildMemberSelect(options=options[25:], min_values=0, max_values=len(select2_options))

    # Create a `Button` component to submit the selection
    submit_button = Button(label="Submit")

    # Create a view
    view = View()
    view.add_item(select)
    if select_2:
        view.add_item(select_2)
    view.add_item(submit_button)

    # Send a message with the `Select` and `Button` components
    message = await ctx.send("Kuka EI osallistu?", view=view)

    def check(res):
        # Check if the user who invoked the command interacted with the `Button` component
        return res.user == ctx.author and res.message.id == message.id and res.data["component_type"] == 2

    try:
        interaction = await bot.wait_for('interaction', check=check, timeout=120.0)
        selection = select.values + select_2.values

        # Update the form message after submit
        text = ", ".join(selection) if len(selection) else "Kaikki osallistuu! "
        emoji = ":pleading_face:" if len(selection) else ":partying_face:"
        embed=Embed(description=f"{text} \n\n {emoji}", color=0x060b9)
        await message.edit(view=None, embed=embed)
        await interaction.response.defer()

        # Get the TW defence quotas
        total_slots = int(slots_per_sector) * 8
        quotas = get_tw_defence(
            number_of_slots=total_slots,
            guild_members=guild_members,
            exclude_list=selection
        )

        # Send the response
        text = ""
        chat_text = ""
        chat_text_parts = []
        chat_text_part = ""

        for i, line in enumerate(quotas):
            text += f"\n {line['name']}: {line['slots']}"

            if len(chat_text_part) > 100:
                chat_text_parts.append(chat_text_part[:-2])
                chat_text_part = ""

            chat_text_part += f"{line['name']}={line['slots']}"

            if i < len(quotas) - 1:
                chat_text_part += ", "

            if i == len(quotas) - 1:
                chat_text_parts.append(chat_text_part) 

        chat_text = "\n\n".join(chat_text_parts)

        embed=Embed(title="TW-puolustus", description=text, color=0x31FC00)
        chat_embed=Embed(title="Peli-chat", description=chat_text, color=0x31FC00)
        await ctx.send(embed=embed)
        await ctx.send(embed=chat_embed)

    except asyncio.TimeoutError:
        await ctx.send("Time's up! Try again!")
        return


@bot.command(name="excel", help="TW-puolustuskiintiöt XLSX-muodossa")
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


@bot.event
async def on_command_error(ctx, error):
    print("on_command_error:", error)
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command. Try using** `!help` **to figure out the commands!")
    if isinstance(error, APIError):
        print("APIError:", error)
        await ctx.send("SWGOH API is not responding. Try again later.")

bot.run(TOKEN)
