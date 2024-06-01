from flask import Flask, request, render_template, redirect, url_for, session
from score import get_games
from flask_socketio import SocketIO, join_room, leave_room, send
from datetime import datetime
import pytz
import os

app = Flask(__name__)
app_key = os.getenv("SECRET_KEY")
app.config["SECRET_KEY"] = app_key
socketio = SocketIO(app, async_mode='gevent')

# A mock database to persist data
rooms = {}

@app.route('/', methods=["GET", "POST"])
def score():
    session.clear()
    today_date = datetime.now(pytz.timezone("US/Arizona")).date()
    today_date = '2024-02-24'
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
        if chatcode not in rooms:
            room_code = chatcode
            new_room = {
                    'members': 0,
                    'messages': []
                }
            rooms[room_code] = new_room
        if len(status) > 8:
            status = "Not Started"
        game = {"team1": team1, "score1": score1, "team2": team2, "score2": score2, "logo1": logo1, "logo2": logo2, "status": status, "chatcode": chatcode}
        games_list.append(game)
    if request.method == "POST":
        code = request.form.get('code')
        name = request.form.get('name')
        if not name:
            return render_template('score.html', error="Name is required", ngames = ngames, games = games_list)
        if code not in rooms:
            room_code = code
            new_room = {
                    'members': 0,
                    'messages': []
                }
            rooms[room_code] = new_room
        session['room'] = code
        session['name'] = name
        return redirect(url_for('room'))
    else:
        return render_template(
            "score.html",
            ngames = ngames,
            games = games_list,
        )

@app.route('/room')
def room():
    room = session.get('room')
    name = session.get('name')
    messages = rooms[room]['messages']
    return render_template('room.html', room=room, user=name, messages=messages)

@socketio.on('connect')
def handle_connect():
    name = session.get('name')
    room = session.get('room')
    join_room(room)
    send({
        "sender": "",
        "message": f"{name} has entered the chat"
    }, to=room)
    rooms[room]["members"] += 1

@socketio.on('message')
def handle_message(payload):
    room = session.get('room')
    name = session.get('name')
    if room not in rooms:
        return
    message = {
        "sender": name,
        "message": payload["message"]
    }
    send(message, to=room)
    rooms[room]["messages"].append(message)

@socketio.on('disconnect')
def handle_disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)
    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
        send({
        "message": f"{name} has left the chat",
        "sender": ""
    }, to=room)

if __name__ == "__main__":
    socketio.run(app, debug=True)
