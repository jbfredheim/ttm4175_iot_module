import requests
import json
from urllib.parse import quote, unquote


def dictionary_to_string(dictionary):
    return json.dumps(dictionary)

def encode_string_into_url(string):
    return quote(string)

def print_response(response):
    print('-------- Response --------')
    print('Status code: {}'.format(response.status_code))
    print('-------- Content--------')
    print(response.text)
    print('------------------------')

# example data
dictionary = {}
dictionary['temperature'] = 20.0
dictionary['sensor_name'] = 'kitchen'

# ... your code ...
dstr = dictionary_to_string(dictionary)
dstr_enc = encode_string_into_url(dstr)
print(dstr_enc)
response = requests.post('http://localhost:8023/?data={}'.format(dstr_enc))
print_response(response)