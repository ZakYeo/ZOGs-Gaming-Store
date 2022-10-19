from flask import Flask, redirect, url_for, request, render_template, session, flash
from flask_bootstrap import Bootstrap5
import os
from datetime import datetime
from google.cloud import datastore

datastore_client = datastore.Client(project="ad-2021-03")

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.urandom(12)
Bootstrap5(app)


@app.route("/store")
def store():
    query = datastore_client.query(kind="Item")
    items = list(query.fetch())
    if(is_logged_in()):
        username = session["logged_in"]
    else:
        username = ""

    return render_template("main_store_page.html", name=username, items=items)


@app.route("/")
def home():
    return redirect(url_for("store"))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        if(user == "admin" and password == "admin"):
            session["logged_in"] = user
            return redirect(url_for("store"))
        else:
            return render_template('login.html')
    else:
        if(is_logged_in()):
            return redirect(url_for("store"))
        else:
            return render_template('login.html')


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


if __name__ == '__main__':
    app.run(debug=True)
