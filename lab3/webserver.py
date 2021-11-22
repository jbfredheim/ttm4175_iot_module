from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import quote, unquote
import json
import socket
import requests

def get_yr_forecast(city):
    places = {
    "trondheim": {"lat": 63.43, "lon": 10.39},
    "oslo": {"lat": 59.91, "lon": 10.75},
    "bergen": {"lat": 60.39, "lon": 5.32},
    "avaldsnes": {"lat": 59.35, "lon": 5.27},
    "tromsø": {"lat": 69.64, "lon": 18.95},
    }
    
    def get_air_temp(lat, lon):
        url = 'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={}&lon={}'.format(lat, lon)
        r = requests.get(url, headers={'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        return r.json()['properties']['timeseries'][0]['data']['instant']['details']['air_temperature']
    
    def get_air_temp_2(place):
        place = place.lower()
        return get_air_temp(places[place]['lat'], places[place]['lon'])
    
    return get_air_temp_2(city)

def extract_json_string(string):
    start = string.find("{")
    stop = string.rfind("}")
    return string[start : stop + 1]


def get_ip_address():
    return socket.gethostbyname(socket.gethostname())


def dictionary_to_string(dictionary):
    return json.dumps(dictionary)


def json_string_to_dictionary(json_string):
    return json.loads(json_string)


def encode_string_into_url(string):
    return quote(string)


def decode_url_back_to_string(url_encoded_string):
    return unquote(url_encoded_string)


def string_to_unicode_bytes(string):
    return string.encode("utf-8")


class RequestHandler(BaseHTTPRequestHandler):
    def store_data(self, name, data):
        if not hasattr(self.server, "data"):
            self.server.data = {}
        self.server.data[name] = data

    def load_data(self, name):
        if hasattr(self.server, "data"):
            if name in self.server.data:
                return self.server.data[name]
        return None

    def do_GET(self):
        # Phase 1: What has been requested?
        print("-------- Incoming GET request --------")
        print("  Request data: {}".format(self.requestline))

        # Phase 2: Which data do we want to send back?
        if "data" in self.path: #Was any data requested?
            rstr = decode_url_back_to_string(self.path.split('?data=')[1])
            rdict = json_string_to_dictionary(extract_json_string(rstr))
            if not hasattr(self.server, "data") and "city" not in rdict: #Is there data stored?
                response = "No data stored yet."
            elif "city" in rdict: #Was a city requested? Use YR API?
                response = "Temperature of {} is {}".format(rdict['city'],get_yr_forecast(rdict["city"]))
            else:
                name = ""
                if "sensor_name" in rdict: #Does data for this type exist?
                    name = rdict["sensor_name"]
                    if name in self.server.data: #Does data for this sensor exist?
                        response = "Temperature of {} is {}".format(name, self.load_data(name))
                    else:
                        response = "No data for given name"
        else:
            response = "No data requested" #Default response

        # Phase 3: Let's send back the data!
        response_in_bytes = string_to_unicode_bytes(response)
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(response_in_bytes)

    def do_POST(self):
        print("-------- Incoming POST request --------")
        print("  Request data: {}".format(self.requestline))
        #Format request data back into a dictionary and store it.
        rstr = decode_url_back_to_string(self.path.split('?data=')[1])
        rdict = json_string_to_dictionary(extract_json_string(rstr))
        self.store_data(rdict["sensor_name"], rdict["temperature"])
        
        response = "Stored data: "+rstr
        
        response_in_bytes = string_to_unicode_bytes(response)
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(response_in_bytes)

port = 8023
httpd = HTTPServer(
    ("", port),
    RequestHandler,
)
print("")
print(" ******** TTM4175 Web Server  ******** ")
print(
    "    The server will be reachable via  http://{}:{}/".format(get_ip_address(), port)
)
print("    Terminate the server via Ctrl-C.")
print(" ************************************* ")
print("")
httpd.serve_forever()