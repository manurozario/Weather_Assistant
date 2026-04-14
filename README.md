# 🌤️ Weather Tracker

A Python-based weather monitoring system that fetches real-time weather data from the OpenWeatherMap API, stores it in a PostgreSQL database, and delivers a personalized daily morning summary to your phone via Telegram bot.

---

## Features

- Fetches real-time weather data using the OpenWeatherMap API
- Decodes weather icon codes into emojis
- Stores each weather reading into a PostgreSQL database
- Loads last 5 temperature readings from the database for NumPy statistical analysis
- Sends a formatted morning weather summary via Telegram bot
- Scheduled to run every morning at 7:00 AM via cron

---

## Telegram Message Preview

```
Good morning Manuel!
Expected today in Fate: clear sky ☀️
It is currently 78°F
Humidity is 55%
Wind speed is 8.1 mph
Here's today's temp compared to the past 5 days:
Avg Temp: 80.2°F | Max Temp: 85.0°F | Min Temp: 75.0°F
```

---

## Tech Stack

- **Python 3.13**
- **OpenWeatherMap API** — real-time weather data
- **PostgreSQL** — weather data persistence
- **psycopg2** — PostgreSQL adapter for Python
- **NumPy** — statistical analysis on historical readings
- **Telegram Bot API** — morning weather notifications
- **python-dotenv** — environment variable management

---

## Project Structure

```
weather-tracker/
├── src/
│   └── main.py
├── .env.example
├── requirements.txt
└── README.md
```

---

## Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/your-username/weather-tracker.git
cd weather-tracker
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up your `.env` file
```bash
cp .env.example .env
```

Fill in your credentials:
```
API_KEY=your_openweathermap_api_key
HTTP_API=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

### 4. Configure your database connection
In `src/main.py` update the connection block:
```python
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="postgres",
    user="postgres",
    password="your_password"
)
```

### 5. Create the database table
Open pgAdmin or psql and run:
```sql
CREATE TABLE weather_forecast (
    id          SERIAL PRIMARY KEY,
    city        VARCHAR(100),
    country     VARCHAR(10),
    temperature INT,
    description VARCHAR(100),
    humidity    INT,
    wind_speed  FLOAT,
    dt_txt      TIMESTAMP,
    created_at  TIMESTAMP DEFAULT NOW()
);
```

### 6. Run the script
```bash
python src/main.py
```

---

## Telegram Setup

1. Open Telegram and search for **@BotFather**
2. Send `/newbot` and follow the prompts to get your bot token
3. Search for **@userinfobot** and send any message to get your Chat ID
4. Add both values to your `.env` file

---

## How It Works

```
OpenWeatherMap API
        ↓
  Fetch current weather
        ↓
  Insert into PostgreSQL
        ↓
  Load last 5 readings
        ↓
  NumPy calculations
        ↓
  Send Telegram message
```

---

## NumPy Stats

On each run the script loads the last 5 temperature readings from PostgreSQL and computes:

| Stat | Description |
|---|---|
| `avg_temp` | Average temperature over last 5 readings |
| `max_temp` | Highest recorded temperature |
| `min_temp` | Lowest recorded temperature |

---

## Scheduled Daily Run (Cron)

To receive your morning message every day at 7:00 AM:
```bash
crontab -e
```
Add:
```
0 7 * * * /usr/bin/python3 /path/to/weather-tracker/src/main.py
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `API_KEY` | OpenWeatherMap API key |
| `HTTP_API` | Telegram bot token |
| `TELEGRAM_CHAT_ID` | Your Telegram user Chat ID |

---

## Requirements

```
requests
python-dotenv
psycopg2-binary
numpy
```

---

## .env.example

```
API_KEY=
HTTP_API=
TELEGRAM_CHAT_ID=
```

---

## License

This project is licensed under the [GPL-3.0 License](https://www.gnu.org/licenses/gpl-3.0.en.html).
