from flask import Flask, render_template, request
from score import get_games
from waitress import serve
from datetime import date

app = Flask(__name__)

@app.route('/')
@app.route('/index')

@app.route('/score')
def get_score():
    today_date = date.today()
    game_data = get_games(today_date)

    games_list = []
    ngames = len(game_data["data"])
    for i in range(ngames):
        team1 = game_data["data"][i]["home_team"]["full_name"]
        team2 = game_data["data"][i]["visitor_team"]["full_name"]
        score1 = game_data["data"][i]["home_team_score"]
        score2 = game_data["data"][i]["visitor_team_score"]
        logo1 = f'/static/logos/{team1}.png'
        logo2 = f'/static/logos/{team2}.png'
        status = game_data["data"][i]["status"]
        if len(status) > 8:
            status = "Not Started"
        game = {"team1": team1, "score1": score1, "team2": team2, "score2": score2, "logo1": logo1, "logo2": logo2, "status": status}
        games_list.append(game)

    return render_template(
        "score.html",
        ngames = ngames,
        title = date,
        games = games_list
    )

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port = 8000)