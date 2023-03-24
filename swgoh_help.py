import os
import requests

from dotenv import load_dotenv

from errors import APIError

load_dotenv()

SWGOH_HELP_API_USERNAME = os.getenv("SWGOH_HELP_API_USERNAME")
SWGOH_HELP_API_PASSWORD = os.getenv("SWGOH_HELP_API_PASSWORD")


def get_api_token():
    # Set the API endpoint to fetch the API token
    token_url = 'https://api.swgoh.help/auth/signin'

    user = "username="+SWGOH_HELP_API_USERNAME    
    user += "&password="+SWGOH_HELP_API_PASSWORD
    user += "&grant_type=password"
    user += "&client_id="+"something"
    user += "&client_secret="+"anything"

    payload = user

    api_token = None

    # Set the API headers to fetch the API token
    token_headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': str(len(payload)),
    }

    # Send a POST request to fetch the API token
    token_response = requests.post(token_url, headers=token_headers, data=payload, timeout=10)

    # Check if the response is successful
    if token_response.status_code == 200:
        # Get the API token from the response
        api_token = token_response.json()['access_token']
    else:
        print("Error: Failed to fetch API token from swgoh.help API")
        raise APIError("Could not fetch guild data from swgoh.help API.")

    return api_token


def get_guild_members_from_swgoh_help(allycode):
    api_token = get_api_token()

    guild_members = []

    if api_token:
        # Set the API endpoint and parameters
        url = 'https://api.swgoh.help/swgoh/guild/'
        guild_name = 'Northern Twilight'

        # Set the API parameters
        params = {
            'allycode': allycode,  # Enter your ally code here
            'guildname': guild_name,
        }

        # Set the API headers
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + api_token,
        }

        # Send a POST request to get guild data from the API endpoint
        response = requests.post(url, headers=headers, json=params)

        # Check if the response is successful
        if response.status_code == 200:
            # Get the guild members from the response
            data = response.json()
            guild_members = data[0]['roster']

            guild_members = sorted(guild_members, key=lambda x: x["gp"], reverse=True)
        else:
            print("Error: Failed to fetch guild roster from swgoh.help API")
            raise APIError("Could not fetch guild data from swgoh.help API.")
    else:
        print("Error: Failed to fetch guild roster from swgoh.help API")
        raise APIError("Could not fetch guild data from swgoh.help API.")

    return guild_members
