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


def get_guild_members(allycode):
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


def get_tw_defence(number_of_slots, guild_members, exclude_list=[]):
    # Exclude the people who don't participate
    participants = [x for x in guild_members if x['name'] not in exclude_list]

    # Calculate the total GP of all guild members
    total_gp = sum(member['gp'] for member in participants)

    # Calculate the minimum number of slots per member (2)
    min_slots_per_member = 2
    num_members = len(participants)

    # Calculate the number of slots per member based on GP, with a minimum of 2 slots
    slots_per_gp = number_of_slots / total_gp
    slots_per_member = [max(min_slots_per_member, round(member['gp'] * slots_per_gp)) for member in participants]

    # Calculate the total number of slots assigned
    total_slots = sum(slots_per_member)

    # Allocate the remaining slots more evenly between players, but still based on GP
    while total_slots < number_of_slots:
        # Calculate the GP per slot for each member
        gp_per_slot = [member['gp'] / slot_count for member, slot_count in zip(participants, slots_per_member)]

        # Find the member with the highest GP per slot
        max_gp_per_slot_index = gp_per_slot.index(max(gp_per_slot))

        # Allocate an additional slot to the member with the highest GP per slot
        if total_slots + 1 <= number_of_slots:
            slots_per_member[max_gp_per_slot_index] += 1
            total_slots += 1
        else:
            break

    # TODO: Ensure that the total doesn't exceed number_of_slots
    # if total_slots > number_of_slots:
    #     diff = total_slots - number_of_slots
    #     while diff > 0:
    #         # Find the first player (from the bottom)
    #         # with more than 2 slots and deduct one
    #         diff -= 1

    # Print the guild members' names and slot assignments
    data = []
    for i, member in enumerate(participants):
        name = member['name']
        slots = slots_per_member[i]
        data.append({"name": name, "slots": slots})

    # print("AVAILABLE SLOTS", number_of_slots)
    # print("TOTAL:", sum(slots_per_member))
    return data
