from pymongo import MongoClient, errors
from random import randint

# Entry Point


def add_game(request):
    name = request.args.get("name")
    price = request.args.get("price")
    if name is None or price is None:
        return ({"error": "Please specify name & price"}, 400)

    try:
        cluster = MongoClient(
            "")  # mongodb+srv:// URL to MongoDB here
    except errors.PyMongoError as e:
        return({"error": str(e)}, 503)  # 503 Service Unavailable
    try:
        price = float(price)
    except ValueError:
        return ({"error": "Please ensure price is a decimal value"}, 400)

    try:
        id_ = randint(10000, 99999)
        _ = cluster["GameStore"]["Games"].insert_one({"name": f"{name}", "price": price, "id_": id_,
                                                      "image": "https://res.cloudinary.com/dhujezr6s/image/upload/v1671103440/placeholder_x80qox.png", "desc_brief": " ",
                                                      "desc_long": " "})
    except errors.PyMongoError as e:
        return({"error": str(e)}, 503)  # 503 Service Unavailable

    return ({"success": "Inserted game", "id_": id_}, 200)
