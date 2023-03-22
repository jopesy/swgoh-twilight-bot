import discord
from discord import ui



class GuildMemberSelect(ui.Select):
    # def __init__(self):
    #     # The options that can be selected
    #     options = []

    #     for x in range(25):
    #         options.append(discord.SelectOption(label=f"Guild Member {x}"))

    #     # options.append(discord.SelectOption(label=f"ViperFray"))
    #     # options.append(discord.SelectOption(label=f"RebelSorsa"))

    #     super().__init__(options=options, min_values=0, max_values=25)

    async def callback(self, interaction: discord.Interaction):
        # Called when the user has chosen an option
        await interaction.response.defer()
