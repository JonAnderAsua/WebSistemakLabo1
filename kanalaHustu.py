import json

import requests
import urllib

method = 'GET'
uri = "https://api.thingspeak.com/channels.json?api_key=KJ0S8T8BGX7C3TMN"  # Ateratzeko form-en begiratu
erantzun = requests.request(method, uri, allow_redirects=False)

zerrenda = json.loads(erantzun.content)
print(zerrenda[1]['id'])
