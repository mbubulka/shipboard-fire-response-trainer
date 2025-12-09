"""
Fetch real USGS streamflow data for Potomac River gauges
and store in MySQL database.
"""

import requests
import json
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

# Real USGS Gauge IDs for Potomac River sections
# Source: https://waterdata.usgs.gov/monitoring-location/
GAUGES = {
    1: {
        "name": "Little Falls",
        "usgs_id": "01646580",  # Potomac River at Little Falls Tdam
        "lat": 38.9456,
        "lon": -77.2211
    },
    2: {
        "name": "Mathers Gorge",
        "usgs_id": "01645500",  # South Branch Potomac River at Petersburg
        "lat": 39.1378,
        "lon": -79.1028
    },
    3: {
        "name": "North Branch",
        "usgs_id": "01604500",  # North Branch Potomac River near Paw Paw
        "lat": 39.5711,
        "lon": -78.6467
    },
    4: {
        "name": "Shenandoah Staircase",
        "usgs_id": "01620000",  # Shenandoah River at Millville (near Shenandoah Staircase section)
        "lat": 39.0711,
        "lon": -77.8133
    }
}

# USGS Water Services endpoint
USGS_IV_URL = "https://waterservices.usgs.gov/nwis/iv/"

def fetch_current_conditions():
    """
    Fetch real-time USGS data for all gauges.
    
    Returns:
        dict: Current conditions for each gauge
    """
    try:
        # Build parameters for USGS API
        site_ids = ",".join([f"USGS-{g['usgs_id']}" for g in GAUGES.values()])
        
        params = {
            "sites": site_ids.replace("USGS-", ""),  # Remove USGS- prefix for this API
            "parameterCd": "00060",  # 00060=Streamflow only (temperature not always available)
            "siteStatus": "active",
            "format": "json"
        }
        
        print(f"📡 Fetching data from USGS for gauges: {list(GAUGES.values())}")
        response = requests.get(USGS_IV_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if "value" not in data:
            print("❌ No data returned from USGS API")
            return None
        
        # Parse USGS response
        results = {}
        
        for value_obj in data["value"]["timeSeries"]:
            source_info = value_obj["sourceInfo"]
            
            # Find matching gauge
            gauge_id = None
            for gid, gauge_info in GAUGES.items():
                if gauge_info["usgs_id"] in source_info["geoLocation"]["geogLocation"]["srs"]:
                    gauge_id = gid
                    break
            
            if gauge_id and "values" in value_obj:
                values_list = value_obj["values"][0]["value"]
                if values_list:
                    latest_value = values_list[-1]  # Most recent reading
                    
                    results[gauge_id] = {
                        "gauge_id": gauge_id,
                        "flow_cfs": float(latest_value["value"]),
                        "flow_cms": float(latest_value["value"]) * 0.0283168,
                        "timestamp": latest_value["dateTime"],
                        "usgs_id": GAUGES[gauge_id]["usgs_id"],
                        "site_name": source_info["siteName"]
                    }
        
        return results
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching USGS data: {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"❌ Error parsing USGS response: {e}")
        return None

def store_conditions_in_db(conditions):
    """
    Store fetched conditions in MySQL database.
    """
    try:
        db_url = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@mysql:3306/paddle_db")
        engine = create_engine(db_url)
        
        with engine.connect() as conn:
            for gauge_id, condition in conditions.items():
                query = text("""
                    INSERT INTO current_conditions 
                    (gauge_id, flow_cfs, flow_cms, timestamp, data_source)
                    VALUES (:gauge_id, :flow_cfs, :flow_cms, :timestamp, :source)
                    ON DUPLICATE KEY UPDATE
                        flow_cfs = :flow_cfs,
                        flow_cms = :flow_cms,
                        timestamp = :timestamp
                """)
                
                conn.execute(query, {
                    "gauge_id": gauge_id,
                    "flow_cfs": condition["flow_cfs"],
                    "flow_cms": condition["flow_cms"],
                    "timestamp": condition["timestamp"],
                    "source": "USGS"
                })
            
            conn.commit()
            print(f"✅ Stored {len(conditions)} conditions in database")
            
    except Exception as e:
        print(f"❌ Error storing data in database: {e}")

def display_fetched_data(conditions):
    """
    Display fetched data in readable format.
    """
    if not conditions:
        return
    
    print("\n" + "="*70)
    print("REAL USGS DATA FOR POTOMAC RIVER SECTIONS")
    print("="*70)
    
    for gauge_id in sorted(conditions.keys()):
        c = conditions[gauge_id]
        print(f"\n📍 {GAUGES[gauge_id]['name']} (Gauge: {c['usgs_id']})")
        print(f"   Site: {c['site_name']}")
        print(f"   Flow: {c['flow_cfs']:.1f} CFS ({c['flow_cms']:.2f} m³/s)")
        print(f"   Last Updated: {c['timestamp']}")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    print("\n🌊 Starting USGS Data Fetch...\n")
    
    # Fetch current conditions from USGS
    conditions = fetch_current_conditions()
    
    if conditions:
        display_fetched_data(conditions)
        store_conditions_in_db(conditions)
        print("\n✅ Data fetch complete!")
    else:
        print("\n⚠️  Could not fetch real data. Check USGS API status.")
