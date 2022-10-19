from flask import Flask, redirect, url_for, request, render_template, session, flash
from flask_bootstrap import Bootstrap5
import os
from datetime import datetime
from google.cloud import datastore

datastore_client = datastore.Client(project="ad-2021-03")

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.urandom(12)
Bootstrap5(app)


@app.route("/")
def home():
    if not session.get("logged_in"):
        return render_template('login.html')
    else:
        return "You're logged in"


@app.route('/success/<name>')
def success(name):
    if(is_logged_in()):
        query = datastore_client.query(kind="Item")
        items = list(query.fetch())
        return render_template("logged_in.html", name=name, items=items)
    else:
        return home()


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        if(user == "admin" and password == "admin"):
            session["logged_in"] = user
            return redirect(url_for('success', name=user))
        else:
            return home()
    else:
        if(is_logged_in()):
            return redirect(url_for('success', name=session["logged_in"]))
        else:
            return render_template('login.html')


@app.route("/logout")
def logout():
    session['logged_in'] = None
    return home()


def is_logged_in():
    try:
        _ = session["logged_in"]
        return True
    except KeyError:
        return False


if __name__ == '__main__':
    app.run(debug=True)
