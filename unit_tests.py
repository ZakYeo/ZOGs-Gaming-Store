from main import app
from pymongo import MongoClient

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TESTING FLASK ENDPOINT STATUS CODES


def test_root_redirect_status(client):
    response = client.get("/")
    # data = response.data.decode()
    assert response.status_code == 302  # "Moved Temporarily" (redirect)


def test_store_status(client):
    response = client.get("/store/")
    assert response.status_code == 200  # "OK" (redirect)
    response = client.get("/store/1/")
    assert response.status_code == 200  # "OK" (redirect)
    response = client.post("/store/1/update/", json={
        "token": "token",
        "filter_key": "",
        "filter_value": "",
        "new_key": "",
        "new_value": ""
    })
    assert response.status_code == 400  # Since invalid token passed, expect 400
    #response = client.post("/store/1/delete/", json={})
    # assert response.status_code == 400  # Since invalid token passed, expect 400


def test_login_status(client):
    response = client.get("/login")
    assert response.status_code == 200


def test_login_status(client):
    response = client.get("/signup")
    assert response.status_code == 200


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TESTING FLASK ENDPOINT HTML CONTENTS

def test_store_html(client):
    response = client.get("/store/")
    cluster = MongoClient(
        "mongodb+srv://ZakAdvancedDev:eMdjKMHKfsawLrT4@cluster0.9xwlxzr.mongodb.net/?retryWrites=true&w=majority")

    assert any([game["name"] in response.data.decode()
                for game in cluster["GameStore"]["Games"].find()])


def test_store_html(client):
    cluster = MongoClient(
        "mongodb+srv://ZakAdvancedDev:eMdjKMHKfsawLrT4@cluster0.9xwlxzr.mongodb.net/?retryWrites=true&w=majority")

    assert any([game["name"] and str(game["price"]) in
                client.get(f"/store/{game['id_']}",
                           follow_redirects=True).data.decode()
                for game in cluster["GameStore"]["Games"].find()])


def test_login_html(client):
    response = client.get("/login")

    assert 'login' in response.data.decode().lower()


def test_signup_html(client):
    response = client.get("/signup")

    assert 'signup' in response.data.decode().lower()


if __name__ == '__main__':
    test_client = app.test_client()
    test_root_redirect_status(test_client)
    test_store_status(test_client)
    test_login_status(test_client)
    test_login_status(test_client)
    test_store_html(test_client)
    test_login_html(test_client)
    test_signup_html(test_client)
