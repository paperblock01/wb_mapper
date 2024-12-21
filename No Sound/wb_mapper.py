import requests
import time
import getopt, sys


# Add modes or maps to these dictionaries.
# Add a shorthand and full name in Modes and Modes_long

Modes = {
    "tdm": 128,
    "ml": 138,
    "bd": 275,
    "cp": 135,
    "ve": 136,
    "gg": 15,
}
Modes_long = {
    "Team Death Match": 128,
    "Missile Launch": 138,
    "Bomb Disposal": 275,
    "Capture Points": 135,
    "Vehicle Escort": 136,
    "Gun Game": 15,
}
Maps = {
    "area15base": 21,
    "area15bunker": 22,
    "citypoint": 13,
    "cologne": 44,
    "desert": 0,
    "escape": 6,
    "flooded": 4,
    "frontier": 31,
    "goldmine": 47,
    "goldminev2": 49,
    "heist": 32,
    "kitchen": 29,
    "moonbase": 20,
    "northwest": 1,
    "office": 3,
    "pacific": 2,
    "remagen": 8,
    "siege": 39,
    "skullisland": 24,
    "southwest": 7,
    "spacestation": 38,
    "temple": 5,
    "thesomme": 15,
    "tomb": 14,
    "tribute": 18,
    "tribute(cyberpunk)": 19,
    "cyberpunk": 19,
    "zengarden": 43,
    "containers": 37,
    "crisscross": 40,
    "dwarfsdungeon": 28,
    "dwarf'sdungeon": 28,
    "dwarfdungeon": 28,
    "hanger": 25,
    "pyramid": 36,
    "quarry": 27,
    "sniperalley": 35,
    "snipersonly": 41,
    "threelane": 34,
    "towerofpower": 33,
}

# Regional locations
classic = ["USA","USA_WEST","ASIA","JAPAN","EUROPE","INDIA","AUSTRALIA","RUSSIA"]
fourvfour = ["USA_4V4","EU_4V4","ASIA_4V4"]

# Default program arguments
# players: True stands for G (greater than or equal) and False stands for L (less than or equal)
var = {
    "game": "classic",
    "players": [True, 1],
    "mode": "",
    "map": "",
    "location": "",
    "finite": True,
}

# The help message
def help_msg():
    # A string of the modes and their shorthand
    str_modes = ""
    for i,j in zip(Modes, Modes_long):
        # Adds a 5 space padding to the right
        str_modes += f"        {i.ljust(5)}: {j}\n"

    # A string of the maps
    str_maps = ""
    for i in Maps:
        # Adds a 5 space padding to the right
        str_maps += f"        {i}\n"

    # A string of the classic regions
    str_classic = ""
    for i in classic:
        str_classic += f"            {i}\n"

    # A string of the 4v4 regions
    str_4v4 = ""
    for i in fourvfour:
        str_4v4 += f"            {i}\n"

    # Printed help message
    Help = f"""           _
          | |
 __      _| |__          _ __ ___   __ _ _ __  _ __   ___ _ __
 \\ \\ /\\ / / '_ \\        | '_ ` _ \\ / _` | '_ \\| '_ \\ / _ \\ '__|
  \\ V  V /| |_) |       | | | | | | (_| | |_) | |_) |  __/ |
   \\_/\\_/ |_.__/ ______ |_| |_| |_|\\__,_| .__/| .__/ \\___|_|
                |______|                | |   | |
                                        |_|   |_|

 A program to search the War Brokers server list for servers that
 match a specified number of players, game mode, map, or region.

 NOTE: [Servers with no human players are not detected]

 Arguments
    -h, --help              Display this help message

    -f, --forever           Include this argument and the program
                            will map servers until the user stops
                            it manually.

    -g, --game=             Specify the game. Default is classic.

        classic
        4v4

    -p, --players=          Specify the players in the server. The
                            sign is the first character and the number
                            of players follows. The number of players
                            cannot equal Zero.

        -p [sign][number]

        [sign]
        L : Less than or equal to
        G : greater than or equal to

        -p L10
        -p G4

    -m, --mode=             Specify a mode. Write ONLY the shorthand. If
                            spaces are included, put it in quotes. The
                            default is all modes. Works only when classic
                            is selected.

{str_modes}
    -a, --map=              Specify a map. If spaces are included, put it
                            in quotes. The default is all maps.

{str_maps}
    -r, --region=           Specify a region. If spaces are included, put
                            it in quotes. Only regions in the chosen game
                            are accepted.

        Classic Regions:
{str_classic}
        4v4 Regions:
{str_4v4}
Example:

python3 {sys.argv[0]} -g Classic -p G10 -m gg -a 'Area 15 Bunker' -r 'usa, usa_west, europe'
"""
    print(Help)

# Handle user input

# Code stolen from https://www.geeksforgeeks.org/command-line-arguments-in-python/
# Remove the first argument from the list of arguments because it is the file name
argumentList = sys.argv[1:]
# Options
options = "hfg:p:m:a:r:"

# Long options
long_options = ["help", "forever", "game=", "players=", "mode=","map=","region="]

try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)

    # checking each argument
    for currentArgument, currentValue in arguments:

        if currentArgument in ("-h", "--help"):
            help_msg()
            exit(0)
        elif currentArgument in ("-f", "--forever"):
            # When the program should not stop after a match is found
            var["finite"] = False
        elif currentArgument in ("-g", "--game"):
            var["game"] = currentValue

        elif currentArgument in ("-p", "--players"):
            # Get the G or L sign and the player number
            sign = currentValue[0]

            if sign == "G":
                sign = True
            elif sign == "L":
                sign = False
            else:
                print("\n- [ERROR]: Unknown player operater! (G | L)\n")
                exit(1)

            # If a number is not inputted
            try:
                int(currentValue[1:])
            except ValueError:
                print("\n- [ERROR]: Enter an integer after the sign: [L|G][integer]\n  example: L10\n")
                exit(1)

            num = int(currentValue[1:])

            var["players"][0] = sign
            var["players"][1] = num

        elif currentArgument in ("-m", "--mode"):
            var["mode"] = currentValue

        elif currentArgument in ("-a", "--map"):
            var["map"] = currentValue

        elif currentArgument in ("-r", "--region"):
            var["location"] = currentValue

except getopt.error as err:
    # output error, and return with an error code
    print (str(err))
    exit(1)

# Accepts an data values and returns a list of data used in the mapper function
# string, list[bool,int], string, string, string
def set_data(game,players,mode,map,location):
    # list for the finalized data
    data = []

# Game
    # If a game that is not classic or 4v4 is selected
    if game.lower() != "classic" and game.lower() != "4v4":
        print("\n- [ERROR]: Unknown game selected! (classic | 4v4)\n")
        exit(1)

    # Variable to store which regions depending on the mode played
    game_regions = 0

    # If the game is classic, add all the classic locations
    if game.lower() == "classic":
        game_regions = classic
    # Add all the 4v4 locations
    elif game.lower() == "4v4":
        game_regions = fourvfour
        # Unselect any modes
        mode = ""

    # Add the game to the data
    data.append(game.lower())


# Players
    # Add the player list to data
    data.append(players)

# Mode
    # Makes a list of each selected mode in an ordered manner
    striped_mode = mode.lower().replace(" ", "").split(",")

    # If no mode is selected
    if mode == "":
        data.append("all")
    # If the inputted modes exist as keys in the modes list
    elif all(name in Modes.keys() for name in striped_mode):
        # Match each mode with its number from the modes list
        for i in range(0,len(striped_mode)):
            # Change the string to the matching number in the striped_mode list
            striped_mode[i] = Modes[striped_mode[i]]

        # Add the new striped_mode list to data
        data.append(striped_mode)
    else:
        print("\n- [ERROR]: Unknown mode selected! (tdm | ml | bd | cp | ve | gg)\n")
        exit(1)

# Map
    # Makes an ordered list of selected maps
    striped_map = map.lower().replace(" ", "").split(",")

    # If no map is selected
    if map == "":
        data.append("all")
    # If the inputted maps exist as keys in the maps list
    elif all(name in Maps.keys() for name in striped_map):
        # Match each map to its number from the maps list
        for i in range(0,len(striped_map)):
            # Change the string to the matching number in the striped_map list
            striped_map[i] = Maps[striped_map[i]]

        # Add the new striped_map list to data
        data.append(striped_map)
    else:
        print("\n- [ERROR]: Unknown map selected!\n")
        exit(1)

# Location
    # If no location is selected
    if location == "":
        # Add the regions based on the game selected
        data.append(game_regions)
    # If certain locations are set
    elif location != "":
        # Orders the string of locations
        striped_location = location.upper().replace(" ", "").split(",")

        if all(name in game_regions for name in striped_location):
            data.append(striped_location)
        else:
            print("\n- [ERROR]: Unknown regions selected! Check set game.\n")
            exit(1)

    return data

# Returns a list of data for every server in the specified region
def get_server_data(region):
    # Send a request to the following endpoint and retrieve server data from the defined region
    r = requests.get(f'https://store2.warbrokers.io/293//server_list.php?location={region}')

    # If an actual region was not inputted
    if r.text == "0":
        print("\n- [ERROR]: Unknown region!\n")
        exit(1)

    # Store the text response in an array split by the following string
    response = r.text.split(f",{region},")

    return response

# Takes lists from get_server_data and set_data. Outputs a list of 1 and 0 for each server that does or does not match the criteria
def player_check(server_data, set_data):
    # The index of the sign. True is >=. False is <=.
    sign = set_data[1][0]
    # The index for the set number of players
    num = int(set_data[1][1])

    if num == 0:
        print("\n- [ERROR]: Number of players cannot Be zero!\n")
        exit(1)

    players = [];
    # Sort the server data into their own lists. Ignoring the first string.
    for i in range (1,len(server_data)):
        # Split the server data into values
        x = server_data[i].split(",")
        # The number of players is the third value
        players.append(int(x[2]))

    # List describing if a server matches the player criteria
    check = []

    # Loop through the players in each server
    for i in players:
        # If there are no players in the server, skip
        if i == 0:
            check.append(0)
            continue
        # If sign is true and players in the server is >= num
        elif sign and i >= num:
            check.append(1)
        # If sign is false and players in the server is <= num
        elif not sign and i <= num:
            check.append(1)
        # If the server does not match the player criteria, add a 0
        else:
            check.append(0)

    return check

def mode_check(server_data, set_data):
    # Index for the list of wanted game modes
    wanted = set_data[2]

    # If all maps are allowed
    if wanted == "all":
        return True

    modes = [];
    # Sort the server data into their own lists. Ignoring the first string
    for i in range (1,len(server_data)):
        # Split the server data into values
        x = server_data[i].split(",")
        # The game mode data is the second value
        modes.append(int(x[1]))

    # List describing if a server matches the mode criteria
    check = []

    # Loop through the mode on each server
    for i in modes:
        # If the mode on the server is in the list of wanted modes
        if i in wanted:
            check.append(1)
        else:
            check.append(0)

    return check

def map_check(server_data, set_data):
    # Index for the list of wanted maps
    wanted = set_data[3]

    # If all maps are allowed
    if wanted == "all":
        return True

    maps = [];
    # Sort the server data into their own lists. Ignoring the first string.
    for i in range (1,len(server_data)):
        # Split the server data into values
        x = server_data[i].split(",")
        # The map data is the fourth value
        maps.append(int(x[3]))

    # List describing if a server matches the map criteria
    check = []

    # Loop through the maps on each server
    for i in maps:
        # If the map on the server is in the list of wanted maps
        if i in wanted:
            check.append(1)
        else:
            check.append(0)

    return check

# server_data is a list from get_server_data. index is the index of the server. location is a string.
def output(server_data, index, location):
    # Skip the first data value in server_data
    data = server_data[index+1].split(",")
    # Information about the server
    player = int(data[2])
    mode = int(data[1])
    map = int(data[3])

    # Find the name of the mode on the server
    for i in Modes_long:
        if mode == Modes_long[i]:
            mode = i.upper()
            break
        else:
            continue
    # Find the name of the map on the server
    for j in Maps:
        if map == Maps[j]:
            map = j.upper()
            break
        else:
            continue

    # Print the information about the server
    print(f"{location} : {mode} : {map} ({data[3]}) : {player} / 16 players")

# Takes a list outputted from the set_data function
def game_check(set_data):
    # check is a variable that describes the number of matching servers
    check = 0

    # Loop through all the set regions
    for i in set_data[4]:
        # Gets server data for the current region
        server_data = get_server_data(i)

        # The matches of players, modes, and maps in the server
        player = player_check(server_data,set_data)
        mode = mode_check(server_data,set_data)
        map = map_check(server_data,set_data)

        # If mode or map are not set to anything (they are set to True)
        # Set them to a list of 1's
        if mode == True:
            mode = [1 for k in range(len(player))]
        if map == True:
            map = [1 for k in range(len(player))]


        for j in range (0,len(player)):
            # If all values in the check list are 1 and true
            if player[j] and mode[j] and map[j]:
                output(server_data,j,i)
                # Add a number for a match
                check += 1
            # Otherwise check the next server
            else:
                continue

    # Return the results of the check
    return check

# Generates data based on the user's input
settings = set_data(var["game"],var["players"],var["mode"],var["map"],var["location"])

try:
    while True:
        # Number of matching servers
        check = game_check(settings)

        # If matches are found, stop the loop
        if check:
            print(f"- Found {check} Match{"!" if check == 1 else "es!"}\n")

            # If playalert is True, play a notification
            if var["playalert"]:
                notification()

            # If finite is True and the program should not run forever
            if var["finite"]:
                exit(0)

        time.sleep(30)

# If Ctrl + C or similar is pressed, exit gracefully
except KeyboardInterrupt:
    print("\n\nMapping stopped.")
    exit(0)


