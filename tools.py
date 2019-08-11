import httplib2
import xmltodict
import json
import time

# ELEXON PORTAL
API_VERSION = "v1"
try:
    from config import KEY
except ImportError:
    print("KEY not found!")
    print("Exiting...")
    exit()

def post_elexon(url):
    http_obj = httplib2.Http()
    resp, content = http_obj.request(
        uri=url+"&ServiceType=xml",
        method="GET",
        headers={"Content-Type": f"application/xml; charset=UTF-8"},
    )

    print(f"===Response Status {resp['status']}===")
    print(f"===Requested {resp['content-location']} ===")
    print(f"==={'SUCCESS' if 'content-disposition' in resp else 'ERROR'}===")

    data = xmltodict.parse(content)
    json_data = json.dumps(data)
    return json.loads(json_data)["response"]

def print_json(data,indent=2):
    print(json.dumps(data,indent=indent))

def print_columns(data, col_width=10):
    for row in data:
        print("".join(str(word).ljust(col_width) for word in row))

def current_production(fuel_type=""):
    return post_elexon(
    url=f'https://api.bmreports.com/BMRS/FUELINSTHHCUR/{API_VERSION}?APIKey={KEY}&FuelType={fuel_type}')

if __name__ == "__main__":
    data = current_production()
    production = []
    # get all production types. name and amount
    domestic_production = data["responseBody"]["responseList"]["item"]
    for prod_type in domestic_production:
        fuel = prod_type["fuelType"]
        MW = prod_type["currentMW"]
        percent = prod_type["currentPercentage"]
        production.append((fuel,MW,percent))
    print("===DOMESTIC PRODUCTION===")
    print_columns(production)
