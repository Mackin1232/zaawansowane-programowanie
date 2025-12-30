import requests
import json
from api_key import API_KEY
from db.modele import Airport
from Aplikacja import app

## API_KEY przechowuję w pliku api_key.py na swoim kompie, wolałbym nie wrzucać na gita bo jest ryzyko że wycieknie
## Jeśli chcecie się tym pobawić to napiszcie do mnie, dam wam klucz -- Maciek


with app.app_context():
  lotniska = [a.to_dict() for a in Airport.query.all()]
  kody = [l['iata'] for l in lotniska]
  for airport in kody:
    # loty wylatujące z lotniska
    params = {
      'api_key': API_KEY,
      'dep_iata': airport,
    }
    result = requests.get("https://airlabs.co/api/v9/schedules", params=params)
    response = result.json()['response']
    response = sorted(response, key=lambda item: item['dep_time'])

    with open(f"./db/base_data/api_data/flights_{airport}_departures.json", 'w') as file: 
        json.dump(response,file,indent=4) # np. loty wylatujące z Katowic zapisane w pliku api_data/flights_KTW_departures.json
    
    # loty przylatujące do lotniska
    params = {
      'api_key': API_KEY,
      'arr_iata': airport,
    }
    result = requests.get("https://airlabs.co/api/v9/schedules", params=params)
    response = result.json()['response']
    response = sorted(response, key=lambda item: item['dep_time'])

    with open(f"./db/base_data/api_data/flights_{airport}_arrivals.json", 'w') as file: 
        json.dump(response,file,indent=4) # np. loty przylatujące do Katowic zapisane w pliku api_data/flights_KTW_arrivals.json
