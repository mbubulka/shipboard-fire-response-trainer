"""
Hypothermia Risk Assessment based on USCG and NOAA data.

Scientific backing:
- USCG Cold Water Immersion data: Time to incapacitation by water temperature
- NOAA Hypothermia Risk Guidelines
- Wetsuit effectiveness by thickness
"""

from dataclasses import dataclass
from typing import Tuple, Optional


@dataclass
class IncapacitationTime:
    """USCG data: Time to incapacitation (loss of muscular function) in minutes"""
    water_temp_f: int
    min_time: int
    max_time: int
    description: str


# USCG Cold Water Immersion incapacitation times
USCG_INCAPACITATION_TIMES = [
    IncapacitationTime(32, 15, 30, "32-40°F: 15-30 min"),
    IncapacitationTime(40, 30, 40, "40-50°F: 30-40 min"),
    IncapacitationTime(50, 60, 120, "50-60°F: 60-120 min (1-2 hrs)"),
    IncapacitationTime(60, 120, 240, "60-70°F: 2-4 hours"),
    IncapacitationTime(70, 240, 1440, "70°F+: 4+ hours"),
]

# Wetsuit insulation effectiveness (adds to core temp retention, in °F equivalent)
WETSUIT_PROTECTION = {
    "none": 0,
    "rash_guard": 3,
    "3mm": 5,
    "5mm": 8,
    "7mm": 10,
    "dry_suit": 15,
}

# Wind chill effect modifier (severe wind can accelerate hypothermia)
WIND_EXPOSURE_FACTOR = {
    "calm": 1.0,  # < 10 mph
    "moderate": 1.2,  # 10-25 mph
    "strong": 1.5,  # 25+ mph
}


def get_incapacitation_time(water_temp_f: float) -> Tuple[int, int]:
    """Get USCG incapacitation time range for given water temperature in minutes."""
    for spec in USCG_INCAPACITATION_TIMES:
        if water_temp_f <= spec.water_temp_f + 5:
            return (spec.min_time, spec.max_time)
    # Beyond 70°F
    return (240, 1440)


def calculate_combined_risk_score(
    water_temp_f: float,
    air_temp_f: float,
    wind_speed_mph: float = 0,
    exposure_minutes: int = 120,
) -> dict:
    """
    Calculate combined hypothermia risk score (0-100).
    
    Factors:
    1. Water temperature (primary driver of hypothermia speed)
    2. Air temperature (affects pre-immersion heat loss)
    3. Wind speed (accelerates heat loss via wind chill)
    4. Time in water (exposure duration)
    
    Returns:
        dict with:
        - risk_score (0-100): Overall risk
        - risk_level: "CRITICAL", "HIGH", "MODERATE", "LOW_MODERATE", "LOW"
        - incapacitation_min/max: Minutes to incapacitation
        - protective_gear: Recommended gear list
        - rationale: Explanation of scoring
    """
    
    # Get USCG incapacitation times
    incap_min, incap_max = get_incapacitation_time(water_temp_f)
    
    # Base risk from water temperature (primary factor - 60% weight)
    water_risk = 0
    if water_temp_f < 32:
        water_risk = 100
    elif water_temp_f < 40:
        water_risk = 90  # < 40°F: Critical
    elif water_temp_f < 50:
        water_risk = 75  # 40-50°F: High
    elif water_temp_f < 60:
        water_risk = 50  # 50-60°F: Moderate
    elif water_temp_f < 70:
        water_risk = 25  # 60-70°F: Low-Moderate
    else:
        water_risk = 10  # 70°F+: Low
    
    # Air temperature modifier (20% weight)
    air_risk = 0
    if air_temp_f < 32:
        air_risk = 100  # Freezing air
    elif air_temp_f < 40:
        air_risk = 50  # Cold air
    elif air_temp_f < 50:
        air_risk = 25  # Cool air
    elif air_temp_f < 60:
        air_risk = 10  # Mild air
    else:
        air_risk = 0  # Warm
    
    # Wind exposure modifier (15% weight)
    wind_factor = 1.0
    if wind_speed_mph > 25:
        wind_factor = WIND_EXPOSURE_FACTOR["strong"]
        wind_risk = 40
    elif wind_speed_mph > 10:
        wind_factor = WIND_EXPOSURE_FACTOR["moderate"]
        wind_risk = 20
    else:
        wind_factor = WIND_EXPOSURE_FACTOR["calm"]
        wind_risk = 0
    
    # Exposure time modifier (5% weight)
    time_risk = 0
    if exposure_minutes > incap_max:
        time_risk = 100  # Exceeds max safe time
    elif exposure_minutes > incap_min:
        time_risk = (exposure_minutes - incap_min) / (incap_max - incap_min) * 50
    
    # Combined weighted score
    combined_score = (
        (water_risk * 0.60) +
        (air_risk * 0.20) +
        (wind_risk * 0.15) +
        (time_risk * 0.05)
    )
    
    # Apply wind chill multiplier to adjust severity
    combined_score = min(100, combined_score * wind_factor)
    
    # Determine risk level and gear recommendation
    if combined_score >= 80:
        risk_level = "CRITICAL"
        emoji = "🔴"
        gear = [
            "Dry suit with waterproof seals",
            "Immersion-rated PFD (Type III or V with immersion collar)",
            "Neoprene gloves & booties",
            "Neck gaiter or hood",
            "Consider limiting to very short duration only"
        ]
        rationale = f"Water {water_temp_f:.0f}°F + Air {air_temp_f:.0f}°F creates severe hypothermia risk. Incapacitation in {incap_min}-{incap_max} minutes."
    elif combined_score >= 60:
        risk_level = "HIGH"
        emoji = "🟠"
        gear = [
            "5mm+ wet suit or semi-dry suit",
            "Immersion-rated PFD",
            "Neoprene gloves",
            "Wool hat or hood",
            "Consider limiting duration"
        ]
        rationale = f"Water {water_temp_f:.0f}°F requires substantial insulation. Incapacitation in {incap_min}-{incap_max} minutes."
    elif combined_score >= 40:
        risk_level = "MODERATE"
        emoji = "🟡"
        gear = [
            "3mm wet suit or thick rash guard",
            "Standard PFD",
            "Gloves recommended",
            "Quick-dry clothing layer"
        ]
        rationale = f"Water {water_temp_f:.0f}°F + Air {air_temp_f:.0f}°F = moderate risk. Gradual hypothermia possible after {incap_max} minutes."
    elif combined_score >= 20:
        risk_level = "LOW_MODERATE"
        emoji = "🟢"
        gear = [
            "Rash guard or quick-dry shirt",
            "Standard PFD",
            "Optional gloves",
            "Quick-dry shorts/pants"
        ]
        rationale = f"Water {water_temp_f:.0f}°F is manageable with light protection. Low incapacitation risk if conditions stable."
    else:
        risk_level = "LOW"
        emoji = "🟢"
        gear = [
            "Standard PFD",
            "Quick-dry clothes",
            "Normal paddling attire"
        ]
        rationale = f"Water {water_temp_f:.0f}°F + Air {air_temp_f:.0f}°F = favorable conditions for paddling."
    
    return {
        "risk_score": round(combined_score, 1),
        "risk_level": risk_level,
        "emoji": emoji,
        "incapacitation_min": incap_min,
        "incapacitation_max": incap_max,
        "protective_gear": gear,
        "rationale": rationale,
        "water_risk_component": round(water_risk, 1),
        "air_risk_component": round(air_risk, 1),
        "wind_risk_component": round(wind_risk, 1),
        "wind_chill_factor": round(wind_factor, 2),
    }


def format_recommendation(risk_data: dict) -> str:
    """Format risk data into readable recommendation string."""
    gear_list = "\n".join([f"  • {item}" for item in risk_data["protective_gear"]])
    
    return f"""
{risk_data['emoji']} **{risk_data['risk_level']} HYPOTHERMIA RISK**

**Incapacitation Time:** {risk_data['incapacitation_min']}-{risk_data['incapacitation_max']} minutes (USCG data)
**Combined Risk Score:** {risk_data['risk_score']}/100

**Rationale:** {risk_data['rationale']}

**Recommended Gear:**
{gear_list}

**Risk Breakdown:**
  • Water Temp Factor: {risk_data['water_risk_component']}/100
  • Air Temp Factor: {risk_data['air_risk_component']}/100
  • Wind Chill Factor: {risk_data['wind_risk_component']}/100 (×{risk_data['wind_chill_factor']} multiplier)
""".strip()
