import requests


def service_layer(request):
    key = request.args.get("key")
    value = request.args.get("value")
    db = request.args.get("db")

    # Insert cloud function URL below
    # e.g https://europe-west1-ad-2021-03.cloudfunctions.net
    url = f"URL HERE" + f"/get-all-games-mesh-layer-{db}"

    if key and value:
        url += f"?key={key}&value={value}"

    resp = requests.get(url)

    return (resp.json(), resp.status_code)
