"""
Background scheduler to fetch weather data at regular intervals.
Run this in a separate process or container.
"""

import time
import logging
from datetime import datetime
from fetch_weather_data import fetch_weather_for_section, store_weather_in_db, SECTIONS

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Fetch interval in seconds (30 minutes = 1800 seconds)
FETCH_INTERVAL = 1800

def run_weather_scheduler():
    """
    Run continuous scheduler to fetch weather data.
    """
    logger.info("🌤️  Starting Weather Data Scheduler...")
    logger.info(f"Fetching data every {FETCH_INTERVAL} seconds ({FETCH_INTERVAL//60} minutes)")
    
    while True:
        try:
            logger.info(f"[{datetime.now()}] Fetching weather data...")
            
            all_weather = []
            for section_id, section_info in SECTIONS.items():
                weather = fetch_weather_for_section(
                    section_id,
                    section_info["lat"],
                    section_info["lon"]
                )
                if weather:
                    all_weather.append(weather)
            
            if all_weather:
                store_weather_in_db(all_weather)
                logger.info(f"✅ Successfully updated weather for {len(all_weather)} sections")
                
                # Log current conditions
                for weather in all_weather:
                    section_id = weather["section_id"]
                    section_name = SECTIONS[section_id]["name"]
                    logger.info(f"   {section_name}: {weather['temperature_f']:.1f}°F, {weather['conditions']}")
            else:
                logger.warning("⚠️  No weather data retrieved")
            
        except Exception as e:
            logger.error(f"❌ Error in scheduler: {e}", exc_info=True)
        
        # Wait for next interval
        time.sleep(FETCH_INTERVAL)

if __name__ == "__main__":
    run_weather_scheduler()
