from flask import Flask, render_template, request
from score import get_games
from waitress import serve

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/score')
def get_score():
    date = request.args.get('date')
    game_data = get_games(date)

    games_list = []
    ngames = len(game_data["data"])
    for i in range(ngames):
        team1 = game_data["data"][i]["home_team"]["full_name"]
        team2 = game_data["data"][i]["visitor_team"]["full_name"]
        score1 = game_data["data"][i]["home_team_score"]
        score2 = game_data["data"][i]["visitor_team_score"]
        game = {"team1": team1, "score1": score1, "team2": team2, "score2": score2}
        games_list.append(game)

    return render_template(
        "score.html",
        ngames = ngames,
        title = date,
        games = games_list
    )

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port = 8000)