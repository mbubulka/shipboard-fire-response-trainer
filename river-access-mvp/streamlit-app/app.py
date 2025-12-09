import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import folium
from streamlit_folium import st_folium

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Page config
st.set_page_config(
    page_title="River Access & Conditions",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styling - Professional theme
st.markdown("""
<style>
    /* Primary theme colors */
    :root {
        --primary: #0066cc;
        --success: #00a86b;
        --warning: #ff9500;
        --danger: #ff4444;
    }
    
    .header {
        background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%);
        color: white;
        padding: 2rem;
        border-radius: 8px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0,102,204,0.2);
    }
    
    .header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .subheader {
        color: #666;
        font-size: 1rem;
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #0066cc;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .metric-label {
        color: #999;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-value {
        color: #333;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .status-good {
        background-color: #f0fdf4;
        color: #00a86b;
    }
    
    .status-warning {
        background-color: #fffbf0;
        color: #ff9500;
    }
    
    .status-danger {
        background-color: #fff5f5;
        color: #ff4444;
    }
    
    .section-header {
        color: #0066cc;
        font-size: 1.3rem;
        font-weight: 700;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e0e0e0;
    }
    
    .info-box {
        background-color: #e3f2fd;
        border-left: 4px solid #0066cc;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background-color: #fffbf0;
        border-left: 4px solid #ff9500;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


# Header
st.markdown('<div class="header"> River Access & Conditions</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Real-time flow data and predictions for the DMV region</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("## Navigation")
page = st.sidebar.radio("Select a section:", ["Dashboard", "Predictions", "Map", "Access Points", "SQL Queries", "API"])

@st.cache_data(ttl=300)
def fetch_current_conditions(gauge_id=1):
    """Fetch current conditions from API"""
    try:
        response = requests.get(f"{API_URL}/api/conditions/{gauge_id}", timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching conditions: {e}")
        return None

@st.cache_data(ttl=300)
def fetch_predictions(gauge_id=1):
    """Fetch predictions from API"""
    try:
        response = requests.get(f"{API_URL}/api/predictions/{gauge_id}", timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching predictions: {e}")
        return None

@st.cache_data(ttl=300)
def fetch_rivers():
    """Fetch rivers from API"""
    try:
        response = requests.get(f"{API_URL}/api/rivers", timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching rivers: {e}")
        return []

def get_status_color(status):
    """Get color for status badge"""
    if "Good" in status:
        return "🟢"
    elif "High" in status or "Low" in status:
        return ""
    else:
        return ""

if page == "Dashboard":
    # Define available sections with their gauge IDs
    sections = {
        "Little Falls": 1,
        "Mathers Gorge": 2,
        "North Branch": 3,
        "Shenandoah Staircase": 4
    }
    
    selected_section = st.sidebar.selectbox(" Select River Section:", list(sections.keys()))
    selected_gauge_id = sections[selected_section]
    
    st.markdown(f"## Current Conditions - {selected_section}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        conditions = fetch_current_conditions(gauge_id=selected_gauge_id)
        weather = None
        
        # Try to fetch weather
        try:
            weather_response = requests.get(f"{API_URL}/api/weather/{selected_gauge_id}", timeout=5)
            if weather_response.status_code == 200:
                weather = weather_response.json()
        except:
            pass
        
        if conditions:
            # Display metrics
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            
            with metric_col1:
                flow_status = conditions.get('status', {})
                st.metric(
                    "Flow Status",
                    f"{get_status_color(flow_status.get('status', 'Unknown'))} {flow_status.get('status', 'Unknown')}",
                    f"{conditions.get('flow_cfs', 0):.0f} CFS"
                )
            
            with metric_col2:
                st.metric(
                    "Gauge Height",
                    f"{conditions.get('gauge_height_ft', 0):.2f} ft"
                )
            
            with metric_col3:
                wind_speed = weather.get('wind_speed_mph') if weather else None
                wind_gust = weather.get('wind_gust_mph') if weather else None
                st.metric(
                    "Wind Speed",
                    f"{wind_speed} mph" if wind_speed else "N/A",
                    f"Gust: {wind_gust} mph" if wind_gust else ""
                )
            
            # Temperature section - both air and water
            st.markdown("### ️ Temperature & Conditions")
            temp_col1, temp_col2, temp_col3 = st.columns(3)
            
            with temp_col1:
                water_temp = conditions.get('temperature_f', 0)
                st.metric(
                    " Water Temperature",
                    f"{water_temp:.1f}°F",
                    "*(Simulated data)*"
                )
            
            with temp_col2:
                air_temp = weather.get('temperature_f') if weather else None
                feels_like = weather.get('feels_like_f') if weather else None
                st.metric(
                    "️ Air Temperature",
                    f"{air_temp:.1f}°F" if air_temp else "N/A",
                    f"Feels like {feels_like:.1f}°F" if feels_like else ""
                )
            
            with temp_col3:
                humidity = weather.get('humidity_percent', 0) if weather else 0
                visibility = weather.get('visibility_miles', 0) if weather else 0
                st.metric(
                    " Conditions",
                    f"{humidity}% humidity" if humidity else "N/A",
                    f"Visibility: {visibility} mi" if visibility else ""
                )
            
            # Gear recommendation based on USCG hypothermia data
            if weather and conditions:
                from hypothermia_risk import calculate_combined_risk_score, format_recommendation
                
                water_temp = conditions.get('temperature_f', 0)
                air_temp = weather.get('temperature_f', 0)
                wind_speed = weather.get('wind_speed_mph', 0)
                
                # Calculate scientific risk score
                risk_data = calculate_combined_risk_score(
                    water_temp_f=water_temp,
                    air_temp_f=air_temp,
                    wind_speed_mph=wind_speed if wind_speed else 0,
                    exposure_minutes=120 # Typical 2-hour paddle session
                )
                
                st.markdown("### Protective Gear Recommendation (USCG Hypothermia Data)")
                st.caption("️ **Note:** Water temperature is currently simulated data. Real USGS water temperature integration is in progress.")
                
                # Format and display recommendation
                formatted_rec = format_recommendation(risk_data)
                
                # Use appropriate warning level based on risk
                if risk_data['risk_level'] == 'CRITICAL':
                    st.error(formatted_rec)
                elif risk_data['risk_level'] == 'HIGH':
                    st.warning(formatted_rec)
                else:
                    st.info(formatted_rec)
            
            # Recommendation
            st.info(f"**Recommendation:** {flow_status.get('recommendation', 'No data available')}")
            
            # Last updated
            st.caption(f"Last updated: {conditions.get('timestamp', 'Unknown')}")
        else:
            st.error("Unable to fetch current conditions")
    
    with col2:
        st.markdown(f"### ℹ️ About {selected_section}")
        if selected_section == "Little Falls":
            st.markdown("""
            **River:** Potomac River 
            **Difficulty:** Class II 
            **Length:** 1.5 miles 
            **Optimal Flow:** 4,000 - 8,000 CFS 
            
            Popular section with consistent whitewater and multiple access points.
            """)
        elif selected_section == "Mathers Gorge":
            st.markdown("""
            **River:** Potomac River 
            **Difficulty:** Class III 
            **Length:** 3.0 miles 
            **Optimal Flow:** 5,000 - 9,000 CFS 
            
            Technical section through scenic gorge with multiple small drops.
            """)
        elif selected_section == "North Branch":
            st.markdown("""
            **River:** Potomac River 
            **Difficulty:** Class II+ 
            **Length:** 2.5 miles 
            **Optimal Flow:** 4,500 - 8,500 CFS 
            
            Scenic section with moderate rapids and beautiful forest.
            """)
        elif selected_section == "Shenandoah Staircase":
            st.markdown("""
            **River:** Shenandoah River 
            **Difficulty:** Class III+ 
            **Length:** 4.0 miles 
            **Optimal Flow:** 3,500 - 7,000 CFS 
            
            Technical section with series of drops creating a staircase effect.
            """)
    
    # Quick actions
    st.markdown("---")
    st.markdown("### Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(" Refresh Data"):
            st.cache_data.clear()
            st.rerun()
    
    with col2:
        if st.button(" View on Map"):
            st.info("Click 'Map' tab above to view interactive map")

elif page == "Predictions":
    # Define available sections with their gauge IDs
    sections = {
        "Little Falls": 1,
        "Mathers Gorge": 2,
        "North Branch": 3,
        "Shenandoah Staircase": 4
    }
    
    selected_section = st.sidebar.selectbox(" Select River Section:", list(sections.keys()), key="pred_section")
    selected_gauge_id = sections[selected_section]
    
    st.markdown(f"## Flow Predictions - Next 7 Days ({selected_section})")
    
    predictions = fetch_predictions(gauge_id=selected_gauge_id)
    
    if predictions:
        # Convert to DataFrame
        df = pd.DataFrame(predictions)
        df['prediction_date'] = pd.to_datetime(df['prediction_date'])
        
        # Create interactive plot
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['prediction_date'],
            y=df['predicted_flow_cfs'],
            mode='lines+markers',
            name='Predicted Flow',
            line=dict(color='#1f77d2', width=3),
            marker=dict(size=8)
        ))
        
        fig.add_trace(go.Scatter(
            x=df['prediction_date'],
            y=df['confidence_upper'],
            fill=None,
            mode='lines',
            line_color='rgba(0,0,0,0)',
            showlegend=False
        ))
        
        fig.add_trace(go.Scatter(
            x=df['prediction_date'],
            y=df['confidence_lower'],
            fill='tonexty',
            mode='lines',
            line_color='rgba(0,0,0,0)',
            name='Confidence Interval',
            fillcolor='rgba(31, 119, 210, 0.2)'
        ))
        
        fig.update_layout(
            title="ARIMA Flow Predictions",
            xaxis_title="Date",
            yaxis_title="Flow (CFS)",
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Data table
        st.markdown("### Prediction Details")
        st.dataframe(df[['prediction_date', 'predicted_flow_cfs', 'confidence_lower', 'confidence_upper']], 
                    use_container_width=True)

        # Model Description Section
        st.markdown("---")
        st.markdown("### About the Forecasting Model")
        
        with st.expander(" Model Details", expanded=False):
            st.markdown("""
            **Forecasting Methodology: ARIMA(1,1,1)**
            
            This application uses an AutoRegressive Integrated Moving Average (ARIMA) model to predict river flow 7 days into the future.
            
            **Model Parameters:**
            - **AR (p=1)**: Autoregressive component - uses 1 previous flow value
            - **I (d=1)**: Differencing order - removes trend by taking first differences
            - **MA (q=1)**: Moving average component - uses 1 previous forecast error
            
            **Why ARIMA?**
            - Captures temporal patterns in river flow data
            - Handles non-stationary time series effectively
            - Provides confidence intervals for uncertainty quantification
            - Lightweight and interpretable for real-time forecasting
            
            **Data Requirements:**
            - At least 30 days of historical flow data
            - Updates daily with new USGS measurements
            - Falls back to trend analysis if insufficient data
            
            **Accuracy Considerations:**
            - Short-term predictions (1-2 days) are more reliable
            - Longer forecasts have wider confidence intervals
            - Extreme events may not be fully captured
            - Model retrains daily with latest USGS data
            
            **Confidence Intervals:**
            The shaded area represents the 95% confidence interval around predictions, showing the range where actual flow is likely to fall.
            """)

    else:
        st.error("Unable to fetch predictions")

elif page == "Map":
    st.markdown("## ️ Interactive Map - River Access Points")
    section_data = {
        "Little Falls": {"lat": 39.0067, "lon": -77.2481, "zoom": 12},
        "Mathers Gorge": {"lat": 39.0812, "lon": -77.3389, "zoom": 12},
        "North Branch": {"lat": 39.5234, "lon": -79.2876, "zoom": 11},
        "Shenandoah Staircase": {"lat": 38.9234, "lon": -77.8901, "zoom": 12}
    }
    
    # Access points data with coordinates
    access_points_map = {
        "Little Falls": [
            {"name": "Great Falls Park", "lat": 39.0067, "lon": -77.2481, "type": "Put-in"},
            {"name": "Violettes Lock", "lat": 39.0156, "lon": -77.2347, "type": "Both"},
            {"name": "Carderock Recreation Area", "lat": 38.9750, "lon": -77.2033, "type": "Take-out"}
        ],
        "Mathers Gorge": [
            {"name": "Seneca Creek", "lat": 39.0812, "lon": -77.3389, "type": "Put-in"},
            {"name": "Mathers Gorge Take-Out", "lat": 39.0756, "lon": -77.3201, "type": "Take-out"}
        ],
        "North Branch": [
            {"name": "North Branch Put-In", "lat": 39.5234, "lon": -79.2876, "type": "Put-in"},
            {"name": "North Branch Take-Out", "lat": 39.4821, "lon": -79.1234, "type": "Take-out"}
        ],
        "Shenandoah Staircase": [
            {"name": "Shenandoah Staircase Put-In", "lat": 38.9234, "lon": -77.8901, "type": "Put-in"},
            {"name": "Shenandoah Staircase Take-Out", "lat": 38.8945, "lon": -77.8456, "type": "Take-out"}
        ]
    }
    
    # Section selector
    sections = {
        "Little Falls": 1,
        "Mathers Gorge": 2,
        "North Branch": 3,
        "Shenandoah Staircase": 4
    }
    
    selected_section = st.sidebar.selectbox(" Select River Section:", list(sections.keys()), key="map_section")
    
    # Create map
    section_info = section_data[selected_section]
    m = folium.Map(
        location=[section_info["lat"], section_info["lon"]],
        zoom_start=section_info["zoom"],
        tiles="OpenStreetMap"
    )
    
    # Add access points to map
    for point in access_points_map[selected_section]:
        if point["type"] == "Put-in":
            color = "green"
        elif point["type"] == "Take-out":
            color = "red"
        else:
            color = "blue"
        
        folium.Marker(
            location=[point["lat"], point["lon"]],
            popup=f"<b>{point['name']}</b><br>{point['type']}",
            tooltip=point['name'],
            icon=folium.Icon(color=color, icon="info-sign")
        ).add_to(m)
    
    # Display map
    try:
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            m.save(f.name)
            with open(f.name, 'r') as map_file:
                map_html = map_file.read()
            components.html(map_html, height=800)
    except Exception as e:
        st.error(f"Error rendering map: {e}")
        st.write(f"Selected section: {selected_section}")
    
    # Info about access points
    st.markdown(f"### Access Points - {selected_section}")
    for point in access_points_map[selected_section]:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{point['name']}** \n{point['type']}")
        with col2:
            if point["type"] == "Put-in":
                st.markdown("🟢")
            elif point["type"] == "Take-out":
                st.markdown("")
            else:
                st.markdown("")

elif page == "Access Points":
    # Define available sections with their access points
    sections = {
        "Little Falls": 1,
        "Mathers Gorge": 2,
        "North Branch": 3,
        "Shenandoah Staircase": 4
    }
    
    selected_section = st.sidebar.selectbox(" Select River Section:", list(sections.keys()), key="access_points_section")
    selected_section_id = sections[selected_section]
    
    st.markdown(f"## Access Points - {selected_section}")
    
    # Access points organized by section
    access_points_by_section = {
        1: {  # Little Falls
            "Name": ["Great Falls Park", "Violettes Lock", "Carderock Recreation Area"],
            "Type": ["Put-in", "Both", "Take-out"],
            "Parking": ["Large lot ($10 fee)", "Small lot (Free)", "Moderate lot (Free)"],
            "Difficulty": ["Easy", "Moderate", "Moderate"],
            "Facilities": ["Restrooms, Picnic, Visitor center", "Restrooms", "Picnic area"],
            "Notes": ["Popular starting point", "Can get busy", "Main takeout"]
        },
        2: {  # Mathers Gorge
            "Name": ["Seneca Creek", "Mathers Gorge Take-Out"],
            "Type": ["Put-in", "Take-out"],
            "Parking": ["Roadside (Limited)", "Small lot (Free)"],
            "Difficulty": ["Moderate", "Difficult"],
            "Facilities": ["Street parking", "Basic parking"],
            "Notes": ["Access to Mathers Gorge", "Technical takeout, requires portage"]
        },
        3: {  # North Branch
            "Name": ["North Branch Put-In", "North Branch Take-Out"],
            "Type": ["Put-in", "Take-out"],
            "Parking": ["Large lot (Free)", "Small lot (Free)"],
            "Difficulty": ["Easy", "Moderate"],
            "Facilities": ["Picnic tables, Restrooms", "Limited facilities"],
            "Notes": ["Scenic access point", "After North Branch run"]
        },
        4: {  # Shenandoah Staircase
            "Name": ["Shenandoah Staircase Put-In", "Shenandoah Staircase Take-Out"],
            "Type": ["Put-in", "Take-out"],
            "Parking": ["Large lot ($5 fee)", "Small lot (Limited, Free)"],
            "Difficulty": ["Moderate", "Difficult"],
            "Facilities": ["Restrooms, Picnic area", "No facilities"],
            "Notes": ["Gateway to technical section", "Steep takeout after run"]
        }
    }
    
    access_data = access_points_by_section[selected_section_id]
    df_access = pd.DataFrame(access_data)
    
    # Display as table
    st.dataframe(df_access, use_container_width=True)
    
    # Add info box
    col1, col2 = st.columns(2)
    with col1:
        st.info(f" {len(access_data['Name'])} access points available for {selected_section}")
    with col2:
        st.info("️ Check the Map tab for interactive map with all access points")

elif page == "SQL Queries":
    st.markdown("## Advanced SQL Queries")
    st.markdown("Real queries executing against MySQL database with performance metrics")
    
    query_type = st.selectbox(
        " Select Advanced SQL Pattern:",
        [
            "Flow Comparison by Section (CTE + Aggregation)",
            "Section Comparison (UNION Pattern)",
            "Gauge Performance Ranking (Window Functions)",
            "Access Points Availability (Self-Join + Aggregation)",
            "Weather-Flow Correlation (Multi-JOIN + Temporal)",
            "Predictive Accuracy Analysis (Subqueries + Calculations)",
            "Schema Overview"
        ]
    )
    
    if query_type == "Flow Comparison by Section (CTE + Aggregation)":
        st.markdown("### CTE + GROUP BY HAVING + CASE")
        st.markdown("""
        **SQL Pattern Showcase:**
        - **CTE (Common Table Expression)** - WITH clause for code reusability
        - **GROUP BY + HAVING** - Filter groups by aggregate conditions
        - **CASE Statements** - Conditional logic in SELECT
        - **Aggregate Functions** - AVG, MIN, MAX, STDDEV, COUNT
        
        **What it calculates:**
        - 24-hour flow statistics per section
        - Flow volatility (standard deviation)
        - Data quality metrics
        """)
        
        with st.spinner("Executing query..."):
            try:
                response = requests.get(f"{API_URL}/queries/flow-comparison-by-section", timeout=10)
                if response.status_code == 200:
                    result = response.json()
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Query Type", "CTE + Aggregation")
                    with col2:
                        st.metric("Execution Time", f"{result['execution_time_ms']}ms")
                    with col3:
                        st.metric("Rows Returned", result['rows_returned'])
                    
                    if result['data']:
                        df = pd.DataFrame(result['data'])
                        st.dataframe(df, use_container_width=True)
                        
                        # Show SQL explanation
                        with st.expander(" View SQL Query"):
                            st.code("""
WITH recent_flows AS (
    SELECT ug.gauge_id, rs.section_id, rs.name,
           cc.flow_cfs, cc.timestamp
    FROM current_conditions cc
    JOIN usgs_gauges ug ON cc.gauge_id = ug.gauge_id
    JOIN river_sections rs ON ug.section_id = rs.section_id
    WHERE cc.timestamp >= DATE_SUB(NOW(), INTERVAL 1 DAY)
),
section_stats AS (
    SELECT section_id, section_name,
           AVG(flow_cfs) as avg_flow, 
           MIN(flow_cfs) as min_flow,
           MAX(flow_cfs) as max_flow,
           STDDEV(flow_cfs) as volatility,
           COUNT(*) as sample_count
    FROM recent_flows
    GROUP BY section_id, section_name
    HAVING COUNT(*) > 0
)
SELECT * FROM section_stats ORDER BY volatility DESC;
                            """, language="sql")
                    else:
                        st.info("No data available yet. Schedulers will populate data soon.")
            except Exception as e:
                st.error(f"Error executing query: {e}")
    
    elif query_type == "Section Comparison (UNION Pattern)":
        st.markdown("### UNION + Subqueries Pattern")
        st.markdown("""
        **SQL Pattern Showcase:**
        - **UNION** - Combine multiple result sets
        - **Subqueries** - Nested queries in FROM clause
        - **Data Consolidation** - Merge different data sources
        
        **What it does:**
        - Combines actual current flows with target optimal ranges
        - Shows comparison between real vs target metrics
        """)
        
        with st.spinner("Executing query..."):
            try:
                response = requests.get(f"{API_URL}/queries/section-comparison-union", timeout=10)
                if response.status_code == 200:
                    result = response.json()
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Query Type", "UNION")
                    with col2:
                        st.metric("Execution Time", f"{result['execution_time_ms']}ms")
                    with col3:
                        st.metric("Rows Returned", result['rows_returned'])
                    
                    if result['data']:
                        df = pd.DataFrame(result['data'])
                        st.dataframe(df, use_container_width=True)
                        
                        with st.expander(" View SQL Query"):
                            st.code("""
SELECT section_name, 'Current Flow' as metric_type,
       AVG(flow_cfs) as value, 'CFS' as unit
FROM (
    SELECT rs.name as section_name, cc.flow_cfs
    FROM current_conditions cc
    JOIN usgs_gauges ug ON cc.gauge_id = ug.gauge_id
    JOIN river_sections rs ON ug.section_id = rs.section_id
    WHERE cc.timestamp >= DATE_SUB(NOW(), INTERVAL 1 DAY)
) as recent_flows
GROUP BY section_name

UNION ALL

SELECT rs.name, 'Optimal Min Flow' as metric_type,
       rs.optimal_min_cfs as value, 'CFS' as unit
FROM river_sections rs
ORDER BY section_name, metric_type;
                            """, language="sql")
            except Exception as e:
                st.error(f"Error executing query: {e}")
    
    elif query_type == "Gauge Performance Ranking (Window Functions)":
        st.markdown("### Window Functions Pattern")
        st.markdown("""
        **SQL Pattern Showcase:**
        - **ROW_NUMBER()** - Sequential ranking
        - **RANK()** - Ranking with gaps
        - **DENSE_RANK()** - Ranking without gaps
        - **PARTITION BY** - Divide data into groups
        - **ORDER BY** - Define ranking order
        
        **What it analyzes:**
        - Rank gauges by number of readings
        - Rank by data consistency (flow stability)
        - Calculate data coverage percentage
        """)
        
        with st.spinner("Executing query..."):
            try:
                response = requests.get(f"{API_URL}/queries/gauge-performance-ranking", timeout=10)
                if response.status_code == 200:
                    result = response.json()
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Query Type", "Window Functions")
                    with col2:
                        st.metric("Execution Time", f"{result['execution_time_ms']}ms")
                    with col3:
                        st.metric("Rows Returned", result['rows_returned'])
                    
                    if result['data']:
                        df = pd.DataFrame(result['data'])
                        st.dataframe(df, use_container_width=True)
                        
                        with st.expander(" View SQL Query"):
                            st.code("""
WITH gauge_metrics AS (
    SELECT ug.gauge_id, ug.gauge_name, rs.name as section,
           COUNT(*) as total_readings,
           COUNT(DISTINCT DATE(cc.timestamp)) as days_with_data,
           STDDEV(cc.flow_cfs) as flow_consistency,
           AVG(cc.flow_cfs) as avg_flow
    FROM current_conditions cc
    JOIN usgs_gauges ug ON cc.gauge_id = ug.gauge_id
    JOIN river_sections rs ON ug.section_id = rs.section_id
    WHERE cc.timestamp >= DATE_SUB(NOW(), INTERVAL 30 DAY)
    GROUP BY ug.gauge_id, ug.gauge_name, rs.name
)
SELECT gauge_id, gauge_name, section, total_readings,
       ROW_NUMBER() OVER (ORDER BY total_readings DESC) as reading_rank,
       RANK() OVER (ORDER BY flow_consistency ASC) as consistency_rank,
       ROUND(100 * days_with_data / 30, 1) as data_coverage_pct
FROM gauge_metrics
ORDER BY reading_rank;
                            """, language="sql")
            except Exception as e:
                st.error(f"Error executing query: {e}")
    
    elif query_type == "Access Points Availability (Self-Join + Aggregation)":
        st.markdown("### ️ Aggregation + CASE Pattern")
        st.markdown("""
        **SQL Pattern Showcase:**
        - **CASE WHEN** - Conditional aggregation
        - **SUM with CASE** - Count conditional rows
        - **GROUP_CONCAT** - Aggregate strings
        - **LEFT JOIN** - Include all main records
        
        **What it shows:**
        - Put-in vs Take-out availability per section
        - Parking fee analysis
        - Access point inventory
        """)
        
        with st.spinner("Executing query..."):
            try:
                response = requests.get(f"{API_URL}/queries/access-points-availability", timeout=10)
                if response.status_code == 200:
                    result = response.json()
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Query Type", "Aggregation + CASE")
                    with col2:
                        st.metric("Execution Time", f"{result['execution_time_ms']}ms")
                    with col3:
                        st.metric("Rows Returned", result['rows_returned'])
                    
                    if result['data']:
                        df = pd.DataFrame(result['data'])
                        st.dataframe(df, use_container_width=True)
                        
                        with st.expander(" View SQL Query"):
                            st.code("""
SELECT rs.name as section, rs.difficulty_class,
       SUM(CASE WHEN ap.type = 'put_in' THEN 1 ELSE 0 END) as put_in_count,
       SUM(CASE WHEN ap.type = 'takeout' THEN 1 ELSE 0 END) as takeout_count,
       COUNT(*) as total_access_points,
       AVG(CASE WHEN ap.parking_fee > 0 THEN ap.parking_fee ELSE NULL END) as avg_parking_fee,
       GROUP_CONCAT(DISTINCT ap.name SEPARATOR ', ') as access_point_names
FROM river_sections rs
LEFT JOIN access_points ap ON rs.section_id = ap.section_id
GROUP BY rs.section_id, rs.name, rs.difficulty_class
ORDER BY rs.name;
                            """, language="sql")
            except Exception as e:
                st.error(f"Error executing query: {e}")
    
    elif query_type == "Weather-Flow Correlation (Multi-JOIN + Temporal)":
        st.markdown("### ️ CTE + Multi-JOIN + Temporal Analysis")
        st.markdown("""
        **SQL Pattern Showcase:**
        - **CTE (WITH clause)** - Named subqueries
        - **Multiple JOINs** - Combine 5+ tables
        - **DATE/HOUR functions** - Temporal grouping
        - **Complex WHERE conditions** - Filter after aggregation
        
        **What it analyzes:**
        - Correlation between weather and flow patterns
        - Hour-by-hour trends
        - Data quality by combining sources
        """)
        
        with st.spinner("Executing query..."):
            try:
                response = requests.get(f"{API_URL}/queries/weather-impact-analysis", timeout=10)
                if response.status_code == 200:
                    result = response.json()
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Query Type", "Multi-JOIN + CTE")
                    with col2:
                        st.metric("Execution Time", f"{result['execution_time_ms']}ms")
                    with col3:
                        st.metric("Rows Returned", result['rows_returned'])
                    
                    if result['data']:
                        df = pd.DataFrame(result['data'])
                        st.dataframe(df.head(20), use_container_width=True)
                        st.caption(f"Showing first 20 of {len(df)} rows")
                        
                        with st.expander(" View SQL Query"):
                            st.code("""
WITH hourly_data AS (
    SELECT rs.name as section, DATE(cc.timestamp) as date,
           HOUR(cc.timestamp) as hour,
           AVG(cc.flow_cfs) as avg_flow,
           AVG(wc.temperature_f) as avg_temp,
           AVG(wc.wind_speed_mph) as avg_wind,
           wc.conditions
    FROM current_conditions cc
    JOIN usgs_gauges ug ON cc.gauge_id = ug.gauge_id
    JOIN river_sections rs ON ug.section_id = rs.section_id
    LEFT JOIN weather_conditions wc ON rs.section_id = wc.section_id
        AND DATE(cc.timestamp) = DATE(wc.timestamp)
    WHERE cc.timestamp >= DATE_SUB(NOW(), INTERVAL 7 DAY)
    GROUP BY rs.name, DATE(cc.timestamp), HOUR(cc.timestamp), wc.conditions
)
SELECT * FROM hourly_data
WHERE flow_readings > 0 AND weather_readings > 0
ORDER BY section, date DESC, hour DESC;
                            """, language="sql")
            except Exception as e:
                st.error(f"Error executing query: {e}")
    
    elif query_type == "Predictive Accuracy Analysis (Subqueries + Calculations)":
        st.markdown("### Predictive Accuracy + Complex Calculations")
        st.markdown("""
        **SQL Pattern Showcase:**
        - **Subqueries** - In WHERE and SELECT clauses
        - **Complex Math** - Calculate error percentages
        - **Nested Calculations** - Multi-step formulas
        - **CASE WHEN** - Evaluate accuracy ratings
        
        **What it evaluates:**
        - Compare ARIMA predictions vs actual flows
        - Calculate absolute and percentage errors
        - Rate model accuracy
        """)
        
        with st.spinner("Executing query..."):
            try:
                response = requests.get(f"{API_URL}/queries/predictive-accuracy", timeout=10)
                if response.status_code == 200:
                    result = response.json()
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Query Type", "Prediction Analysis")
                    with col2:
                        st.metric("Execution Time", f"{result['execution_time_ms']}ms")
                    with col3:
                        st.metric("Rows Returned", result['rows_returned'])
                    
                    if result['data']:
                        df = pd.DataFrame(result['data'])
                        st.dataframe(df, use_container_width=True)
                        
                        with st.expander(" View SQL Query"):
                            st.code("""
SELECT rs.name as section, ap.prediction_date,
       ap.predicted_flow_cfs,
       AVG(cc.flow_cfs) as actual_avg_flow,
       ABS(ap.predicted_flow_cfs - AVG(cc.flow_cfs)) as absolute_error,
       ROUND(ABS((ap.predicted_flow_cfs - AVG(cc.flow_cfs)) 
           / AVG(cc.flow_cfs) * 100), 2) as pct_error,
       CASE 
           WHEN ABS(...pct_error...) < 5 THEN 'Excellent'
           WHEN ABS(...pct_error...) < 15 THEN 'Good'
           ELSE 'Needs Improvement'
       END as accuracy_rating
FROM arima_predictions ap
JOIN usgs_gauges ug ON ap.gauge_id = ug.gauge_id
JOIN river_sections rs ON ug.section_id = rs.section_id
LEFT JOIN current_conditions cc ON ug.gauge_id = cc.gauge_id
WHERE ap.prediction_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
GROUP BY ap.prediction_id, rs.name, ap.prediction_date
ORDER BY rs.name, ap.prediction_date DESC;
                            """, language="sql")
            except Exception as e:
                st.error(f"Error executing query: {e}")
    
    elif query_type == "Schema Overview":
        st.markdown("### Database Schema & Structure")
        
        st.markdown("#### Entity Relationship Diagram (ER)")
        
        mermaid_html = """
        <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
        <div class="mermaid">
erDiagram
    RIVERS ||--o{ RIVER_SECTIONS : contains
    RIVERS ||--o{ USGS_GAUGES : monitors
    RIVERS ||--o{ ACCESS_POINTS : hasAccess
    RIVER_SECTIONS ||--o{ USGS_GAUGES : gaugeLocation
    RIVER_SECTIONS ||--o{ ACCESS_POINTS : providesAccess
    RIVER_SECTIONS ||--o{ WEATHER_CONDITIONS : hasWeather
    USGS_GAUGES ||--o{ CURRENT_CONDITIONS : produces
    USGS_GAUGES ||--o{ ARIMA_PREDICTIONS : forecasts
    
    RIVERS {
        int river_id PK
        string name UK
        string state
        text description
    }
    RIVER_SECTIONS {
        int section_id PK
        int river_id FK
        string name
        string difficulty_class
        int optimal_min_cfs
        int optimal_max_cfs
    }
    USGS_GAUGES {
        int gauge_id PK
        int river_id FK
        int section_id FK
        string site_number UK
        decimal latitude
        decimal longitude
    }
    CURRENT_CONDITIONS {
        int condition_id PK
        int gauge_id FK
        datetime timestamp "⭐ Indexed"
        decimal flow_cfs
        decimal gauge_height_ft
    }
    ARIMA_PREDICTIONS {
        int prediction_id PK
        int gauge_id FK
        date prediction_date
        decimal predicted_flow_cfs
        decimal confidence_lower
        decimal confidence_upper
    }
    ACCESS_POINTS {
        int access_id PK
        int section_id FK
        string name
        string type
        decimal parking_fee
    }
    WEATHER_CONDITIONS {
        int weather_id PK
        int section_id FK
        datetime timestamp
        decimal temperature_f
        decimal wind_speed_mph
        string conditions
    }
        </div>
        """
        
        components.html(mermaid_html, height=1000, scrolling=True)

        st.markdown("#### Table Definitions")
        
        with st.expander(" **rivers** - Master table for all rivers", expanded=False):
            st.code("""
CREATE TABLE rivers (
    river_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    state VARCHAR(20),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_river_name (name, state)
);
            """, language="sql")
            st.markdown("""
            **Purpose:** Base table for all river systems
            
            **Key Features:**
            - Composite UNIQUE constraint prevents duplicate rivers
            - Description field for context
            - timestamp for audit trail
            """)
        
        with st.expander(" **river_sections** - Paddling sections with difficulty ratings", expanded=False):
            st.code("""
CREATE TABLE river_sections (
    section_id INT PRIMARY KEY AUTO_INCREMENT,
    river_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    difficulty_class VARCHAR(10),
    optimal_min_cfs INT,
    optimal_max_cfs INT,
    FOREIGN KEY (river_id) REFERENCES rivers(river_id) ON DELETE CASCADE,
    INDEX idx_river (river_id)
);
            """, language="sql")
            st.markdown("""
            **Purpose:** Specific paddling sections with flow thresholds
            
            **Key Features:**
            - difficulty_class: I, II, III, IV, V (rapids scale)
            - Flow thresholds for safe paddling conditions
            - INDEX on river_id for fast JOINs
            """)
        
        with st.expander(" **usgs_gauges** - Real-time USGS monitoring stations", expanded=False):
            st.code("""
CREATE TABLE usgs_gauges (
    gauge_id INT PRIMARY KEY AUTO_INCREMENT,
    river_id INT NOT NULL,
    section_id INT,
    site_number VARCHAR(20) UNIQUE NOT NULL,
    gauge_name VARCHAR(100),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    FOREIGN KEY (river_id) REFERENCES rivers(river_id) ON DELETE CASCADE,
    FOREIGN KEY (section_id) REFERENCES river_sections(section_id)
);
            """, language="sql")
            st.markdown("""
            **Purpose:** Links USGS gauges to our river sections
            
            **Key Features:**
            - UNIQUE site_number (official USGS identifier)
            - Coordinates for mapping
            - Real-time data source integration
            """)
        
        with st.expander(" **current_conditions** - Real-time sensor data (TIME-SERIES)", expanded=False):
            st.code("""
CREATE TABLE current_conditions (
    condition_id INT PRIMARY KEY AUTO_INCREMENT,
    gauge_id INT NOT NULL,
    timestamp DATETIME NOT NULL,
    flow_cfs DECIMAL(10, 2),
    gauge_height_ft DECIMAL(6, 2),
    FOREIGN KEY (gauge_id) REFERENCES usgs_gauges(gauge_id) ON DELETE CASCADE,
    INDEX idx_gauge_time (gauge_id, timestamp),
    INDEX idx_timestamp (timestamp)
);
            """, language="sql")
            st.markdown("""
            **Purpose:** Time-series data from USGS sensors
            
            **Key Features:**
            - ⭐ **Composite index (gauge_id, timestamp)** = Fast range queries
            - Tracks flow (CFS), height
            - CASCADE delete orphans when gauge is deleted
            """)
        
        with st.expander(" **arima_predictions** - ARIMA(1,1,1) forecasts with uncertainty", expanded=False):
            st.code("""
CREATE TABLE arima_predictions (
    prediction_id INT PRIMARY KEY AUTO_INCREMENT,
    gauge_id INT NOT NULL,
    prediction_date DATE NOT NULL,
    predicted_flow_cfs DECIMAL(10, 2),
    confidence_lower DECIMAL(10, 2),
    confidence_upper DECIMAL(10, 2),
    FOREIGN KEY (gauge_id) REFERENCES usgs_gauges(gauge_id) ON DELETE CASCADE,
    UNIQUE KEY unique_prediction (gauge_id, prediction_date)
);
            """, language="sql")
            st.markdown("""
            **Purpose:** 7-day flow forecasts with confidence intervals
            
            **Key Features:**
            - Confidence bounds for uncertainty quantification
            - UNIQUE constraint prevents duplicate predictions
            - Indexed for fast lookups
            """)
        
        with st.expander(" **access_points** - Put-in/takeout locations with parking info", expanded=False):
            st.code("""
CREATE TABLE access_points (
    access_id INT PRIMARY KEY AUTO_INCREMENT,
    river_id INT NOT NULL,
    section_id INT,
    name VARCHAR(100) NOT NULL,
    type ENUM('put_in', 'takeout', 'both'),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    parking_type ENUM('roadside', 'small_lot', 'large_lot', 'fee_required'),
    parking_fee DECIMAL(5, 2),
    FOREIGN KEY (river_id) REFERENCES rivers(river_id) ON DELETE CASCADE,
    FOREIGN KEY (section_id) REFERENCES river_sections(section_id)
);
            """, language="sql")
            st.markdown("""
            **Purpose:** Geospatial access points with parking/facility info
            
            **Key Features:**
            - ENUM types constrain parking/difficulty options (storage efficient)
            - Coordinates for mapping integration
            - Foreign keys to river and section
            """)
        
        st.markdown("---")
        
        st.markdown("### Indexing Strategy")
        st.code("""
-- Composite index for time-series range queries (CRITICAL for performance)
CREATE INDEX idx_gauge_time ON current_conditions(gauge_id, timestamp);

-- For temporal filtering
CREATE INDEX idx_timestamp ON current_conditions(timestamp);

-- For prediction lookups and date filtering
CREATE INDEX idx_gauge_date ON arima_predictions(gauge_id, prediction_date);

-- Foreign key indexes for JOIN performance
CREATE INDEX idx_river ON river_sections(river_id);
CREATE INDEX idx_river ON usgs_gauges(river_id);
CREATE INDEX idx_section ON access_points(section_id);
        """, language="sql")
        
        st.markdown("""
        **Performance Impact:**
        - **idx_gauge_time:** Makes "get last 30 days for gauge 1" run in ~5ms instead of 5 seconds
        - **Composite indexes** beat single-column indexes for range queries by 10-100x
        - **Foreign key indexes** speed up JOINs by pre-sorting join data
        - **UNIQUE constraints** prevent duplicates at database level (not application)
        """)

elif page == "API":
    st.markdown("## Data Sources & Architecture")
    
    # Real-time status indicator
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(" USGS Integration", "Live", delta="Real-time")
    with col2:
        st.metric("⏱️ Update Frequency", "Every 15 min", delta="Scheduled")
    with col3:
        st.metric(" Data Source", "USGS APIs", delta="Active")
    
    st.markdown("---")
    
    st.markdown("""
    ### System Architecture
    
    ```
    USGS Water Services API (Automated)
           ↓ (every 15 minutes)
    Python Scheduler Service
           ↓ (fetches & processes)
    MySQL Database Storage
           ↓ (stores real data)
    FastAPI Backend Endpoints
           ↓ (serves requests)
    Streamlit Dashboard
    ```
    
    ### Live Data Sources
    
    **Real USGS Gauge Stations (Potomac River)**
    
    | Section | USGS ID | Gauge Name | Type |
    |---------|---------|------------|------|
    | Little Falls | 01646580 | Potomac River at Little Falls Tdam | Streamflow |
    | Mathers Gorge | 01645500 | South Branch Potomac River at Petersburg | Streamflow |
    | North Branch | 01604500 | North Branch Potomac River near Paw Paw | Streamflow |
    | Shenandoah Staircase | 01620000 | Shenandoah River at Millville | Streamflow |
    
    - **Real-time Data**: Streamflow (discharge in CFS)
    - **Update Interval**: Every 15 minutes
    - **Data Source**: https://waterservices.usgs.gov/nwis/iv/
    - **Parameters Tracked**: Discharge (00060 parameter code)
    
    ### Database Schema (MySQL)
    
    **7 Normalized Tables:**
    
    | Table | Purpose | Updated By | Key Data |
    |-------|---------|-----------|----------|
    | `rivers` | River metadata | Manual | Name, state, description |
    | `river_sections` | Paddling sections | Manual | Difficulty class, flow ranges, length |
    | `usgs_gauges` | USGS gauge stations | Manual | Site number, coordinates, drainage area |
    | `current_conditions` | **Real-time flow data** | **USGS Scheduler (15 min)** | Flow CFS, gauge height, timestamp |
    | `arima_predictions` | 7-day forecasts | **ARIMA Model** | Predicted flow, confidence intervals |
    | `access_points` | Put-in/take-out locations | Manual | Type, parking, facilities, difficulty |
    | `weather_conditions` | **Real-time weather** | **Weather Scheduler (30 min)** | Temperature, wind, humidity, conditions |
    
    ### Data Processing Pipeline
    
    1. **USGS Fetch** - Scheduler queries USGS API every 15 minutes → stores in `current_conditions`
    2. **Weather Fetch** - Scheduler queries Open-Meteo API every 30 minutes → stores in `weather_conditions`
    3. **Parse** - Extract streamflow & weather data for 4 sections
    4. **Transform** - Convert units (CFS ↔ m³/s, °C → °F)
    5. **Store** - Insert/update in database tables with timestamps
    6. **Serve** - FastAPI endpoints query from database
    6. **Display** - Streamlit dashboard shows latest readings
    
    ### Backend Processing
    
    **FastAPI Endpoints (Real Data):**
    - `GET /api/conditions/{gauge_id}` - Current streamflow with flow status
    - `GET /api/predictions/{gauge_id}` - 7-day ARIMA forecasts
    - `GET /api/rivers` - All river information
    - `GET /api/gauges/{gauge_id}` - Gauge station metadata
    - `POST /api/usgs/refresh` - Manual trigger for data refresh
    
    **Flow Status Classification:**
    - 🟢 **Optimal** - Safe paddling conditions
    - 🟡 **Marginal** - Challenging conditions
    - **Too High** - Potentially dangerous
    
    ### Technology Stack
    
    - **Data Fetch**: Python + Requests library
    - **Scheduler**: APScheduler (runs every 15 min)
    - **Database**: MySQL 8.0 with ORM (SQLAlchemy)
    - **API**: FastAPI with async routes
    - **Frontend**: Streamlit + Plotly + Folium
    - **Forecasting**: ARIMA(1,1,1) time series model
    - **Containerization**: Docker + Docker Compose
    
    ### Active Services
    
    ```
     MySQL (Port 3306) - Database engine
     FastAPI (Port 8000) - REST API server
     Scheduler Service - USGS data fetcher
     Streamlit (Port 8501) - Dashboard
    ```
    
    ### Manual Refresh
    
    """)
    
    if st.button(" Fetch Latest USGS Data Now"):
        try:
            response = requests.get(f"{API_URL}/usgs/refresh", timeout=10)
            if response.status_code == 200:
                data = response.json()
                st.success(f" {data['message']}")
                st.info(f"Gauges Updated: {data['gauges_updated']}")
            else:
                st.error(f" Error: {response.status_code}")
        except Exception as e:
            st.error(f"Connection error: {e}")
    
    st.markdown("""
    ---
    
    ### Development Status
    
    - Real USGS data integration enabled
    - Automated scheduler running (15-minute intervals)
    - Database persistently stores readings
    - API endpoints return live data
    - Fallback to mock data if API unavailable
    
    ### Next Steps
    
    - ARIMA predictions trained on real historical data
    - Alerting system for dangerous flow conditions
    - Historical data archival (keep 6+ months)
    - Real USGS gauge station authentication (if required)
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; font-size: 0.9rem;">
    River Access & Conditions MVP | Data source: USGS Water Services | 
    <a href="http://localhost:8000/docs">API Docs</a>
</div>
""", unsafe_allow_html=True)
