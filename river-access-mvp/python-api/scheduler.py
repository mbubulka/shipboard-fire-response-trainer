"""
Background scheduler to fetch USGS data at regular intervals.
Run this in a separate process or container.
"""

import time
import logging
from datetime import datetime
from fetch_usgs_data import fetch_current_conditions, store_conditions_in_db

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Fetch interval in seconds (15 minutes = 900 seconds)
FETCH_INTERVAL = 900

def run_scheduler():
    """
    Run continuous scheduler to fetch USGS data.
    """
    logger.info("🌊 Starting USGS data scheduler...")
    logger.info(f"Fetching data every {FETCH_INTERVAL} seconds ({FETCH_INTERVAL//60} minutes)")
    
    while True:
        try:
            logger.info(f"[{datetime.now()}] Fetching USGS data...")
            conditions = fetch_current_conditions()
            
            if conditions:
                store_conditions_in_db(conditions)
                logger.info(f"✅ Successfully updated {len(conditions)} gauges")
                
                # Log current readings
                for gauge_id, condition in conditions.items():
                    logger.info(f"   Gauge {gauge_id}: {condition['flow_cfs']:.1f} CFS")
            else:
                logger.warning("⚠️  No data returned from USGS")
            
        except Exception as e:
            logger.error(f"❌ Error in scheduler: {e}", exc_info=True)
        
        # Wait for next interval
        time.sleep(FETCH_INTERVAL)

if __name__ == "__main__":
    run_scheduler()
