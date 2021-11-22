import requests
user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
url = 'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=63.43&lon=10.39'
r = requests.get(url, headers=user_agent)
print(r.text)