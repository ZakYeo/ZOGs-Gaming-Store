from pymongo import MongoClient
import requests


def update_game(request):
    token = request.args.get('token')
    filter_key = request.args.get('filter_key')
    filter_value = request.args.get('filter_value')
    new_key = request.args.get('new_key')
    new_value = request.args.get('new_value')

    if token is None:
        return ({"error": "Please specify a token"}, 400)
    if filter_key is None or filter_value is None or new_key is None or new_value is None:
        return ({"error": "Please specify filter_key , filter_value, new_key and new_value parameters"}, 400)

    cluster = MongoClient(
        "")  # mongodb+srv:// URL to MongoDB here

    # Insert cloud function URL below
    # e.g https://europe-west1-ad-2021-03.cloudfunctions.net
    url = f"URL HERE" + f"/verify-firebase-token?token={token}"

    resp = requests.get(url)

    if resp.status_code != 200:
        # Token is not verified , do not proceed
        return (resp.json(), resp.status_code)

    if(filter_key.lower() == "price"):
        try:
            filter_value = float(filter_value)
        except ValueError:
            return ({"error": "Please ensure price is a decimal value"}, 400)
    elif(filter_key.lower() == "id_"):
        try:
            filter_value = int(filter_value)
        except ValueError:
            return ({"error": "Please ensure id is an integer value"}, 400)

    if(new_key.lower() == "price"):
        try:
            new_value = float(new_value)
        except ValueError:
            return ({"error": "Please ensure price is a decimal value"}, 400)
    elif(new_key.lower() == "id_"):
        try:
            new_value = int(new_value)
        except ValueError:
            return ({"error": "Please ensure id is an integer value"}, 400)

    cluster["GameStore"]["Games"].update_one(
        {filter_key: filter_value}, {"$set": {new_key: new_value}})

    return (
        {"success": f"Updated {new_key} to {new_value}."}, 200
    )
