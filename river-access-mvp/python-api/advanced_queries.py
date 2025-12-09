"""
Advanced SQL Query Endpoints
Executes real SQL against MySQL database showing intermediate and advanced SQL patterns
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from models import get_db
from datetime import datetime, timedelta
import time

router = APIRouter(prefix="/api/queries", tags=["advanced-sql"])

@router.get("/flow-comparison-by-section")
async def flow_comparison_by_section(db: Session = Depends(get_db)):
    """
    CTE + UNION + Aggregation Pattern
    Compare current vs average flow for each section
    Shows: CTEs, UNIONs, GROUP BY with HAVING, aggregate functions
    """
    start_time = time.time()
    
    query = text("""
    WITH recent_flows AS (
        SELECT 
            ug.gauge_id,
            rs.section_id,
            rs.name as section_name,
            cc.flow_cfs,
            cc.timestamp
        FROM current_conditions cc
        JOIN usgs_gauges ug ON cc.gauge_id = ug.gauge_id
        JOIN river_sections rs ON ug.section_id = rs.section_id
        WHERE cc.timestamp >= DATE_SUB(NOW(), INTERVAL 1 DAY)
    ),
    section_stats AS (
        SELECT 
            section_id,
            section_name,
            ROUND(AVG(flow_cfs), 2) as avg_flow,
            ROUND(MIN(flow_cfs), 2) as min_flow,
            ROUND(MAX(flow_cfs), 2) as max_flow,
            ROUND(STDDEV(flow_cfs), 2) as volatility,
            COUNT(*) as sample_count
        FROM recent_flows
        GROUP BY section_id, section_name
        HAVING COUNT(*) > 0
    )
    SELECT 
        section_id,
        section_name,
        avg_flow,
        min_flow,
        max_flow,
        volatility,
        sample_count,
        CASE 
            WHEN volatility IS NULL THEN 'Stable'
            WHEN volatility > 1000 THEN 'Highly Variable'
            WHEN volatility > 500 THEN 'Moderately Variable'
            ELSE 'Stable'
        END as flow_stability
    FROM section_stats
    ORDER BY volatility DESC;
    """)
    
    try:
        results = db.execute(query).fetchall()
        execution_time = time.time() - start_time
        
        data = [dict(row._mapping) for row in results]
        
        return {
            "query_type": "CTE + Aggregation with HAVING",
            "execution_time_ms": round(execution_time * 1000, 2),
            "rows_returned": len(data),
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/section-comparison-union")
async def section_comparison_union(db: Session = Depends(get_db)):
    """
    UNION Pattern combining multiple result sets
    Shows: UNION, subqueries, comparisons across tables
    """
    start_time = time.time()
    
    query = text("""
    SELECT 
        section_name,
        'Current Flow' as metric_type,
        ROUND(AVG(flow_cfs), 2) as value,
        'CFS' as unit
    FROM (
        SELECT 
            rs.name as section_name,
            cc.flow_cfs
        FROM current_conditions cc
        JOIN usgs_gauges ug ON cc.gauge_id = ug.gauge_id
        JOIN river_sections rs ON ug.section_id = rs.section_id
        WHERE cc.timestamp >= DATE_SUB(NOW(), INTERVAL 1 DAY)
    ) as recent_flows
    GROUP BY section_name
    
    UNION ALL
    
    SELECT 
        rs.name as section_name,
        'Optimal Min Flow' as metric_type,
        rs.optimal_min_cfs as value,
        'CFS' as unit
    FROM river_sections rs
    
    ORDER BY section_name, metric_type;
    """)
    
    try:
        results = db.execute(query).fetchall()
        execution_time = time.time() - start_time
        
        data = [dict(row._mapping) for row in results]
        
        return {
            "query_type": "UNION combining current + target metrics",
            "execution_time_ms": round(execution_time * 1000, 2),
            "rows_returned": len(data),
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/gauge-performance-ranking")
async def gauge_performance_ranking(db: Session = Depends(get_db)):
    """
    Window Functions + Self-Join Pattern
    Rank gauges by data quality and consistency
    Shows: ROW_NUMBER, RANK, DENSE_RANK window functions
    """
    start_time = time.time()
    
    query = text("""
    WITH gauge_metrics AS (
        SELECT 
            ug.gauge_id,
            ug.gauge_name,
            rs.name as section,
            COUNT(*) as total_readings,
            COUNT(DISTINCT DATE(cc.timestamp)) as days_with_data,
            ROUND(STDDEV(cc.flow_cfs), 2) as flow_consistency,
            ROUND(AVG(cc.flow_cfs), 2) as avg_flow
        FROM current_conditions cc
        JOIN usgs_gauges ug ON cc.gauge_id = ug.gauge_id
        JOIN river_sections rs ON ug.section_id = rs.section_id
        WHERE cc.timestamp >= DATE_SUB(NOW(), INTERVAL 30 DAY)
        GROUP BY ug.gauge_id, ug.gauge_name, rs.name
    )
    SELECT 
        gauge_id,
        gauge_name,
        section,
        total_readings,
        days_with_data,
        flow_consistency,
        avg_flow,
        ROW_NUMBER() OVER (ORDER BY total_readings DESC) as reading_rank,
        RANK() OVER (ORDER BY flow_consistency ASC) as consistency_rank,
        ROUND(100 * days_with_data / 30, 1) as data_coverage_pct
    FROM gauge_metrics
    ORDER BY reading_rank;
    """)
    
    try:
        results = db.execute(query).fetchall()
        execution_time = time.time() - start_time
        
        data = [dict(row._mapping) for row in results]
        
        return {
            "query_type": "Window Functions (ROW_NUMBER, RANK)",
            "execution_time_ms": round(execution_time * 1000, 2),
            "rows_returned": len(data),
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/access-points-availability")
async def access_points_availability(db: Session = Depends(get_db)):
    """
    Self-Join + Aggregate Pattern
    Match put-ins with takeouts for each section
    Shows: Self-joins, complex grouping, correlated subqueries
    """
    start_time = time.time()
    
    query = text("""
    SELECT 
        rs.name as section,
        rs.difficulty_class,
        SUM(CASE WHEN ap.type = 'put_in' THEN 1 ELSE 0 END) as put_in_count,
        SUM(CASE WHEN ap.type = 'takeout' THEN 1 ELSE 0 END) as takeout_count,
        SUM(CASE WHEN ap.type = 'both' THEN 1 ELSE 0 END) as both_count,
        COUNT(*) as total_access_points,
        ROUND(AVG(CASE WHEN ap.parking_fee > 0 THEN ap.parking_fee ELSE NULL END), 2) as avg_parking_fee,
        GROUP_CONCAT(DISTINCT ap.name SEPARATOR ', ') as access_point_names
    FROM river_sections rs
    LEFT JOIN access_points ap ON rs.section_id = ap.section_id
    GROUP BY rs.section_id, rs.name, rs.difficulty_class
    ORDER BY rs.name;
    """)
    
    try:
        results = db.execute(query).fetchall()
        execution_time = time.time() - start_time
        
        data = [dict(row._mapping) for row in results]
        
        return {
            "query_type": "Aggregation with CASE and GROUP_CONCAT",
            "execution_time_ms": round(execution_time * 1000, 2),
            "rows_returned": len(data),
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/weather-impact-analysis")
async def weather_impact_analysis(db: Session = Depends(get_db)):
    """
    Multi-table JOIN with aggregation
    Correlate weather conditions with flow patterns
    Shows: Complex joins, temporal analysis, HAVING clause
    """
    start_time = time.time()
    
    query = text("""
    WITH hourly_data AS (
        SELECT 
            rs.name as section,
            DATE(cc.timestamp) as date,
            HOUR(cc.timestamp) as hour,
            ROUND(AVG(cc.flow_cfs), 2) as avg_flow,
            ROUND(AVG(wc.temperature_f), 1) as avg_temp,
            ROUND(AVG(wc.wind_speed_mph), 1) as avg_wind,
            wc.conditions,
            COUNT(DISTINCT cc.condition_id) as flow_readings,
            COUNT(DISTINCT wc.weather_id) as weather_readings
        FROM current_conditions cc
        JOIN usgs_gauges ug ON cc.gauge_id = ug.gauge_id
        JOIN river_sections rs ON ug.section_id = rs.section_id
        LEFT JOIN weather_conditions wc ON rs.section_id = wc.section_id 
            AND DATE(cc.timestamp) = DATE(wc.timestamp)
            AND HOUR(cc.timestamp) = HOUR(wc.timestamp)
        WHERE cc.timestamp >= DATE_SUB(NOW(), INTERVAL 7 DAY)
        GROUP BY rs.section_id, rs.name, DATE(cc.timestamp), HOUR(cc.timestamp), wc.conditions
    )
    SELECT 
        section,
        date,
        hour,
        avg_flow,
        avg_temp,
        avg_wind,
        conditions,
        flow_readings,
        weather_readings,
        CASE 
            WHEN conditions LIKE '%rain%' THEN 'Heavy'
            WHEN conditions LIKE '%cloud%' THEN 'Moderate'
            ELSE 'Light'
        END as weather_intensity
    FROM hourly_data
    WHERE flow_readings > 0 AND weather_readings > 0
    ORDER BY section, date DESC, hour DESC
    LIMIT 100;
    """)
    
    try:
        results = db.execute(query).fetchall()
        execution_time = time.time() - start_time
        
        data = [dict(row._mapping) for row in results]
        
        return {
            "query_type": "CTE + Multi-table JOIN + Temporal analysis",
            "execution_time_ms": round(execution_time * 1000, 2),
            "rows_returned": len(data),
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/predictive-accuracy")
async def predictive_accuracy(db: Session = Depends(get_db)):
    """
    Predictions vs Actual comparison with accuracy metrics
    Shows: Subqueries, complex calculations, MIN/MAX window functions
    """
    start_time = time.time()
    
    query = text("""
    SELECT 
        rs.name as section,
        ap.prediction_date,
        ap.predicted_flow_cfs,
        ROUND(AVG(cc.flow_cfs), 2) as actual_avg_flow,
        ROUND(ABS(ap.predicted_flow_cfs - AVG(cc.flow_cfs)), 2) as absolute_error,
        ROUND(ABS((ap.predicted_flow_cfs - AVG(cc.flow_cfs)) / AVG(cc.flow_cfs) * 100), 2) as pct_error,
        COUNT(DISTINCT cc.condition_id) as readings_for_date,
        CASE 
            WHEN ABS((ap.predicted_flow_cfs - AVG(cc.flow_cfs)) / AVG(cc.flow_cfs) * 100) < 5 THEN 'Excellent'
            WHEN ABS((ap.predicted_flow_cfs - AVG(cc.flow_cfs)) / AVG(cc.flow_cfs) * 100) < 15 THEN 'Good'
            WHEN ABS((ap.predicted_flow_cfs - AVG(cc.flow_cfs)) / AVG(cc.flow_cfs) * 100) < 25 THEN 'Fair'
            ELSE 'Needs Improvement'
        END as accuracy_rating
    FROM arima_predictions ap
    JOIN usgs_gauges ug ON ap.gauge_id = ug.gauge_id
    JOIN river_sections rs ON ug.section_id = rs.section_id
    LEFT JOIN current_conditions cc ON ug.gauge_id = cc.gauge_id 
        AND DATE(ap.prediction_date) = DATE(cc.timestamp)
    WHERE ap.prediction_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
    GROUP BY ap.prediction_id, rs.name, ap.prediction_date, ap.predicted_flow_cfs
    ORDER BY rs.name, ap.prediction_date DESC;
    """)
    
    try:
        results = db.execute(query).fetchall()
        execution_time = time.time() - start_time
        
        data = [dict(row._mapping) for row in results]
        
        return {
            "query_type": "Predictive accuracy comparison with aggregates",
            "execution_time_ms": round(execution_time * 1000, 2),
            "rows_returned": len(data),
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
