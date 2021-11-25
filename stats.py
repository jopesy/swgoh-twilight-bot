import os

from dotenv import load_dotenv
from swgoh_api.swgohhelp import settings, SWGOHhelp

from table2ascii import table2ascii as t2a, Alignment

load_dotenv()

SWGOH_HELP_API_USERNAME = os.getenv("SWGOH_HELP_API_USERNAME")
SWGOH_HELP_API_PASSWORD = os.getenv("SWGOH_HELP_API_PASSWORD")

GL_IDS = [
    "SUPREMELEADERKYLOREN",
    "GRANDMASTERLUKE",
    "GLREY",
    "JEDIMASTERKENOBI",
    "SITHPALPATINE",
]

def get_gl_comparison(allycode1, allycode2):

    guild1_gls = get_guild_gl_table(allycode1)
    guild2_gls = get_guild_gl_table(allycode2)

    response = f"{guild1_gls}\n{guild2_gls}"

    return response


def get_guild_gl_table(allycode):
    print("COMPARE GUILDS")
    creds = settings(SWGOH_HELP_API_USERNAME, SWGOH_HELP_API_PASSWORD, "something", "anything")
    client = SWGOHhelp(creds)

    print("get guild data...")
    guild_data = client.get_data("guild", allycode)

    # GALACTIC LEGENDS
    COUNT_GL_TOTAL = 0
    GL_NAME_COUNT_MAP = {
        "SLKR": {
            "TOTAL": 0,
            "G13": 0,
            "ULTI": 0
        },
        "JMK": {
            "TOTAL": 0,
            "G13": 0,
            "ULTI": 0,
        },
        "JML": {
            "TOTAL": 0,
            "G13": 0,
            "ULTI": 0,
        },
        "REY": {
            "TOTAL": 0,
            "G13": 0,
            "ULTI": 0,
        },
        "LV": {
            "TOTAL": 0,
            "G13": 0,
            "ULTI": 0,
        },
        "SEE": {
            "TOTAL": 0,
            "G13": 0,
            "ULTI": 0,
        },
    }

    # OTHER KEY TOONS
    COUNT_TRAYA = 0
    COUNT_GAS = 0
    COUNT_JKL = 0
    COUNT_WAT = 0

    # KEY CAPITAL SHIPS
    SHIP_NAME_COUNT_MAP = {
        "NEGO": {
            "TOTAL": 0,
            "5": 0,
            "6": 0,
            "7": 0,
        },
        "MALE": {
            "TOTAL": 0,
            "5": 0,
            "6": 0,
            "7": 0,
        },
        "EXECUTOR": {
            "TOTAL": 0,
            "5": 0,
            "6": 0,
            "7": 0,
        },
    }

    if guild_data:
        guild_name = guild_data[0]["name"]
        roster = guild_data[0]["roster"]
        player_codes = [player["allyCode"] for player in roster]
        print("get player data...")
        player_data = client.get_data("player", player_codes)
        for player in player_data:
            roster = player["roster"]

            for toon in roster:

                # GALACTIC LEGENDS
                if toon["defId"] in GL_IDS:
                    COUNT_GL_TOTAL += 1
                if toon["defId"] == "SUPREMELEADERKYLOREN":
                    GL_NAME_COUNT_MAP["SLKR"]["TOTAL"] += 1
                    if toon["gear"] == 13:
                        GL_NAME_COUNT_MAP["SLKR"]["G13"] += 1
                if toon["defId"] == "SITHPALPATINE":
                    GL_NAME_COUNT_MAP["SEE"]["TOTAL"] += 1
                    if toon["gear"] == 13:
                        GL_NAME_COUNT_MAP["SEE"]["G13"] += 1
                if toon["defId"] == "GLREY":
                    GL_NAME_COUNT_MAP["GLREY"]["TOTAL"] += 1
                    if toon["gear"] == 13:
                        GL_NAME_COUNT_MAP["GLREY"]["G13"] += 1
                if toon["defId"] == "JEDIMASTERKENOBI":
                    GL_NAME_COUNT_MAP["JMK"]["TOTAL"] += 1
                    if toon["gear"] == 13:
                        GL_NAME_COUNT_MAP["JMK"]["G13"] += 1
                if toon["defId"] == "GRANDMASTERLUKE":
                    GL_NAME_COUNT_MAP["JML"]["TOTAL"] += 1
                    if toon["gear"] == 13:
                        GL_NAME_COUNT_MAP["JML"]["G13"] += 1
                if toon["defId"] == "LORDVADER":
                    GL_NAME_COUNT_MAP["LV"]["TOTAL"] += 1
                    if toon["gear"] == 13:
                        GL_NAME_COUNT_MAP["LV"]["G13"] += 1

                # OTHER KEY TOONS
                if toon["defId"] == "DARTHTRAYA":
                    COUNT_TRAYA += 1
                if toon["defId"] == "GENERALSKYWALKER":
                    COUNT_GAS += 1
                if toon["defId"] == "JEDIKNIGHTLUKE":
                    COUNT_JKL += 1
                if toon["defId"] == "WATTAMBOR":
                    COUNT_WAT += 1

                # KEY CAPITAL SHIPS
                if toon["defId"] == "CAPITALNEGOTIATOR":
                    SHIP_NAME_COUNT_MAP["NEGO"]["TOTAL"] += 1
                    if toon["rarity"] == 7:
                        SHIP_NAME_COUNT_MAP["NEGO"]["7"] += 1
                    if toon["rarity"] == 6:
                        SHIP_NAME_COUNT_MAP["NEGO"]["6"] += 1
                    if toon["rarity"] == 5:
                        SHIP_NAME_COUNT_MAP["NEGO"]["5"] += 1
                if toon["defId"] == "CAPITALMALEVOLENCE":
                    SHIP_NAME_COUNT_MAP["MALE"]["TOTAL"] += 1
                    if toon["rarity"] == 7:
                        SHIP_NAME_COUNT_MAP["MALE"]["7"] += 1
                    if toon["rarity"] == 6:
                        SHIP_NAME_COUNT_MAP["MALE"]["6"] += 1
                    if toon["rarity"] == 5:
                        SHIP_NAME_COUNT_MAP["MALE"]["5"] += 1
                if toon["defId"] == "CAPITALEXECUTOR":
                    SHIP_NAME_COUNT_MAP["EXECUTOR"]["TOTAL"] += 1
                    if toon["rarity"] == 7:
                        SHIP_NAME_COUNT_MAP["EXECUTOR"]["7"] += 1
                    if toon["rarity"] == 6:
                        SHIP_NAME_COUNT_MAP["EXECUTOR"]["6"] += 1
                    if toon["rarity"] == 5:
                        SHIP_NAME_COUNT_MAP["EXECUTOR"]["5"] += 1

    count_g13_total = sum([GL_NAME_COUNT_MAP[x]["G13"] for x in GL_NAME_COUNT_MAP])
    gl_table = t2a(
        header=["GL", "COUNT", "G13", "ULTI"],
        body=[
            ["SLKR", str(GL_NAME_COUNT_MAP["SLKR"]["TOTAL"]), str(GL_NAME_COUNT_MAP["SLKR"]["G13"]), "-"],
            ["JMK", str(GL_NAME_COUNT_MAP["JMK"]["TOTAL"]), str(GL_NAME_COUNT_MAP["JMK"]["G13"]), "-"],
            ["JML", str(GL_NAME_COUNT_MAP["JML"]["TOTAL"]), str(GL_NAME_COUNT_MAP["JML"]["G13"]), "-"],
            ["REY", str(GL_NAME_COUNT_MAP["REY"]["TOTAL"]), str(GL_NAME_COUNT_MAP["REY"]["G13"]), "-"],
            ["LV", str(GL_NAME_COUNT_MAP["LV"]["TOTAL"]), str(GL_NAME_COUNT_MAP["LV"]["G13"]), "-"],
            ["SEE", str(GL_NAME_COUNT_MAP["SEE"]["TOTAL"]), str(GL_NAME_COUNT_MAP["SEE"]["G13"]), "-"],
        ],
        footer=["TOTAL", str(COUNT_GL_TOTAL), str(count_g13_total), "-"],
        first_col_heading=True,
        alignments=[Alignment.LEFT] + [Alignment.RIGHT] * 3, # First is left, remaining 5 are right
        # column_widths=[8] * 6,  # [5, 5, 5, 5, 5, 5]
    )

    ship_table = t2a(
        header=["SHIP", "COUNT", "5*", "6*", "7*"],
        body=[
            [
                "NEGO",
                str(SHIP_NAME_COUNT_MAP["NEGO"]["TOTAL"]),
                str(SHIP_NAME_COUNT_MAP["NEGO"]["5"]),
                str(SHIP_NAME_COUNT_MAP["NEGO"]["6"]),
                str(SHIP_NAME_COUNT_MAP["NEGO"]["7"]),
            ],
            [
                "MALE",
                str(SHIP_NAME_COUNT_MAP["MALE"]["TOTAL"]),
                str(SHIP_NAME_COUNT_MAP["MALE"]["5"]),
                str(SHIP_NAME_COUNT_MAP["MALE"]["6"]),
                str(SHIP_NAME_COUNT_MAP["MALE"]["7"]),
            ],
            [
                "EXECUTOR",
                str(SHIP_NAME_COUNT_MAP["EXECUTOR"]["TOTAL"]),
                str(SHIP_NAME_COUNT_MAP["EXECUTOR"]["5"]),
                str(SHIP_NAME_COUNT_MAP["EXECUTOR"]["6"]),
                str(SHIP_NAME_COUNT_MAP["EXECUTOR"]["7"]),
            ],
        ],
        first_col_heading=True,
        alignments=[Alignment.LEFT] + [Alignment.RIGHT] * 4,
    )

    response = f"```{guild_name}\n=================\n{gl_table}\n{ship_table}```"

    return response
