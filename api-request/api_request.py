import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ["WEATHER_API_KEY"]
api_url = f"https://api.weatherstack.com/current?access_key={api_key}&query=New York"

def fetch_data():
    print("Fetching data from Weatherstack API...")
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        print("API response recieved successfully")
        return response.json()
    except requests.exceptions.RequestException as e: 
        print(f"An error occurred: {e}")
        raise



# This just exists for now because we dont want to keep calling the API hitting rate limits
def mock_fetch_data():
    return {'request': {'type': 'City', 'query': 'New York, United States of America', 'language': 'en', 'unit': 'm'}, 'location': {'name': 'New York', 'country': 'United States of America', 'region': 'New York', 'lat': '40.714', 'lon': '-74.006', 'timezone_id': 'America/New_York', 'localtime': '2026-05-18 16:45', 'localtime_epoch': 1779122700, 'utc_offset': '-4.0'}, 'current': {'observation_time': '08:45 PM', 'temperature': 28, 'weather_code': 113, 'weather_icons': ['https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0001_sunny.png'], 'weather_descriptions': ['Sunny'], 'astro': {'sunrise': '05:36 AM', 'sunset': '08:09 PM', 'moonrise': '06:41 AM', 'moonset': '11:00 PM', 'moon_phase': 'Waxing Crescent', 'moon_illumination': 2}, 'air_quality': {'co': '187.85', 'no2': '35.85', 'o3': '89', 'so2': '2.65', 'pm2_5': '18.15', 'pm10': '20.55', 'us-epa-index': '2', 'gb-defra-index': '2'}, 'wind_speed': 22, 'wind_degree': 158, 'wind_dir': 'SSE', 'pressure': 1021, 'precip': 0, 'humidity': 51, 'cloudcover': 0, 'feelslike': 28, 'uv_index': 4, 'visibility': 16, 'is_day': 'yes'}}
