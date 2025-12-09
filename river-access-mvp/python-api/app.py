from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time
import sys

# Try to connect to database
from models import engine, Base, SessionLocal

# Create tables
try:
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created/verified")
except Exception as e:
    print(f"! Database connection issue (normal on startup): {e}")
    print("  Retrying connection...")
    time.sleep(2)

# Import routes
from routes import router
from advanced_queries import router as advanced_queries_router

# Initialize FastAPI app
app = FastAPI(
    title="River Access API",
    description="Real-time river conditions and access information for DMV region",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)
app.include_router(advanced_queries_router)

@app.get("/")
async def root():
    return {
        "service": "River Access API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
