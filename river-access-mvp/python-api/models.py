from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Enum, ForeignKey, Text, Date, DECIMAL, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://river_user:river_pass@localhost:3306/river_access")

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class River(Base):
    __tablename__ = "rivers"
    
    river_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    state = Column(String(20))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    sections = relationship("RiverSection", back_populates="river", cascade="all, delete-orphan")
    gauges = relationship("USGSGauge", back_populates="river", cascade="all, delete-orphan")
    access_points = relationship("AccessPoint", back_populates="river", cascade="all, delete-orphan")


class RiverSection(Base):
    __tablename__ = "river_sections"
    
    section_id = Column(Integer, primary_key=True, index=True)
    river_id = Column(Integer, ForeignKey("rivers.river_id"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    difficulty_class = Column(String(10))
    length_miles = Column(DECIMAL(5, 2))
    min_flow_cfs = Column(Integer)
    max_flow_cfs = Column(Integer)
    optimal_min_cfs = Column(Integer)
    optimal_max_cfs = Column(Integer)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    river = relationship("River", back_populates="sections")
    gauges = relationship("USGSGauge", back_populates="section")
    access_points = relationship("AccessPoint", back_populates="section")


class USGSGauge(Base):
    __tablename__ = "usgs_gauges"
    
    gauge_id = Column(Integer, primary_key=True, index=True)
    river_id = Column(Integer, ForeignKey("rivers.river_id"), nullable=False, index=True)
    section_id = Column(Integer, ForeignKey("river_sections.section_id"))
    site_number = Column(String(20), unique=True, nullable=False, index=True)
    gauge_name = Column(String(100), nullable=False)
    latitude = Column(DECIMAL(10, 8))
    longitude = Column(DECIMAL(11, 8))
    drainage_area_sqmi = Column(DECIMAL(10, 2))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    river = relationship("River", back_populates="gauges")
    section = relationship("RiverSection", back_populates="gauges")
    conditions = relationship("CurrentCondition", back_populates="gauge", cascade="all, delete-orphan")
    predictions = relationship("ArimaPrediction", back_populates="gauge", cascade="all, delete-orphan")


class CurrentCondition(Base):
    __tablename__ = "current_conditions"
    
    condition_id = Column(Integer, primary_key=True, index=True)
    gauge_id = Column(Integer, ForeignKey("usgs_gauges.gauge_id"), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    flow_cfs = Column(DECIMAL(10, 2))
    gauge_height_ft = Column(DECIMAL(6, 2))
    temperature_f = Column(DECIMAL(5, 2))
    data_quality = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    gauge = relationship("USGSGauge", back_populates="conditions")


class ArimaPrediction(Base):
    __tablename__ = "arima_predictions"
    
    prediction_id = Column(Integer, primary_key=True, index=True)
    gauge_id = Column(Integer, ForeignKey("usgs_gauges.gauge_id"), nullable=False, index=True)
    prediction_date = Column(Date, nullable=False, index=True)
    predicted_flow_cfs = Column(DECIMAL(10, 2))
    confidence_lower = Column(DECIMAL(10, 2))
    confidence_upper = Column(DECIMAL(10, 2))
    model_version = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    gauge = relationship("USGSGauge", back_populates="predictions")


class AccessPoint(Base):
    __tablename__ = "access_points"
    
    access_id = Column(Integer, primary_key=True, index=True)
    river_id = Column(Integer, ForeignKey("rivers.river_id"), nullable=False, index=True)
    section_id = Column(Integer, ForeignKey("river_sections.section_id"))
    name = Column(String(100), nullable=False)
    type = Column(String(10), default="both")  # put_in, takeout, both
    latitude = Column(DECIMAL(10, 8))
    longitude = Column(DECIMAL(11, 8))
    parking_type = Column(String(20), default="small_lot")
    parking_capacity = Column(String(20), default="moderate")
    parking_fee = Column(DECIMAL(5, 2), default=0)
    facilities = Column(Text)
    access_difficulty = Column(String(20), default="moderate")
    notes = Column(Text)
    last_verified = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    river = relationship("River", back_populates="access_points")
    section = relationship("RiverSection", back_populates="access_points")


class WeatherCondition(Base):
    __tablename__ = "weather_conditions"
    
    weather_id = Column(Integer, primary_key=True, index=True)
    section_id = Column(Integer, ForeignKey("river_sections.section_id"), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    temperature_f = Column(DECIMAL(5, 2))
    feels_like_f = Column(DECIMAL(5, 2))
    humidity_percent = Column(Integer)
    wind_speed_mph = Column(DECIMAL(5, 2))
    wind_gust_mph = Column(DECIMAL(5, 2))
    wind_direction_deg = Column(Integer)
    wind_direction = Column(String(3))
    precipitation_in = Column(DECIMAL(6, 3))
    precipitation_chance = Column(Integer)
    visibility_miles = Column(DECIMAL(5, 2))
    uv_index = Column(Integer)
    cloud_cover_percent = Column(Integer)
    conditions = Column(String(100))
    weather_code = Column(Integer)
    data_source = Column(String(50), default="OpenWeatherMap")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    section = relationship("RiverSection")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
