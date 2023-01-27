from pymongo import MongoClient, errors


def remove_game(request):
    id_ = request.args.get("id_")
    if id_ is None:
        return ({"error": "Please specify id_"}, 400)

    try:
        cluster = MongoClient(
            "")  # mongodb+srv:// URL to MongoDB here
    except errors.PyMongoError as e:
        return({"error": str(e)}, 503)  # 503 Service Unavailable
    try:
        id_ = float(id_)
    except ValueError:
        return ({"error": "Please ensure id_ is an integer value"}, 400)

    try:
        _ = cluster["GameStore"]["Games"].delete_one({"id_": id_})
    except errors.PyMongoError as e:
        return({"error": str(e)}, 503)  # 503 Service Unavailable

    return ({"success": "Deleted game", "id_": id_}, 200)
