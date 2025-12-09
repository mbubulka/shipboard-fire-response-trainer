"""
Fetch real weather data for paddling sections using Open-Meteo API (free, no API key needed).
Store in MySQL database.
"""

import requests
import json
from datetime import datetime
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Section locations (lat, lon)
SECTIONS = {
    1: {"name": "Little Falls", "lat": 39.0067, "lon": -77.2481},
    2: {"name": "Mathers Gorge", "lat": 39.0812, "lon": -77.3389},
    3: {"name": "North Branch", "lat": 39.5234, "lon": -79.2876},
    4: {"name": "Shenandoah Staircase", "lat": 38.9234, "lon": -77.8901}
}

# Open-Meteo API endpoint (free, no API key required)
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

def fetch_weather_for_section(section_id, latitude, longitude):
    """
    Fetch current weather for a section using Open-Meteo API.
    
    Returns:
        dict: Weather data or None if failed
    """
    try:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,wind_direction_10m,weather_code,cloud_cover,visibility",
            "timezone": "America/New_York",
            "temperature_unit": "fahrenheit"
        }
        
        response = requests.get(WEATHER_API_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if "current" not in data:
            logger.warning(f"No current weather data for section {section_id}")
            return None
        
        current = data["current"]
        
        weather_data = {
            "section_id": section_id,
            "temperature_f": current.get("temperature_2m"),
            "humidity_percent": current.get("relative_humidity_2m"),
            "wind_speed_mph": current.get("wind_speed_10m"),
            "wind_direction_deg": current.get("wind_direction_10m"),
            "cloud_cover_percent": current.get("cloud_cover"),
            "visibility_miles": current.get("visibility", 10) / 1609.34,  # Convert meters to miles
            "weather_code": current.get("weather_code"),
            "conditions": weather_code_to_description(current.get("weather_code")),
            "timestamp": datetime.fromisoformat(current.get("time").replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return weather_data
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching weather for section {section_id}: {e}")
        return None
    except (KeyError, ValueError) as e:
        logger.error(f"Error parsing weather response for section {section_id}: {e}")
        return None

def weather_code_to_description(code):
    """Convert WMO weather code to description."""
    codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Foggy",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Heavy drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Thunderstorm with hail"
    }
    return codes.get(code, "Unknown")

def store_weather_in_db(weather_list):
    """Store fetched weather in MySQL database."""
    try:
        db_url = os.getenv("DATABASE_URL", "mysql+pymysql://river_user:river_pass@mysql:3306/river_access")
        engine = create_engine(db_url)
        
        with engine.connect() as conn:
            for weather in weather_list:
                query = text("""
                    INSERT INTO weather_conditions 
                    (section_id, timestamp, temperature_f, humidity_percent, wind_speed_mph, 
                     wind_direction_deg, cloud_cover_percent, visibility_miles, weather_code, conditions, data_source)
                    VALUES (:section_id, :timestamp, :temperature_f, :humidity_percent, :wind_speed_mph,
                            :wind_direction_deg, :cloud_cover_percent, :visibility_miles, :weather_code, :conditions, 'OpenMeteo')
                """)
                
                conn.execute(query, weather)
            
            conn.commit()
            logger.info(f"✅ Stored {len(weather_list)} weather conditions in database")
            
    except Exception as e:
        logger.error(f"❌ Error storing weather in database: {e}")

def display_fetched_weather(weather_list):
    """Display fetched weather in readable format."""
    if not weather_list:
        return
    
    print("\n" + "="*70)
    print("REAL WEATHER DATA FOR PADDLING SECTIONS")
    print("="*70)
    
    for weather in weather_list:
        section_id = weather["section_id"]
        section_name = SECTIONS[section_id]["name"]
        print(f"\n📍 {section_name}")
        print(f"   Temperature: {weather['temperature_f']:.1f}°F")
        print(f"   Humidity: {weather['humidity_percent']}%")
        print(f"   Wind: {weather['wind_speed_mph']:.1f} mph from {weather['wind_direction_deg']}°")
        print(f"   Conditions: {weather['conditions']}")
        print(f"   Cloud Cover: {weather['cloud_cover_percent']}%")
        print(f"   Visibility: {weather['visibility_miles']:.1f} miles")
        print(f"   Time: {weather['timestamp']}")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    logger.info("\n🌤️  Starting Weather Data Fetch...\n")
    
    all_weather = []
    
    # Fetch weather for all sections
    for section_id, section_info in SECTIONS.items():
        logger.info(f"Fetching weather for {section_info['name']}...")
        weather = fetch_weather_for_section(
            section_id,
            section_info["lat"],
            section_info["lon"]
        )
        if weather:
            all_weather.append(weather)
    
    if all_weather:
        display_fetched_weather(all_weather)
        store_weather_in_db(all_weather)
        logger.info("\n✅ Weather fetch complete!")
    else:
        logger.warning("\n⚠️  Could not fetch weather data. Check API status.")
