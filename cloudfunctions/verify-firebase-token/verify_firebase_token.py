import google.oauth2.id_token
from google.auth.transport import requests


def verify_firebase_token(request):
    """"""
    token = request.args.get('token')

    if token:
        try:
            # Verify the token against the Firebase Auth API. This example
            # verifies the token on each page load
            claims = google.oauth2.id_token.verify_firebase_token(
                token, requests.Request())

            return (claims, 200)
        except Exception as e:
            # This will be raised if the token is expired or any other
            # verification checks fail.
            return ({"error": str(e)}, 400)

    return ({"error": "No Token Parameter Passed To URL"}, 400)
