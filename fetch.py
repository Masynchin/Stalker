import os
from pprint import pprint

from pyyoutube import Client


client = Client(api_key=os.getenv("YOUTUBE_API_KEY"))
resp = client.channels.list(channel_id="UCwAwyYrh3HHfOFyy3zxQ4Mg", return_json=True)
pprint(resp)
