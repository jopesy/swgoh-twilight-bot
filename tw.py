
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
