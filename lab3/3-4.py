import requests
user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

places = {
    "Trondheim": {"lat": 63.43, "lon": 10.39},
    "Oslo": {"lat": 59.91, "lon": 10.75},
    "Bergen": {"lat": 60.39, "lon": 5.32},
    "Avaldsnes": {"lat": 59.35, "lon": 5.27},
    "Tromsø": {"lat": 69.64, "lon": 18.95},
}

def get_air_temp(lat, lon):
    url = 'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={}&lon={}'.format(lat, lon)
    r = requests.get(url, headers=user_agent)
    return r.json()['properties']['timeseries'][0]['data']['instant']['details']['air_temperature']
    
def get_air_temp_2(place):
    return get_air_temp(places[place]['lat'], places[place]['lon'])

print("Trondheim temp by coords:",get_air_temp(places["Trondheim"]["lat"], places["Trondheim"]["lon"]))
for place in places:
    print(place,"temp by name:", get_air_temp_2(place))