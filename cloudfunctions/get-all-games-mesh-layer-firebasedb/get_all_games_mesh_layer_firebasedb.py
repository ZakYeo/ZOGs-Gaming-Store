
from json import loads
from firebase_admin import credentials
import firebase_admin
from firebase_admin import db
from firebase_admin.exceptions import FirebaseError


def get_all_games_mesh_layer_firebasedb(request):
    key = request.args.get('key')
    value = request.args.get('value')
    firebase_config = loads("""""")  # Place firebase config here
    cred = credentials.Certificate(firebase_config)
    try:
        default_app = firebase_admin.initialize_app(cred, {
            'databaseURL': ''  # Database URL here
        })

    except ValueError:
        pass  # App is already initialized!
    except FirebaseError as e:
        # Server error! Could be connection, corruption, etc.
        return ({"error": str(e)}, 503)

    ref = db.reference("/GameStore/Games/").get()
    if key is None or value is None:
        return ({count+1: game for count, game in enumerate(ref)}, 200)
    else:
        if(key and value):
            if(key.lower() == "price"):
                try:
                    value = float(value)
                except ValueError:
                    return ({"error": "Please ensure price is a decimal value"}, 400)
            elif(key.lower() == "id_"):
                try:
                    value = int(value)
                except ValueError:
                    return ({"error": "Please ensure id is an integer value"}, 400)
        return_dict = {}
        count = 1
        for game in ref:
            if(game[key] == value):
                return_dict[count] = game
                count += 1

        return (return_dict, 200)
