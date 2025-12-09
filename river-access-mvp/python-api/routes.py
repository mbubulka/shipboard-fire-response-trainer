from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import (
    USGSGauge, CurrentCondition, ArimaPrediction, 
    River, RiverSection, AccessPoint, WeatherCondition, get_db
)
from data_generator import generate_mock_conditions, generate_mock_predictions, get_condition_status
from datetime import datetime, timedelta
from pydantic import BaseModel

router = APIRouter(prefix="/api", tags=["api"])


# Pydantic schemas
class ConditionResponse(BaseModel):
    condition_id: int
    flow_cfs: float
    gauge_height_ft: float
    temperature_f: float
    timestamp: datetime
    status: dict
    
    class Config:
        from_attributes = True


class PredictionResponse(BaseModel):
    prediction_id: int
    prediction_date: str
    predicted_flow_cfs: float
    confidence_lower: float
    confidence_upper: float
    model_version: str
    
    class Config:
        from_attributes = True


class GaugeResponse(BaseModel):
    gauge_id: int
    gauge_name: str
    site_number: str
    latitude: float
    longitude: float
    
    class Config:
        from_attributes = True


class RiverResponse(BaseModel):
    river_id: int
    name: str
    state: str
    description: str
    
    class Config:
        from_attributes = True


# Routes

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "timestamp": datetime.utcnow()}


@router.get("/rivers", response_model=list[RiverResponse])
async def get_rivers(db: Session = Depends(get_db)):
    """Get all rivers"""
    rivers = db.query(River).all()
    return rivers


@router.get("/gauges/{gauge_id}", response_model=GaugeResponse)
async def get_gauge(gauge_id: int, db: Session = Depends(get_db)):
    """Get gauge information"""
    gauge = db.query(USGSGauge).filter(USGSGauge.gauge_id == gauge_id).first()
    if not gauge:
        raise HTTPException(status_code=404, detail="Gauge not found")
    return gauge


@router.get("/conditions/{gauge_id}", response_model=ConditionResponse)
async def get_current_conditions(gauge_id: int, db: Session = Depends(get_db)):
    """Get current conditions for a gauge (real USGS data)"""
    gauge = db.query(USGSGauge).filter(USGSGauge.gauge_id == gauge_id).first()
    if not gauge:
        raise HTTPException(status_code=404, detail="Gauge not found")
    
    # Get most recent condition (prioritize USGS real data)
    condition = db.query(CurrentCondition)\
        .filter(CurrentCondition.gauge_id == gauge_id)\
        .order_by(CurrentCondition.timestamp.desc())\
        .first()
    
    # If no real data exists, generate mock data as fallback
    if not condition:
        condition = generate_mock_conditions(db, gauge_id)
    
    status = get_condition_status(condition.flow_cfs, gauge_id, db)
    
    return {
        "condition_id": condition.condition_id,
        "flow_cfs": float(condition.flow_cfs) if condition.flow_cfs else 0,
        "gauge_height_ft": float(condition.gauge_height_ft) if condition.gauge_height_ft else 0,
        "temperature_f": float(condition.temperature_f) if condition.temperature_f else 0,
        "timestamp": condition.timestamp,
        "status": status
    }


@router.get("/predictions/{gauge_id}", response_model=list[PredictionResponse])
async def get_predictions(gauge_id: int, db: Session = Depends(get_db)):
    """Get ARIMA predictions for a gauge"""
    gauge = db.query(USGSGauge).filter(USGSGauge.gauge_id == gauge_id).first()
    if not gauge:
        raise HTTPException(status_code=404, detail="Gauge not found")
    
    # Get predictions for next 7 days
    predictions = db.query(ArimaPrediction)\
        .filter(ArimaPrediction.gauge_id == gauge_id)\
        .filter(ArimaPrediction.prediction_date >= datetime.now().date())\
        .order_by(ArimaPrediction.prediction_date)\
        .limit(7)\
        .all()
    
    # If no predictions, generate mock data
    if not predictions:
        predictions = generate_mock_predictions(db, gauge_id)
    
    return [
        {
            "prediction_id": p.prediction_id,
            "prediction_date": p.prediction_date.isoformat(),
            "predicted_flow_cfs": float(p.predicted_flow_cfs),
            "confidence_lower": float(p.confidence_lower),
            "confidence_upper": float(p.confidence_upper),
            "model_version": p.model_version,
        }
        for p in predictions
    ]


@router.get("/access-points/{river_id}")
async def get_access_points(river_id: int, db: Session = Depends(get_db)):
    """Get access points for a river"""
    access_points = db.query(AccessPoint).filter(AccessPoint.river_id == river_id).all()
    return access_points


@router.post("/conditions/{gauge_id}/refresh")
async def refresh_conditions(gauge_id: int, db: Session = Depends(get_db)):
    """Manually refresh current conditions (generate mock data)"""
    condition = generate_mock_conditions(db, gauge_id)
    if not condition:
        raise HTTPException(status_code=404, detail="Gauge not found")
    return {"message": "Conditions refreshed", "flow_cfs": condition.flow_cfs}


@router.post("/usgs/refresh")
async def refresh_usgs_data(db: Session = Depends(get_db)):
    """
    Refresh data from USGS API.
    This endpoint triggers data fetch from USGS Water Services.
    Call this periodically (e.g., every 15 minutes) for real-time updates.
    """
    try:
        from fetch_usgs_data import fetch_current_conditions, store_conditions_in_db
        
        conditions = fetch_current_conditions()
        if conditions:
            store_conditions_in_db(conditions)
            return {
                "status": "success",
                "message": f"Refreshed {len(conditions)} gauge readings from USGS",
                "gauges_updated": list(conditions.keys())
            }
        else:
            return {
                "status": "error",
                "message": "Could not fetch data from USGS API"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error refreshing USGS data: {str(e)}")


@router.get("/weather/{section_id}")
async def get_weather(section_id: int, db: Session = Depends(get_db)):
    """Get current weather for a section"""
    section = db.query(RiverSection).filter(RiverSection.section_id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    # Get most recent weather
    weather = db.query(WeatherCondition)\
        .filter(WeatherCondition.section_id == section_id)\
        .order_by(WeatherCondition.timestamp.desc())\
        .first()
    
    if not weather:
        return {
            "section_id": section_id,
            "message": "No weather data available yet",
            "temperature_f": None,
            "conditions": "Data not available"
        }
    
    return {
        "weather_id": weather.weather_id,
        "section_id": weather.section_id,
        "timestamp": weather.timestamp,
        "temperature_f": float(weather.temperature_f) if weather.temperature_f else None,
        "humidity_percent": weather.humidity_percent,
        "wind_speed_mph": float(weather.wind_speed_mph) if weather.wind_speed_mph else None,
        "wind_direction_deg": weather.wind_direction_deg,
        "cloud_cover_percent": weather.cloud_cover_percent,
        "visibility_miles": float(weather.visibility_miles) if weather.visibility_miles else None,
        "conditions": weather.conditions,
        "data_source": weather.data_source
    }


@router.get("/weather")
async def get_all_weather(db: Session = Depends(get_db)):
    """Get latest weather for all sections"""
    sections = db.query(RiverSection).all()
    result = []
    
    for section in sections:
        weather = db.query(WeatherCondition)\
            .filter(WeatherCondition.section_id == section.section_id)\
            .order_by(WeatherCondition.timestamp.desc())\
            .first()
        
        if weather:
            result.append({
                "section_id": section.section_id,
                "section_name": section.name,
                "temperature_f": float(weather.temperature_f) if weather.temperature_f else None,
                "humidity_percent": weather.humidity_percent,
                "wind_speed_mph": float(weather.wind_speed_mph) if weather.wind_speed_mph else None,
                "conditions": weather.conditions,
                "timestamp": weather.timestamp
            })
    
    return result




@router.get("/weather/{gauge_id}")
async def get_weather(gauge_id: int, db: Session = Depends(get_db)):
    """Get latest weather conditions for a gauge's section"""
    try:
        # Get gauge and its section
        gauge = db.query(USGSGauge).filter(USGSGauge.gauge_id == gauge_id).first()
        if not gauge:
            raise HTTPException(status_code=404, detail="Gauge not found")
        
        if not gauge.section_id:
            return {"conditions": "Data not available", "message": "Gauge not assigned to a section"}
        
        # Get most recent weather for the section
        weather = db.query(WeatherCondition)\
            .filter(WeatherCondition.section_id == gauge.section_id)\
            .order_by(WeatherCondition.timestamp.desc())\
            .first()
        
        if not weather:
            return {"conditions": "Data not available", "message": "No weather data yet"}
        
        return {
            "weather_id": weather.weather_id,
            "section_id": weather.section_id,
            "timestamp": weather.timestamp,
            "temperature_f": float(weather.temperature_f) if weather.temperature_f else None,
            "feels_like_f": float(weather.feels_like_f) if weather.feels_like_f else None,
            "humidity_percent": weather.humidity_percent,
            "wind_speed_mph": float(weather.wind_speed_mph) if weather.wind_speed_mph else None,
            "wind_gust_mph": float(weather.wind_gust_mph) if weather.wind_gust_mph else None,
            "wind_direction_deg": weather.wind_direction_deg,
            "wind_direction": weather.wind_direction,
            "precipitation_in": float(weather.precipitation_in) if weather.precipitation_in else None,
            "precipitation_chance": weather.precipitation_chance,
            "visibility_miles": float(weather.visibility_miles) if weather.visibility_miles else None,
            "conditions": "Data available"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching weather: {str(e)}")


@router.post("/weather/refresh")
async def refresh_weather(db: Session = Depends(get_db)):
    """
    Refresh weather data for all sections from Open-Meteo API.
    """
    try:
        from fetch_weather_data import fetch_weather_for_section, store_weather_in_db, SECTIONS
        
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
            return {
                "status": "success",
                "message": f"Refreshed weather for {len(all_weather)} sections",
                "sections_updated": [w["section_id"] for w in all_weather]
            }
        else:
            return {
                "status": "error",
                "message": "Could not fetch weather data"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error refreshing weather: {str(e)}")
