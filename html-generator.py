import os
import json
import sys

def getActiveGamesDict():
    json_files = [x for x in os.listdir() if "_filtered.json" in x]
    active_games_dict = {}
    for json_file in json_files:
        with open(json_file, 'r') as f:
            active_games_dict[json_file.split("_")[0]] = json.loads(f.read())
    return active_games_dict

def getConsoleName(console_number):
    with open("platform_numbers.json") as f:
        data = json.loads(f.read())
        return data[str(console_number)]

def generateHeader(current_console_number, active_games_dict):
    resulting_html = """<div class="title-box-wrapper">\n"""
    generic_item = """<a class="title-box-item" href="!href!">!consoleName!</a>\n"""
    generic_selected_item = """<a class="title-box-item selected-item" href="!href!">!consoleName!</a>\n"""

    for console in active_games_dict:
        console_name = getConsoleName(console)
        current_item = ""
        if current_console_number == console:
            current_item = generic_selected_item
        else:
            current_item = generic_item
        current_item = current_item.replace("!href!","./" + console + ".html")
        current_item = current_item.replace("!consoleName!", console_name)
        resulting_html += current_item
    resulting_html += """</div>"""
    return resulting_html

def generateGame(game_data):
    game_name = game_data["name"]
    game_link = """https://www.twitch.tv/directory/game/""" + game_name
    box_art = game_data["box_art_url"].replace(r"{width}", "285").replace(r"{height}", "380")

    resulting_html = """<div class="game">\n"""
    resulting_html += """<a class="game-link" href=""" + "\"" + game_link + "\">\n"
    resulting_html += """<img class="game-image" src=""" + "\"" + box_art + "\"/>\n"
    resulting_html += """<div>""" + game_name + """</div>\n"""
    resulting_html += "</a>\n"
    resulting_html += """</div>\n"""
    return resulting_html

def generateGamesList(console_number, active_games_dict):
    resulting_html = """<div class="games-wrapper">\n"""
    for game in active_games_dict[console_number]:
        resulting_html += generateGame(game)
    resulting_html += """</div>\n"""
    return resulting_html

def generatePage(console_number, active_games_dict):
    resulting_html = """<!DOCTYPE html>
<html lang="en" >
<head>
<meta charset="UTF-8">
<title>Twitch Console Filter</title>
<meta property="og:title" content="Twitch Console Filter"/>
<meta property="og:description" content="Twitch Console Filter"/>
<link rel="icon" type="image/png" href="https://i.imgur.com/o9VHc6R.png">
<link rel="stylesheet" href="./style.css">

</head>
<body>
<!-- partial:index.partial.html -->
<div class="page-wrapper">"""
    resulting_html += generateHeader(console_number,active_games_dict)
    resulting_html += generateGamesList(console_number,active_games_dict)
    resulting_html += """ </div>
<!-- partial -->

</body>
</html>
"""
    return resulting_html

def buildAllPages():
    active_games_dict = getActiveGamesDict()
    for console in active_games_dict:
        html_file = "./html/" + console + ".html"
        with open(html_file, "w", encoding='utf-8', errors='ignore') as f:
            f.write(generatePage(console, active_games_dict))
    print ("All pages built.")

def main():
    buildAllPages()

main()