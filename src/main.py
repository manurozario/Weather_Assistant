import requests
import os
from dotenv import load_dotenv

def configure():
    load_dotenv()

def get_weather_info(url):
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        print(f"{response.status_code}")
        return weather_data
    else:
        print(f"Failed to retrive data {response.status_code}")

def main():
    configure()
    lat = 32.92
    lon = -96.38
    unit_type = "imperial"

    count = 1
    name = "Manuel"
    url_current = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units={unit_type}&appid={os.getenv('api_key')}"
    url_daily = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units={unit_type}&appid={os.getenv('api_key')}"
    current_info = get_weather_info(url_current)
    daily_info = get_weather_info(url_daily)

    icon_to_emoji = {
        "01d": "☀️",  "01n": "🌙",
        "02d": "⛅",  "02n": "🌑",
        "03d": "🌤️", "03n": "🌤️",
        "04d": "☁️",  "04n": "☁️",
        "09d": "🌧️", "09n": "🌧️",
        "10d": "🌦️", "10n": "🌧️",
        "11d": "⛈️", "11n": "⛈️",
        "13d": "❄️",  "13n": "❄️",
        "50d": "🌫️", "50n": "🌫️"
    }

    emoji = icon_to_emoji.get(daily_info["list"][0]["weather"][0]["icon"])
    forecast = daily_info["list"][0]["weather"][0]["description"]
    curr_temp = current_info["main"]["temp"]
    temp_max = daily_info["list"][0]["main"]["temp_max"]
    temp_min = daily_info["list"][0]["main"]["temp_min"]

    print(f"{current_info["main"]["temp"]}")
    print(f"{daily_info["list"][0]["main"]["temp_max"]}")
    print(f"{daily_info["list"][0]["dt_txt"]}")

    if current_info and daily_info:
        print(f"Good morning {name}!\n"
            f"Expected today: {forecast}{emoji}\n"
            f"It is currently {curr_temp}\u00b0F, with a high of {temp_max}\u00b0F and low of {temp_min}\u00b0F")
        
main()




