import requests
user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
url = 'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=63.43&lon=10.39'
r = requests.get(url, headers=user_agent) 
print("Most recent temperature: ", r.json()['properties']['timeseries'][0]['data']['instant']['details']['air_temperature'],"C")
for i in r.json()['properties']['timeseries']:
    print(f"{i['time']} : {i['data']['instant']['details']['air_temperature']}C")
