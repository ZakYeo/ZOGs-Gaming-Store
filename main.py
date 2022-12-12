from flask import Flask, redirect, url_for, request, render_template
from flask_bootstrap import Bootstrap5
from os import urandom
from google.cloud import datastore
import requests
from time import sleep
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
    """ Root page for the Online GameStore

    Arguments:
    game -- [optional] The 'id_' attribute of the game to display
            If supplied, will return a detailed screen of that game
            If no game is given, or the value of game is invalid, will return the root store

    Returns:
    Returns either the main_store_page or game_details html pages for rendering            
    """

    if not game:  # Render all games
        resp = handle_game_request()
        items = []
        if resp:
            games = resp.json()
            items = list(games.values())
            # sort games alphabetically by name
            items = sorted(items, key=lambda item: item["name"])
        # Now render the html
        return render_template("main_store_page.html", items=items)
    else:  # Render a singular game
        resp = handle_game_request("id_", int(game))
        if(resp is None or len(resp.json()) == 0):  # Game not found
            return redirect(url_for("store"))

        if request.method == 'POST':  # Admin is updating game via POST
            json = request.get_json()
            filter_key = json["filter_key"]
            filter_value = json["filter_value"]
            new_key = json["new_key"]
            new_value = json["new_value"]
            resp = update_game(request.cookies.get("token"), filter_key,
                               filter_value, new_key, new_value)

            return (resp.json(), resp.status_code)  # Return response
        # Now render game
        return render_template("game_details.html", game=resp.json()["1"])


@ app.route("/")
def home():
    """Redirect root routing to the store page at this endpoint"""
    return redirect(url_for("store"))


@ app.route('/login', methods=['GET'])
@ app.route('/login/record', methods=['POST'])
def login():
    """Renders the login.html at this endpoint"""
    return render_template('login.html')


@ app.route("/admin/", methods=["GET"])
def admin():
    """ Endpoint to check if a user has administrative permissions or not

    It does this by verifying the user's token cookie and checking against the database

    Returns:
        1 or 0 for administrator or not   
        HTTP status code 200 if successful        
    """

    claims = check_firebase_login(request.cookies.get("token"))
    admin = 0
    if claims:
        resp = is_administrator(claims["user_id"])
        if resp["administrator"] == 1:  # User is an administrator
            admin = 1

    return ({"administrator": admin}, 200)


@ app.route("/times/<limit>", methods=["GET"])
def times(limit):
    """ Endpoint to fetch the last x amount of entries in the Google Datastore

    This is used as a tool for administrators to check the logs / recent activity

    Arguments:
        limit -- The amount of entries to fetch

    Returns:
        json object of the recent Google Datastore activity
        HTTP status code 200 if successful       
    """
    return (fetch_times(limit), 200)


@ app.route("/record", methods=["POST"])
def record():
    """ Records the POSTed json into the Google Datastore
    Intended use is for logging purposes to display to admins.
    e.g recording a login
    """
    data = request.json
    entity = datastore.Entity(key=datastore_client.key('login'))
    claims = check_firebase_login(request.cookies.get("token"))
    if data["type"] == "login":  # Record a login from any user
        entity.update({"timestamp": datetime.now(),
                       "user_id": claims["user_id"],
                       "email": claims["email"]
                       })
    datastore_client.put(entity)


def handle_game_request(key=None, value=None):
    """ Queries the database for games

    Will first attempt to pull from Mongodb
    If the connection was unsuccessful (password change, data corruption, connection unavailable etc),
    then it will attempt to access the secondary backup database from Firebase's Realtime Database

    Uses exponential backoff at a rate of 2^attempts 
    and retries both databases if they both return unsuccessful
    At 5 attempts, will give up

    Arguments:
        key   -- The key of the data to query (used to narrow search)
        value -- The value of the data to query (used to narrow search)

    Returns:
        HTTP response containing json response and HTTP status code       
    """
    code = 503
    attempts = 0
    while code == 503 or code == 500:  # 503 = Service Unavailable, 500 = internal server error

        sleep(attempts**2)  # Exponential backoff

        if key and value:
            resp = get_all_games("mongodb",
                                 key, value)  # Grab from Mongodb
        else:
            resp = get_all_games("mongodb")
        code = resp.status_code
        if(code == 503 or code == 500):  # Database busy / offline / corrupt etc, try backup DB
            if key and value:
                resp = get_all_games("firebasedb",
                                     key, value)  # Grab from firebasedb
            else:
                resp = get_all_games("firebasedb")
            code = resp.status_code
        elif(code == 400):  # Clientside error, bad request
            return None

        attempts += 1
        if attempts == 5:
            # After 5 attempts just end
            return None
    return resp


def fetch_times(limit):
    """Calls get-logins cloud function to return the json response of Google Datastore"""
    url = f"{BASE_URL}/get-logins?limit={limit}"

    resp = requests.get(url)

    return resp.json()


def check_firebase_login(token=""):
    """Calls verify-firebase-token cloud function

    Intended to be used to verify if a firebase token is valid

    Arguments:
        token -- The token to check against

    Returns:
        Json of the response if successful
        else None
    """
    url = f"{BASE_URL}/verify-firebase-token?token={token}"

    resp = requests.get(url)

    if resp.status_code == 200:
        return resp.json()
    else:
        return None


def update_game(token=None, filter_key=None, filter_value=None, new_key=None, new_value=None):
    """ Calls a cloud function to update a game entry in the databases

    Arguments [Optional]:
        token        -- The token for verification, only administrators can update a database entry
        filter_key   -- The key of the data to query (used to narrow search)
        filter_value -- The value of the data to query (used to narrow search)
        new_key      -- The key of the new data to update
        new_value    -- The new value to update

    Returns:
        Response object of the cloud function, contains json and status code
    """
    url = f"{BASE_URL}/update-game?token={token}&filter_key={filter_key}&filter_value={filter_value}&new_key={new_key}&new_value={new_value}"

    resp = requests.get(url)

    return resp


def is_administrator(user_id):
    """ Calls the is-administrator cloud function

    Arguments:
        user_id -- The user_id of the user's Firestore authentication account

    Returns:
        json of the response containing 0 for non-admin and 1 for admin
    """

    url = f"{BASE_URL}/is-administrator?user_id={user_id}"

    resp = requests.get(url)

    return resp.json()


def get_all_games(db, key=None, value=None):
    """ Calls the get-all-games-service-layer cloud function

    Arguments:
        db    -- The database to query, e.g 'mongodb' or 'firestoredb'
        key   -- [optional] The key of the data to query (used to narrow search)
        value -- [optional] The value of the data to query (used to narrow search)

    Returns:
        response object of the cloud function containing the games from a database
    """

    url = f"{BASE_URL}/get-all-games-service-layer?db={db}"

    if key and value:
        url += f"&key={key}&value={value}"

    resp = requests.get(url)

    return resp


if __name__ == '__main__':
    app.run(debug=True)
