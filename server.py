from flask import Flask, render_template, request
from score import get_games
from waitress import serve
from datetime import datetime
import pytz

app = Flask(__name__)

@app.route('/')
@app.route('/index')

@app.route('/score')
def get_score():
    today_date = datetime.now(pytz.timezone("US/Arizona")).date()
    game_data = get_games(today_date)

    games_list = []
    ngames = len(game_data["data"])
    for i in range(ngames):
        team1 = game_data["data"][i]["home_team"]["full_name"]
        abbrev1 = game_data["data"][i]["home_team"]["abbreviation"]
        team2 = game_data["data"][i]["visitor_team"]["full_name"]
        abbrev2 = game_data["data"][i]["visitor_team"]["abbreviation"]
        score1 = game_data["data"][i]["home_team_score"]
        score2 = game_data["data"][i]["visitor_team_score"]
        logo1 = f'/static/logos/{team1}.png'
        logo2 = f'/static/logos/{team2}.png'
        status = game_data["data"][i]["status"]
        chatcode = abbrev1 + abbrev2
        if len(status) > 8:
            status = "Not Started"
        game = {"team1": team1, "score1": score1, "team2": team2, "score2": score2, "logo1": logo1, "logo2": logo2, "status": status, "chatcode": chatcode}
        games_list.append(game)

    return render_template(
        "score.html",
        ngames = ngames,
        games = games_list
    )

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port = 8000)