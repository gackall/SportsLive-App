import re
from urllib import response
from dotenv import load_dotenv
from pprint import pprint
import requests
import os
import urllib.request
import json

load_dotenv()


api_key = os.getenv("API_KEY")

def get_games(date = "2024-05-09"):
    api_url = f'https://api.balldontlie.io/v1/games?dates[]={date}'

    headers = {
    'Authorization': api_key 
    }
    req = urllib.request.Request(api_url, headers=headers)
    response = urllib.request.urlopen(req)
    json_res = json.loads(response.read())
    return json_res

#    if response.status_code == 200:
#        data = response.json()
#        return data
#    else:
#        return ("Error:", response.status_code)

if __name__ == '__main__':
    print('\n*** Get Games Scores *** \n')
    date = input('\n Please select a date: ')
    game_data = get_games(date)
    ngames = len(game_data["data"])
    games_list = []
    for i in range(ngames):
        team1 = game_data["data"][i]["home_team"]["full_name"]
        team2 = game_data["data"][i]["visitor_team"]["full_name"]
        score1 = game_data["data"][i]["home_team_score"]
        score2 = game_data["data"][i]["visitor_team_score"]
        status = game_data["data"][i]["status"]
        game = {"team1": team1, "score1": score1, "team2": team2, "score2": score2}
        games_list.append(game)
    print("\n")
    pprint(game_data["data"][0])
