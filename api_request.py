import requests
import json
from api_key import API_KEY

## API_KEY przechowuję w pliku api_key.py na swoim kompie, wolałbym nie wrzucać na gita bo jest ryzyko że wycieknie
## Jeśli chcecie się tym pobawić to napiszcie do mnie, dam wam klucz -- Maciek

airport = "POZ"
params = {
  'api_key': API_KEY,
  'dep_iata': airport,
}
result = requests.get("https://airlabs.co/api/v9/schedules", params=params)
response = result.json()['response']
response = sorted(response, key=lambda item: item['dep_time'])

with open(f"./api_data/flights_{airport}.json", 'w') as file: 
    json.dump(response,file,indent=4) # np. dla lotniska KTW dane zapisane w pliku api_data/flights_KTW.json
