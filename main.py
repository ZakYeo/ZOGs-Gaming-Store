from flask import Flask, redirect, url_for, request, render_template
from flask_bootstrap import Bootstrap5
from os import urandom
from google.cloud import datastore
import requests


datastore_client = datastore.Client(project="ad-2021-03")
BASE_URL = "https://europe-west1-ad-2021-03.cloudfunctions.net"

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = urandom(12)
Bootstrap5(app)


@app.route("/store", defaults={"game": ""})
@app.route("/store/", defaults={"game": ""})
@app.route("/store/<game>")
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
        except ValueError and KeyError:
            return redirect(url_for("store"))

        return render_template("game_details.html", game=game)


@ app.route("/")
def home():
    return redirect(url_for("store"))


@ app.route('/login', methods=['POST', 'GET'])
def login():

    claims = check_firebase_login(request.cookies.get("token"))
    if(claims):  # User is logged in
        email = claims["email"]
        return redirect(url_for("store", email=email))
    else:  # User is not logged in
        return render_template('login.html')


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


if __name__ == '__main__':
    app.run(debug=True)
