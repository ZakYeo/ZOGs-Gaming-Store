from flask import Flask, redirect, url_for, request, render_template, session
from flask_bootstrap import Bootstrap5
from os import urandom
from google.cloud import datastore
#import requests
from google.auth.transport import requests 

import google.oauth2.id_token

firebase_request_adapter = requests.Request()
datastore_client = datastore.Client(project="ad-2021-03")

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = urandom(12)
Bootstrap5(app)


@app.route("/store", defaults={'email': "Please Log In"})
@app.route('/store/<email>', methods=["GET", "POST"])
def store(email):
    query = datastore_client.query(kind="Item")
    items = list(query.fetch())
    #id_token = request.cookies.get("token")
    #claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
    #if(is_logged_in()):
    #    username = session["logged_in"]
    #else:
    #    username = ""
    claims = check_firebase_login()
    if(claims): # User is logged in
        email = claims["email"]

    return render_template("main_store_page.html", items=items)


@app.route("/")
def home():
    return redirect(url_for("store"))


@app.route('/login', methods=['POST', 'GET'])
def login():
    email = ""

    claims = check_firebase_login()
    if(claims): # User is logged in
        email = claims["email"]
        return redirect(url_for("store", email=email))
    else: # User is not logged in
        return render_template('login.html')   


    #if request.method == 'POST':
    #    user = request.form['username']
    #    password = request.form['password']
    #    if(user == "admin" and password == "admin"):
    #        session["logged_in"] = user
    #        return redirect(url_for("store"))
    #    else:
    #        return render_template('login.html')
    #else:
    #    if(is_logged_in()):
    #        return redirect(url_for("store"))
    #    else:
    #        return render_template('login.html')


@app.route("/logout")
def logout():
    if(is_logged_in()):
        del session['logged_in']
    return redirect(url_for("store"))


def is_logged_in():
    try:
        _ = session["logged_in"]
        return True
    except KeyError:
        return False

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
            pass # Continue, return None later

    return None


if __name__ == '__main__':
    app.run(debug=True)
