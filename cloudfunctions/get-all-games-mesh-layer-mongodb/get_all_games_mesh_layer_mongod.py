from json import dumps
from pymongo import MongoClient, errors


def get_all_games_mesh_layer_mongodb(request):
    key = request.args.get('key')
    value = request.args.get('value')
    try:
        cluster = MongoClient(
            "")  # mongodb+srv:// URL to MongoDB here
    except errors.PyMongoError as e:
        return({"error": str(e)}, 503)  # 503 Service Unavailable

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
        try:
            return_val = {count+1: game for count, game in enumerate(
                cluster["GameStore"]["Games"].find({key: value}))}
        except errors.PyMongoError as e:
            return({"error": str(e)}, 503)  # 503 Service Unavailable
    else:
        try:
            return_val = {count+1: game for count, game in enumerate(
                cluster["GameStore"]["Games"].find())}
        except errors.PyMongoError as e:
            return({"error": str(e)}, 503)  # 503 Service Unavailable
    for k, v in return_val.items():
        del v["_id"]

    return (return_val, 200)
