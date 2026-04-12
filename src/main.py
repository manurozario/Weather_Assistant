import requests
import json
import os
from dotenv import load_dotenv
import psycopg2
from datetime import datetime, timezone
import numpy as np

def configure():
    load_dotenv()

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="postgres",
    user="postgres",
    password="1234"
)
cursor = conn.cursor() 

def get_weather_info(get_url):
    response = requests.get(get_url)

    if response.status_code == 200:
        weather_data = response.json()
        print(f"{response.status_code}")
        return weather_data
    else:
        print(f"Failed to retrive data {response.status_code}")

def send_telegram_messsage(message):
    url = f"https://api.telegram.org/bot{os.getenv('HTTP_API')}/sendMessage"
    payload = {
        "chat_id": os.getenv('TELEGRAM_CHAT_ID'),
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    return response.json()

def load_data():
    cursor.execute("""
        SELECT temperature 
        FROM weather_forecast 
        ORDER BY created_at DESC 
        LIMIT 5
    """)
    rows = cursor.fetchall()
    rows = [int(row[0]) for row in rows]
    return rows

def main():

    configure()
    lat = 32.92
    lon = -96.38
    unit_type = "imperial"
    count = 1
    name = "Manuel"

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units={unit_type}&appid={os.getenv('API_KEY')}"
    # url_daily = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units={unit_type}&appid={os.getenv('API_KEY')}"
    weather_info = get_weather_info(url)

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

    emoji = icon_to_emoji.get(weather_info["weather"][0]["icon"])
    forecast = weather_info["weather"][0]["description"]
    curr_temp = round(weather_info["main"]["temp"])
    humidity = weather_info["main"]["temp"]
    wind_speed = weather_info["wind"]["speed"]
    city = weather_info["name"]
    country = weather_info["sys"]["country"]
    dt = datetime.fromtimestamp(weather_info["dt"], tz=timezone.utc)
    dt_out = dt.replace(tzinfo=None)

    cursor.execute("""
        INSERT INTO weather_forecast 
            (
                city, 
                country, 
                temperature, 
                description, 
                humidity, 
                wind_speed, 
                dt_txt
            )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
            city,
            country,
            curr_temp,
            forecast,
            humidity,
            wind_speed,
            dt_out
    ))  
    conn.commit()

    temps = load_data()
    stats = {
                "avg_temp":     np.round(np.mean(temps), 1),
                "max_temp":     np.round(np.max(temps), 1),
                "min_temp":     np.round(np.min(temps), 1)
    }

    if weather_info:
        message= (
            f"Good morning {name}!\n"
            f"Expected today in {city}: {forecast}{emoji}\n"
            f"It is currently {curr_temp}\u00b0F\n" 
            f"Humidity is {humidity}%\n"
            f"Wind speed is {wind_speed} mph"
            f"Here's todays temp compared to the past 5 days:\n"
            f"Avg Temp: {stats['avg_temp']}\u00b0F | Max Temp: {stats['max_temp']}\u00b0F | Min Temp: {stats['min_temp']}\u00b0F"
        )

        send_telegram_messsage(message)
        # print(message)
        print("Message sent!")

        cursor.close()
        conn.close()
        
main()




