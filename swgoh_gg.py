import requests

from errors import APIError

def get_guild_members_from_swgoh_gg(guild_id=None):
    guild_id = guild_id or "SF0zGaLuQiCapg85lVPxxw"

    guild_members = []

    # Set the API endpoint
    url = f"http://api.swgoh.gg/guild-profile/{guild_id}"

    # Send a GET request to get guild data from the API endpoint
    response = requests.get(url)

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
