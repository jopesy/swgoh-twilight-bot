import os
import requests

from dotenv import load_dotenv

from errors import APIError

def get_guild_members_from_swgoh_gg(guild_id=None):

    # Load environment variables from .env
    load_dotenv()

    guild_id = guild_id or "SF0zGaLuQiCapg85lVPxxw"
    api_key = os.getenv("SWGOH_GG_API_KEY")

    guild_members = []

    # Set the API endpoint
    url = f"http://swgoh.gg/api/guild-profile/{guild_id}"
    headers = {
        "x-gg-bot-access": api_key
    }

    # Send a GET request to get guild data from the API endpoint
    response = requests.get(url, headers=headers)

    # Check if the response is successful
    if response.status_code == 200:
        # Get the guild members from the response
        data = response.json()["data"]
        roster = data.get("members")

        roster = sorted(roster, key=lambda x: x["galactic_power"], reverse=True)
        guild_members = [
            {
                "name": member["player_name"],
                "gp": member["galactic_power"],
            } for member in roster
        ]
    else:
        print("Error: Failed to fetch guild roster from swgoh.gg")
        raise APIError("Could not fetch guild data from swgoh.gg")

    return guild_members
