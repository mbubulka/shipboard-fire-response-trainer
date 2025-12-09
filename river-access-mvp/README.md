# River Access & Conditions MVP

A full-stack data analytics application showcasing real-time river monitoring, ARIMA forecasting, and advanced SQL patterns. Built for the DMV region with professional-grade SQL implementations.

**Portfolio project demonstrating:** Full-stack development • Docker containerization • Time series forecasting • Database design • SQL optimization • API development

---

## Features

### Dashboard
- **Real-time Conditions**: Live flow data, gauge height, temperature from USGS
- **7-Day Forecast**: ARIMA(1,1,1) predictions with confidence intervals
- **Interactive Mapping**: River sections and access points with Folium
- **Access Points**: Curated put-in/take-out locations with details

### Advanced SQL Queries (Portfolio Showcase)
- **CTE + Aggregation**: Flow comparison across river sections
- **UNION Patterns**: Multi-section analysis
- **Window Functions**: Gauge performance rankings
- **Self-Joins**: Access points availability analysis
- **Multi-Table Joins**: Weather-flow correlation
- **Subqueries**: Predictive accuracy analysis
- **Schema Overview**: Database structure exploration

**Each query includes:**
- Execution metrics (time, rows returned)
- Detailed SQL explanation (expandable)
- Real results from MySQL database
- Pattern documentation

### API & Backend
- FastAPI with OpenAPI docs
- RESTful endpoints for all data
- Background schedulers (USGS 15min, Weather 30min)
- MySQL persistence with SQLAlchemy ORM

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit (Python web framework) |
| **Backend** | FastAPI + Uvicorn |
| **Database** | MySQL 8.0 |
| **Forecasting** | Statsmodels ARIMA |
| **Containerization** | Docker Compose |
| **Version Control** | Git |

---

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Git

### Local Development

```bash
# Clone repository
git clone <your-github-repo>
cd river-access-mvp

# Start all services
docker-compose up --build
```

**Access the app:**
- **Dashboard:** http://localhost:8506
- **API Docs:** http://localhost:8005/docs
- **API Base:** http://localhost:8005

### Environment Setup

Copy `.env.example` to `.env` (default values are suitable for local development):

```bash
cp .env.example .env
```

Configuration variables:
- `MYSQL_ROOT_PASSWORD`: Database admin password
- `MYSQL_DATABASE`: Database name
- `DATABASE_URL`: SQLAlchemy connection string
- `API_URL`: Backend API endpoint

---

## Project Structure

```
river-access-mvp/
├── streamlit-app/          # Frontend dashboard
│   ├── app.py              # Main Streamlit application
│   └── requirements.txt     # Python dependencies
│
├── python-api/             # Backend services
│   ├── app.py              # FastAPI application
│   ├── models.py           # SQLAlchemy ORM models
│   ├── routes.py           # API endpoints
│   ├── data_generator.py   # ARIMA forecasting logic
│   ├── scheduler.py        # USGS data collection
│   ├── weather_scheduler.py # Weather data collection
│   └── requirements.txt     # Python dependencies
│
├── mysql-init/             # Database initialization
│   └── schema.sql          # Database schema & migrations
│
├── docker-compose.yml      # Multi-container orchestration
├── .env.example            # Environment variable template
├── .gitignore              # Git ignore rules
├── README.md               # This file
├── QUICKSTART.md           # Quick start guide
└── SQL_DOCUMENTATION.md    # SQL patterns documentation
```

---

## Architecture

```
┌─────────────────────────────────────────┐
│    Streamlit Dashboard (Port 8506)      │
│  - Real-time conditions                 │
│  - ARIMA predictions                    │
│  - SQL query explorer                   │
│  - Interactive mapping                  │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│     FastAPI Backend (Port 8005)         │
│  - RESTful API endpoints                │
│  - ARIMA model integration              │
│  - Data processing                      │
│  - SQLAlchemy ORM                       │
└──────────────────┬──────────────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
┌──────────────────┐  ┌─────────────────────┐
│  MySQL Database  │  │  Background Tasks   │
│  (Port 3306)     │  │  - USGS Scheduler   │
│                  │  │  - Weather Scheduler│
└──────────────────┘  └─────────────────────┘
```

---

## Data Flow

### Real-time Updates
1. **USGS Scheduler** (15-min intervals)
   - Fetches latest flow data
   - Stores in `current_conditions` table
   
2. **Weather Scheduler** (30-min intervals)
   - Fetches temperature & conditions
   - Updates `weather_data` table

3. **Streamlit Dashboard**
   - Queries latest conditions via API
   - Displays with real-time updates

### Forecasting
1. **Data Generator** reads historical flows
2. **ARIMA(1,1,1) Model** fits on last 30 days
3. **7-day prediction** with 95% confidence intervals
4. Results cached and served via API

### SQL Queries
- Pattern showcase using real river data
- CTEs, window functions, joins, subqueries
- Execution metrics & explanations
- Educational for SQL portfolio

---

## API Endpoints

### Conditions
```
GET /api/conditions/{gauge_id}       # Current flow/gauge data
GET /api/current-weather             # Temperature & conditions
```

### Predictions
```
GET /api/predictions/{gauge_id}      # 7-day ARIMA forecast
```

### Queries
```
GET /queries/flow-comparison-by-section
GET /queries/gauge-performance-ranking
GET /queries/weather-flow-correlation
# ... (7 total SQL query patterns)
```

Full documentation: http://localhost:8005/docs

---

## Development

### Adding Features

1. **Backend**: Edit `python-api/app.py` or `python-api/routes.py`
2. **Frontend**: Edit `streamlit-app/app.py`
3. **Database**: Update schema in `mysql-init/schema.sql`
4. **Restart**: `docker-compose restart <service>`

### Debugging

View logs:
```bash
docker-compose logs -f streamlit
docker-compose logs -f python-api
docker-compose logs -f mysql
```

### Testing SQL Queries

SSH into MySQL container:
```bash
docker exec -it river_mysql mysql -u river_user -p
```

---

## Deployment

For production deployment to Railway, Render, or other cloud platforms:

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions including:
- Configuring environment variables
- Cloud database setup (PlanetScale)
- Domain configuration
- CI/CD integration

---

## Data Sources

- **USGS Water Services**: Real-time gauging station data (Public API)
- **Open-Meteo**: Weather data (Free API)
- **Manual Data**: Access points curated for DMV region

All APIs used are free and public - no credentials required for basic operations.

---

## Performance Metrics

- **Forecast Accuracy**: ARIMA evaluated on out-of-sample test set
- **Query Performance**: Indexed tables for O(1) lookups
- **API Response Time**: <200ms average
- **Dashboard Load Time**: <3s with cold cache

---

## Future Enhancements

- [ ] Real USGS API authentication for production data
- [ ] Additional river sections (Potomac, Shenandoah tributaries)
- [ ] User accounts & saved predictions
- [ ] Mobile-responsive design
- [ ] Alert system (high/low flow notifications)
- [ ] Historical trend analysis

---

## Troubleshooting

### Containers won't start
```bash
docker-compose down
docker system prune -f
docker-compose up --build
```

### Database connection errors
- Ensure MySQL container is fully initialized (wait 10-15 seconds)
- Check `docker logs river_mysql` for initialization errors

### Streamlit app crashes
- Check `docker logs river_streamlit` for Python errors
- Verify FastAPI backend is running (`docker logs river_python_api`)

---

## License

Portfolio project - Use freely for learning and demonstration

---

## Contact & Portfolio

This project demonstrates:
- ✅ Full-stack web development (Python, SQL, Docker)
- ✅ Time series forecasting & machine learning
- ✅ RESTful API design
- ✅ Database schema design & optimization
- ✅ DevOps & containerization
- ✅ Data visualization & dashboarding

Perfect for interview discussions about production-ready applications.
