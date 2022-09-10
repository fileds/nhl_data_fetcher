from pprint import pprint
import json
import requests

response = requests.get("https://statsapi.web.nhl.com/api/v1/teams/1?expand=team.roster")
data = response.json()
pprint(data)
