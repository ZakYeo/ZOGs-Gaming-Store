from flask import Flask, redirect, url_for, request, render_template
from flask_bootstrap import Bootstrap5
from os import urandom
from google.cloud import datastore
import requests
from datetime import datetime


datastore_client = datastore.Client(project="ad-2021-03")
BASE_URL = "https://europe-west1-ad-2021-03.cloudfunctions.net"
app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = urandom(12)
Bootstrap5(app)


@app.route("/store", defaults={"game": ""})
@app.route("/store/", defaults={"game": ""})
@app.route("/store/<game>/")
@app.route("/store/<game>/update/", methods=['POST'])
def store(game):

    if not game:
        games = get_games()
        items = list(games.values())
        # sort games alphabetically by name
        items = sorted(items, key=lambda item: item["name"])
        return render_template("main_store_page.html", items=items)
    else:
        try:
            game = get_games("id_", int(game))["1"]  # Get specific game
        except (ValueError, KeyError) as _:
            return redirect(url_for("store"))

        if request.method == 'POST':
            json = request.get_json()
            filter_key = json["filter_key"]
            filter_value = json["filter_value"]
            new_key = json["new_key"]
            new_value = json["new_value"]
            resp = update_game(request.cookies.get("token"), filter_key,
                               filter_value, new_key, new_value)

            return (resp.json(), resp.status_code)
        return render_template("game_details.html", game=game)


@ app.route("/")
def home():
    return redirect(url_for("store"))


@ app.route('/login', methods=['POST', 'GET'])
def login():

    claims = check_firebase_login(request.cookies.get("token"))
    if(claims):  # User is logged in
        if(request.method == "POST"):  # User is logging in, record
            record_login(datetime.now(), claims["user_id"], claims["email"])
        return redirect(url_for("store"))
    else:  # User is not logged in
        return render_template('login.html')


@ app.route("/admin/", methods=["GET"])
def admin():

    claims = check_firebase_login(request.cookies.get("token"))
    admin = 0
    if claims:
        resp = is_administrator(claims["user_id"])
        if resp["administrator"] == 1:
            admin = 1

    return ({"administrator": admin}, 200)


@ app.route("/times/<limit>", methods=["GET"])
def times(limit):
    return (fetch_times(limit), 200)


def record_login(time, user_id, email):
    entity = datastore.Entity(key=datastore_client.key('login'))
    entity.update({
        'timestamp': time,
        'user_id': user_id,
        'email': email
    })
    datastore_client.put(entity)


def fetch_times(limit):
    url = f"{BASE_URL}/get-logins?limit={limit}"

    resp = requests.get(url)

    return resp.json()


def check_firebase_login(token=""):
    url = f"{BASE_URL}/verify-firebase-token?token={token}"

    resp = requests.get(url)

    if resp.status_code == 200:
        return resp.json()
    else:
        return None


def get_games(key=None, value=None):

    url = f"{BASE_URL}/get-all-games"

    if(key and value):
        url += f"?key={key}&value={value}"

    resp = requests.get(url)

    return resp.json()


def update_game(token=None, filter_key=None, filter_value=None, new_key=None, new_value=None):
    url = f"{BASE_URL}/update-game?token={token}&filter_key={filter_key}&filter_value={filter_value}&new_key={new_key}&new_value={new_value}"

    resp = requests.get(url)

    return resp


def is_administrator(user_id):

    url = f"{BASE_URL}/is-administrator?user_id={user_id}"

    resp = requests.get(url)

    return resp.json()


if __name__ == '__main__':
    app.run(debug=True)
