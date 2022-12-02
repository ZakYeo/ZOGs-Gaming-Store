from flask import Flask, redirect, url_for, request, render_template, session
from flask_bootstrap import Bootstrap5
from os import urandom
from google.cloud import datastore
import requests
from pymongo import MongoClient
from google.auth.transport import requests as grequests

import google.oauth2.id_token

firebase_request_adapter = grequests.Request()
datastore_client = datastore.Client(project="ad-2021-03")

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = urandom(12)
Bootstrap5(app)

cluster = MongoClient(
    "mongodb+srv://ZakAdvancedDev:eMdjKMHKfsawLrT4@cluster0.9xwlxzr.mongodb.net/?retryWrites=true&w=majority")


@app.route("/store", defaults={'email': "Please Log In"})
@app.route('/store/<email>', methods=["GET", "POST"])
def store(email):
    query = datastore_client.query(kind="Item")
    items = list(query.fetch())

    return render_template("main_store_page.html", items=items)


@app.route("/")
def home():
    return redirect(url_for("store"))


@app.route('/login', methods=['POST', 'GET'])
def login():

    claims = check_firebase_login()
    if(claims):  # User is logged in
        email = claims["email"]
        return redirect(url_for("store", email=email))
    else:  # User is not logged in
        return render_template('login.html')


def check_firebase_login():
    id_token = request.cookies.get("token")
    if id_token:
        try:
            # Verify the token against the Firebase Auth API. This example
            # verifies the token on each page load
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)

            return claims

        except Exception:
            # This will be raised if the token is expired or any other
            # verification checks fail.
            pass  # Continue, return None later

    return None


def get_all_games():
    url = "https://europe-west1-ad-2021-03.cloudfunctions.net/get-all-games"

    resp = requests.get(url)

    return resp.json()


if __name__ == '__main__':
    app.run(debug=True)
