from flask import Flask, redirect, url_for, request, render_template, session
from flask_bootstrap import Bootstrap5
from os import urandom
from google.cloud import datastore
import requests
from pymongo import MongoClient
from google.auth.transport import requests as grequests

firebase_request_adapter = grequests.Request()
datastore_client = datastore.Client(project="ad-2021-03")
BASE_URL = "https://europe-west1-ad-2021-03.cloudfunctions.net"

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = urandom(12)
Bootstrap5(app)

cluster = MongoClient(
    "mongodb+srv://ZakAdvancedDev:eMdjKMHKfsawLrT4@cluster0.9xwlxzr.mongodb.net/?retryWrites=true&w=majority")


@app.route("/store")
def store():
    games = get_games()
    items = list(games.values())
    return render_template("main_store_page.html", items=items)


@app.route("/")
def home():
    return redirect(url_for("store"))


@app.route('/login', methods=['POST', 'GET'])
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

    return resp.json()


def get_games(key=None, value=None):

    url = f"{BASE_URL}/get-all-games"

    if(key and value):
        url += f"?key={key}&value={value}"

    resp = requests.get(url)

    return resp.json()


if __name__ == '__main__':
    app.run(debug=True)
