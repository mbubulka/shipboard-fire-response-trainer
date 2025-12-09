# River Access MVP - Quick Start Guide

## Prerequisites

- Docker & Docker Compose installed
- Windows PowerShell or bash terminal

## 🚀 First Time Setup

```bash
# Navigate to project directory
cd "d:\Project SQL\river-access-mvp"

# Copy environment file
copy .env.example .env

# Build and start all services
docker-compose up --build
```

**First startup takes 2-3 minutes** (downloading images, building containers, initializing database)

## 🌐 Access the Application

Once you see messages like:
```
python-api  | INFO:     Uvicorn running on http://0.0.0.0:8000
streamlit   | You can now view your Streamlit app in your browser.
```

Open these URLs:

1. **Dashboard:** http://localhost:8501
2. **API Docs:** http://localhost:8000/docs
3. **API Base:** http://localhost:8000

## ⏹️ Stop the Services

Press `Ctrl+C` in the terminal, or run:

```bash
docker-compose down
```

## 🔄 Restart (After First Run)

```bash
docker-compose up
```

(No `--build` needed unless you change code)

## 📝 File Structure

```
river-access-mvp/
├── docker-compose.yml          # Service orchestration
├── .env                         # Environment variables
│
├── mysql-init/
│   └── schema.sql              # Database initialization
│
├── python-api/                 # FastAPI backend
│   ├── app.py                  # Main application
│   ├── models.py               # Database models
│   ├── routes.py               # API endpoints
│   ├── data_generator.py       # Mock data generation
│   └── requirements.txt
│
└── streamlit-app/              # Frontend dashboard
    ├── app.py                  # Main dashboard
    ├── utils.py                # Helper functions
    └── requirements.txt
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Service health check |
| `/api/rivers` | GET | List all rivers |
| `/api/gauges/{id}` | GET | Get gauge info |
| `/api/conditions/{id}` | GET | Get current conditions |
| `/api/predictions/{id}` | GET | Get 7-day predictions |
| `/api/access-points/{id}` | GET | Get access points |
| `/api/conditions/{id}/refresh` | POST | Refresh mock data |

## 🎯 Current Features (MVP)

- ✅ Current flow conditions (Little Falls)
- ✅ ARIMA 7-day flow predictions
- ✅ Access point information
- ✅ Flow condition classification (Good/High/Low)
- ✅ Interactive Streamlit dashboard
- ✅ REST API with auto-documentation
- ✅ Mock data generation

## 📚 Next Steps

1. **Real USGS Integration** - Replace mock data with live USGS API
2. **More Rivers** - Add Shenandoah, James River sections
3. **Map Visualization** - Add Folium/Mapbox integration
4. **Translation** - Add Spanish translations
5. **Alerts** - Email/SMS notifications for dangerous flow
6. **Historical Analysis** - Trend analysis and statistics

## 🐛 Troubleshooting

### Port Already in Use
```bash
# If port 3306 (MySQL), 8000 (API), or 8501 (Streamlit) is in use:
docker-compose down
# Then restart
```

### Database Connection Error
```bash
# MySQL needs a few seconds to start. If you get connection errors:
# 1. Stop services (Ctrl+C)
# 2. Wait 5 seconds
# 3. Restart: docker-compose up
```

### Can't Access Dashboard
- Check that Streamlit is running: `docker ps` should show 3 containers
- Clear Streamlit cache: Delete `~/.streamlit/` folder
- Try `http://127.0.0.1:8501` instead of `localhost`

## 📊 Database Info

- **Host:** localhost:3306 (inside Docker: mysql:3306)
- **Database:** river_access
- **Username:** river_user
- **Password:** river_pass
- **Root:** river_root_pass

Connect with any MySQL client:
```bash
mysql -h localhost -u river_user -p river_access
```

## 📝 Development Notes

Each service can run independently:

```bash
# Terminal 1: MySQL (already running in compose)

# Terminal 2: API development
cd python-api
pip install -r requirements.txt
uvicorn app:app --reload --port 8000

# Terminal 3: Streamlit development
cd streamlit-app
pip install -r requirements.txt
streamlit run app.py --logger.level=debug
```

## 🎓 Portfolio Value

This project demonstrates:
- Docker & containerization
- FastAPI REST APIs
- SQLAlchemy ORM & database design
- Streamlit dashboard development
- Data integration & processing
- Mock data generation
- Error handling & logging
- Multi-container orchestration

Perfect for showing employers your full-stack capabilities!

---

**Happy paddling! 🏄**
