import requests
user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
url = '''
https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=63.43&lon=10.39
''' #Split url into several lines to fit code in latex
r = requests.get(url, headers=user_agent) 
print(r.text)
