import os
import json
import time
import requests
import sys

giantbomb_api_key = "INSERT KEY HERE"
twitch_api_key = "INSERT KEY HERE"

def getPlatformNumbersFromGiantBomb(gb_api,offset):
    headers = {
    'Accept': 'application/json',
    'User-Agent': 'Pikachu-ororo',
    }

    params = (
        ('api_key',       gb_api),
        ('format',        'json'),
        ('field_list', 'name,id'),
        ('sort',        'id:asc'),
        ('offset',        offset),
    )
    response = requests.get('https://www.giantbomb.com/api/platforms/', headers=headers, params=params)
    return response.json()["results"]


def producePlatformNumbersFile(gb_api):
    print("Producing platform IDs file...")
    offset = 0
    ids = []
    tmp_ids = []
    
    while True:
        print("Querying GiantBomb for platform IDs with offset {}.".format(offset))        
        tmp_ids = getPlatformNumbersFromGiantBomb(gb_api,offset)
        print("Query complete.")
        if not tmp_ids:
            break
        ids = ids + tmp_ids
        offset+=100
        print("Cooling down...")
        time.sleep(5)

    new_dict = {}
    for item in ids:
        new_dict[item['id']] = item['name']
    with open("platform_numbers.json","w") as f:
        f.write(json.dumps(new_dict, indent=4, sort_keys=True))

    print("All pages queried. Platform IDs file successfully generated.")
    return 0

def getGameNumbersFromGiantBomb(gb_api,console_id,offset):
    headers = {
    'Accept': 'application/json',
    'User-Agent': 'Pikachu-ororo',
    }

    params = (
        ('api_key',       gb_api),
        ('format',        'json'),
        ('field_list', 'name,id'),
        ('offset',        offset),
        ('platforms', console_id)
    )
    response = requests.get('https://www.giantbomb.com/api/games/', headers=headers, params=params)
    return response.json()['results']



def produceGameListFile(gb_api,console_id):
    filename = str(console_id) + "_games.json"
    print("Producing platform {} file...".format(console_id))
    offset = 0
    ids = []
    tmp_ids = []
    while True:
        print("Querying GiantBomb for game IDs with offset {}.".format(offset))    
        tmp_ids = getGameNumbersFromGiantBomb(gb_api,console_id,offset)
        print("Query complete.")
        if not tmp_ids:
            break
        ids = ids + tmp_ids
        offset+=100
        print("Cooling down...")
        time.sleep(10)
    with open(filename,"w") as f:
        f.write(json.dumps(ids, indent=4, sort_keys=True))

    print("All pages queried. Platform {} file successfully generated.".format(console_id))
    return 0

def getPageFromTwitch(tw_api,pagination):
    headers = {
        'Client-ID': tw_api,
    }

    params = (
        ('first', '100'),
        ('after', pagination)
    )

    response = requests.get('https://api.twitch.tv/helix/games/top', headers=headers, params=params)
    json_response = response.json()

    try:
        pagination = json_response["pagination"]['cursor']
    except KeyError:
        pagination = 'None'
    data = json_response["data"]
    return (pagination,data)

def getActiveGamesFromTwitch(tw_api):
    print("Getting active games from Twitch...")
    active_games = []
    tmp_games = []
    pagination = ''
    i = 1
    while True:
        print("Querying page {} from Twitch...".format(i))
        results = getPageFromTwitch(tw_api,pagination)
        print("Query complete.")
        pagination = results[0]
        if pagination == 'None':
            break
        tmp_games = results[1]
        active_games = active_games + tmp_games
        i+=1
        print("Cooling down...")
        time.sleep(3)

    print("All pages queried. Active games list generated.")
    return active_games

def filterActiveGamesByConsole(active_games,console_games):
    filtered_games = []
    for ag in active_games:
        for cg in console_games:
            if (ag["id"] == cg["id"]) or ag["name"] == cg["name"]:
                filtered_games.append(ag)
                break
    return filtered_games

def resetFiles():
    os.remove("*.json")
    print("Files have been reset.")

def checkExistingFiles():
    try:
        file = open('platform_numbers.json')
        file.close()
    except FileNotFoundError:
        print("Platform IDs file not found.")
        producePlatformNumbersFile(giantbomb_api_key)
    
    json_files = os.listdir()
    if not json_files:
        return 0

    platform_ids = []
    with open('platform_numbers.json') as f:
        platform_ids = json.load(f)
    
    existing_platforms = {}
    for file in json_files:
        try:
            plat_number = file.split("_")[0]
            if platform_ids[plat_number]:
                existing_platforms[plat_number] = platform_ids[plat_number]
        except:
            continue
    return existing_platforms

def addNewPlatform():
    platform_name = input("Name of the platform [don't use short handles like PSP!]: ").lower()

    possible_results = {}
    platform_ids = []
    with open('platform_numbers.json') as f:
        platform_ids = json.load(f)

    for platform in platform_ids:
        if platform_name in platform_ids[platform].lower():
            possible_results[platform] = platform_ids[platform]
    
    result_size = len(possible_results)

    if result_size == 0:
        print("No platforms found. Did you provide the right name?")
        return 1

    print("One or more platforms found! Is it one of these?")
    for item in possible_results:
        print("{}: {}".format(possible_results[item],item))
    print("None of the above: 0")
    answer = input("Write a number: ")
    try:
        if answer == 0:
            return 1
        elif possible_results[answer]:
            produceGameListFile(giantbomb_api_key, answer)
    except:
        return 0

    return 0

def getFilteredJSON(tw_key, console_id):
    active_games = getActiveGamesFromTwitch(tw_key)
    console_games = []
    filename = str(console_id) + "_games.json"
    with open('active_games.json','r') as f:
        active_games = json.load(f)
        
    with open(filename,'r') as f:
        console_games = json.load(f)
    
    
    results = filterActiveGamesByConsole(active_games,console_games)

    return results

def mainLoop():

    existing_platforms = checkExistingFiles()

    if existing_platforms:
        print("Existing platforms found.")
        print("")
        for platform in existing_platforms:
            print("{}: {}".format(existing_platforms[platform],platform))
    print("Add new platform: 0")
    print("")
    answer = input("Input a number: ")
    
    try:
        if answer == "0":
            addNewPlatform()
        elif existing_platforms[answer]:
            filename = answer + "_filtered.json"
            results = getFilteredJSON(twitch_api_key, answer)
            with open(filename,'w') as f:
                f.write(json.dumps(results, indent=4, sort_keys=True))
    except:
        return 1
    return 0

def main():
    arguments = sys.argv
    if len(arguments) > 1:
        if arguments[1] == "reset":
            resetFiles()
            sys.exit(0)
    
    mainLoop()
    sys.exit(0)

main()
