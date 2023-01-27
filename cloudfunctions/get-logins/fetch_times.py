from google.cloud import datastore
from json import dumps


def fetch_times(request):
    limit = request.args.get('limit')
    try:
        limit = int(limit)
    except (ValueError, TypeError) as e:
        return ({"error": str(e)}, 400)

    datastore_client = datastore.Client(project="")  # Insert project here
    query = datastore_client.query(kind='login')
    query.order = ['-timestamp']
    times = query.fetch(limit=limit)

    return ({count: dict(time) for count, time in enumerate(times)}, 200)
