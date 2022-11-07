import requests
import pandas as pd
from geopandas.tools import geocode
import os
import json


# TODO: Abstract this to a function
API_key = os.getenv('WEATHERAPIKEY')

# geocode needs a couple of arguments (point-of-interest, provider_name, user_agent, timeout)

def get_lon_and_lat(zipcode:str, country_code:str='US-GA') -> tuple:
    url =  f"http://api.openweathermap.org/geo/1.0/zip?zip={zipcode}&appid={API_key}"
    
    resp = requests.get(url=url)
    lat, lon = resp.json()['lat'], resp.json()['lon']

    return lat, lon


def get_current_weather(lat, lon, lang='en'):
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=metric&lang={lang}'

    resp = requests.get(url=url)
    return str(resp.json().get('main').get('temp'))
