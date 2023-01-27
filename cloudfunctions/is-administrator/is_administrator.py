from json import dumps
from pymongo import MongoClient


def is_administrator(request):
    user_id = request.args.get('user_id')

    cluster = MongoClient(
        "")  # mongodb+srv:// URL to MongoDB here

    result = cluster["GameStore"]["Administrators"].find_one(
        {"user_id": user_id})

    if result:
        return ({"administrator": 1}, 200)  # 1 for Admin
    else:
        return ({"administrator": 0}, 200)  # 0 for not Admin
