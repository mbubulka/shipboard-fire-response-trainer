import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import CurrentCondition, ArimaPrediction, USGSGauge
from datetime import date
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings('ignore')


def generate_mock_conditions(db: Session, gauge_id: int = 1):
    """Generate mock current conditions for testing"""
    gauge = db.query(USGSGauge).filter(USGSGauge.gauge_id == gauge_id).first()
    if not gauge:
        return None
    
    # Simulate realistic flow variations
    base_flow = random.randint(4000, 8000)
    variation = random.randint(-500, 500)
    flow = base_flow + variation
    
    condition = CurrentCondition(
        gauge_id=gauge_id,
        timestamp=datetime.utcnow(),
        flow_cfs=flow,
        gauge_height_ft=round(random.uniform(2.5, 5.0), 2),
        temperature_f=round(random.uniform(45, 65), 1),
        data_quality="Good"
    )
    
    db.add(condition)
    db.commit()
    db.refresh(condition)
    
    return condition


def generate_mock_predictions(db: Session, gauge_id: int = 1):
    """Generate ARIMA-based predictions for the next 7 days"""
    gauge = db.query(USGSGauge).filter(USGSGauge.gauge_id == gauge_id).first()
    if not gauge:
        return []
    
    predictions = []
    
    # Get historical data from current_conditions table
    historical = db.query(CurrentCondition).filter(
        CurrentCondition.gauge_id == gauge_id
    ).order_by(CurrentCondition.timestamp.desc()).limit(30).all()
    
    if len(historical) < 3:
        # Not enough data for ARIMA - use fallback trend model
        base_flow = 5000
        for i in range(1, 8):
            pred_date = date.today() + timedelta(days=i)
            existing = db.query(ArimaPrediction).filter(
                ArimaPrediction.gauge_id == gauge_id,
                ArimaPrediction.prediction_date == pred_date
            ).first()
            
            if not existing:
                trend = i * 50
                noise = random.randint(-300, 300)
                predicted_flow = base_flow + trend + noise
                lower = predicted_flow - 500
                upper = predicted_flow + 500
                
                prediction = ArimaPrediction(
                    gauge_id=gauge_id,
                    prediction_date=pred_date,
                    predicted_flow_cfs=round(predicted_flow, 2),
                    confidence_lower=round(lower, 2),
                    confidence_upper=round(upper, 2),
                    model_version="1.0-fallback"
                )
                db.add(prediction)
                predictions.append(prediction)
        
        if predictions:
            db.commit()
        return predictions
    
    try:
        # Extract flow data and reverse to chronological order
        flows = np.array([h.flow_cfs for h in reversed(historical)])
        
        # Fit ARIMA(1,1,1) model - standard for river flow
        model = ARIMA(flows, order=(1, 1, 1))
        fitted_model = model.fit()
        
        # Generate 7-day forecast
        forecast_result = fitted_model.get_forecast(steps=7)
        forecast_values = forecast_result.predicted_mean
        conf_int = forecast_result.conf_int(alpha=0.05)
        
        for i, pred_value in enumerate(forecast_values, 1):
            pred_date = date.today() + timedelta(days=i)
            
            existing = db.query(ArimaPrediction).filter(
                ArimaPrediction.gauge_id == gauge_id,
                ArimaPrediction.prediction_date == pred_date
            ).first()
            
            if not existing:
                predicted_flow = max(float(pred_value), 100)  # Ensure minimum flow
                lower = max(float(conf_int.iloc[i-1, 0]), 100)
                upper = float(conf_int.iloc[i-1, 1])
                
                prediction = ArimaPrediction(
                    gauge_id=gauge_id,
                    prediction_date=pred_date,
                    predicted_flow_cfs=round(predicted_flow, 2),
                    confidence_lower=round(lower, 2),
                    confidence_upper=round(upper, 2),
                    model_version="2.0-arima"
                )
                db.add(prediction)
                predictions.append(prediction)
        
        if predictions:
            db.commit()
        
        return predictions
    
    except Exception as e:
        print(f"ARIMA fitting failed: {e}. Using fallback trend model.")
        # Fallback to simple trend if ARIMA fails
        base_flow = flows[-1] if len(flows) > 0 else 5000
        for i in range(1, 8):
            pred_date = date.today() + timedelta(days=i)
            existing = db.query(ArimaPrediction).filter(
                ArimaPrediction.gauge_id == gauge_id,
                ArimaPrediction.prediction_date == pred_date
            ).first()
            
            if not existing:
                trend = i * 50
                noise = random.randint(-300, 300)
                predicted_flow = base_flow + trend + noise
                lower = predicted_flow - 500
                upper = predicted_flow + 500
                
                prediction = ArimaPrediction(
                    gauge_id=gauge_id,
                    prediction_date=pred_date,
                    predicted_flow_cfs=round(predicted_flow, 2),
                    confidence_lower=round(lower, 2),
                    confidence_upper=round(upper, 2),
                    model_version="1.0-fallback"
                )
                db.add(prediction)
                predictions.append(prediction)
        
        if predictions:
            db.commit()
        
        return predictions


def get_condition_status(flow_cfs: float, gauge_id: int, db: Session) -> dict:
    """Classify conditions as Good/High/Low based on optimal flow"""
    gauge = db.query(USGSGauge).filter(USGSGauge.gauge_id == gauge_id).first()
    if not gauge or not gauge.section:
        return {"status": "unknown", "recommendation": "No data available"}
    
    section = gauge.section
    
    if section.optimal_min_cfs and section.optimal_max_cfs:
        if flow_cfs < section.optimal_min_cfs:
            return {
                "status": "Too Low",
                "recommendation": "Flow is too low for safe paddling",
                "color": "red"
            }
        elif flow_cfs > section.optimal_max_cfs:
            return {
                "status": "Too High",
                "recommendation": "Flow is too high - dangerous conditions",
                "color": "red"
            }
        else:
            return {
                "status": "Good",
                "recommendation": "Optimal conditions for paddling",
                "color": "green"
            }
    
    return {"status": "unknown", "recommendation": "No optimal flow data"}
