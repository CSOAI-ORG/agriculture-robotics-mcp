#!/usr/bin/env python3
"""Agriculture Robotics MCP — MEOK AI Labs. Farm automation governance, crop safety, and autonomous tractor compliance."""

import sys, os

sys.path.insert(0, os.path.expanduser("~/clawd/meok-labs-engine/shared"))
from auth_middleware import check_access

import json
from datetime import datetime, timezone
from collections import defaultdict
from typing import Optional
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "agriculture-robotics",
    instructions="MEOK AI Labs — Agricultural Robotics Governance. ISO 18497 robot safety, EPA pesticide drift, FAA farm drone compliance.",
)

FREE_DAILY_LIMIT = 15
_usage = defaultdict(list)


def _rl(c="anon"):
    now = datetime.now(timezone.utc)
    _usage[c] = [t for t in _usage[c] if (now - t).total_seconds() < 86400]
    if len(_usage[c]) >= FREE_DAILY_LIMIT:
        return json.dumps({"error": f"Limit {FREE_DAILY_LIMIT}/day"})
    _usage[c].append(now)
    return None


ISO_18497_SAFE_SPEED = 2.0
EPA_DRIFT_BUFFER = 5.0


@mcp.tool()
def robot_safety_check(
    robot_type: str, max_speed_ms: float, has_emergency_stop: bool, api_key: str = ""
) -> str:
    """Run safety diagnostics on agricultural robot systems per ISO 18497 (Collaborative robots).

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need structured analysis or classification
        of inputs against established frameworks or standards.

    When NOT to use:
        Not suitable for real-time production decision-making without
        human review of results.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl():
        return err

    risks = []
    if max_speed_ms > ISO_18497_SAFE_SPEED:
        risks.append(
            f"Speed {max_speed_ms}m/s exceeds {ISO_18497_SAFE_SPEED}m/s threshold for human-robot collaboration"
        )
    if not has_emergency_stop:
        risks.append("Missing emergency stop — non-compliant with ISO 18497-1:2022")
    if robot_type.lower() in ["tractor", "harvester", "sprayer"]:
        risks.append(
            f"{robot_type} requires operator presence or remote monitoring per OSHA 1910.178"
        )

    return {
        "robot_type": robot_type,
        "risks": risks,
        "compliant": len(risks) == 0,
        "standard": "ISO 18497-1:2022",
        "reference": "https://www.iso.org/standard/66551.html",
    }


@mcp.tool()
def spray_plan_calculator(
    field_ha: float,
    chemical_l_per_ha: float,
    buffer_m: float,
    wind_speed_ms: float = 0.0,
    api_key: str = "",
) -> str:
    """Calculate spray coverage with EPA drift mitigation and buffer zone compliance.

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need structured analysis or classification
        of inputs against established frameworks or standards.

    When NOT to use:
        Not suitable for real-time production decision-making without
        human review of results.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl():
        return err

    total = field_ha * chemical_l_per_ha
    wind_safe = wind_speed_ms < 4.5
    buffer_compliant = buffer_m >= EPA_DRIFT_BUFFER
    drift_risk = (
        "low" if wind_speed_ms < 3 else "moderate" if wind_speed_ms < 6 else "high"
    )

    warnings = []
    if not wind_safe:
        warnings.append(f"Wind {wind_speed_ms}m/s exceeds 4.5m/s — suspend spraying")
    if not buffer_compliant:
        warnings.append(f"Buffer {buffer_m}m below {EPA_DRIFT_BUFFER}m EPA minimum")
    if drift_risk == "high":
        warnings.append("High drift risk — use drift-reducing nozzles")

    return {
        "total_litres": round(total, 2),
        "buffer_compliant": buffer_compliant,
        "wind_compliant": wind_safe,
        "drift_risk": drift_risk,
        "warnings": warnings,
        "epa_reference": "40 CFR Part 180",
    }


@mcp.tool()
def harvest_optimization(
    crop_type: str,
    moisture_percent: float,
    weather_forecast: str,
    equipment_available: bool = True,
    api_key: str = "",
) -> str:
    """Optimize harvest schedule with moisture, weather, and equipment readiness.

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need structured analysis or classification
        of inputs against established frameworks or standards.

    When NOT to use:
        Not suitable for real-time production decision-making without
        human review of results.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl():
        return err

    ready = moisture_percent < 20 and "rain" not in weather_forecast.lower()
    risk = (
        "low"
        if moisture_percent < 15
        else "moderate"
        if moisture_percent < 25
        else "high"
    )

    recommendations = []
    if not ready:
        recommendations.append("Delay 24-48h for field conditions")
    if "rain" in weather_forecast.lower():
        recommendations.append("Wet conditions — risk of soil compaction")
    if "frost" in weather_forecast.lower() and crop_type.lower() in ["corn", "soybean"]:
        recommendations.append("Frost risk — monitor for lodging")
    if not equipment_available:
        recommendations.append("Schedule equipment maintenance")

    return {
        "crop": crop_type,
        "harvest_ready": ready,
        "moisture": moisture_percent,
        "risk_level": risk,
        "equipment_available": equipment_available,
        "recommendations": recommendations,
    }


@mcp.tool()
def drone_flight_plan(
    field_bounds: list,
    max_altitude_m: float,
    has_geo_fence: bool,
    operation_type: str = "spraying",
    api_key: str = "",
) -> str:
    """Generate agricultural drone flight plan with CAA compliance for Part 107/Part 107+.

    Behavior:
        This tool generates structured output without modifying external systems.
        Output is deterministic for identical inputs. No side effects.
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need structured analysis or classification
        of inputs against established frameworks or standards.

    When NOT to use:
        Not suitable for real-time production decision-making without
        human review of results.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl():
        return err

    within_caa = max_altitude_m <= 120
    part107 = not operation_type.lower() == "bvos"
    warnings = []
    if max_altitude_m > 120:
        warnings.append("Altitude exceeds 120m — requires waiver")
    if not has_geo_fence:
        warnings.append("Geofence recommended for operation over people")
    if operation_type.lower() == "bvos":
        warnings.append("BVLOS requires Part 107+ waiver from FAA")

    return {
        "altitude_ok": within_caa,
        "geo_fence_enabled": has_geo_fence,
        "part107_compliant": part107,
        "operation_type": operation_type,
        "warnings": warnings,
        "faa_reference": "14 CFR Part 107",
    }


@mcp.tool()
def soil_analysis(
    field_id: str,
    ph: float,
    nitrogen_ppm: float,
    phosphorus_ppm: float,
    potassium_ppm: float,
    api_key: str = "",
) -> str:
    """Analyze soil nutrients and generate fertilizer recommendations.

    Behavior:
        This tool generates structured output without modifying external systems.
        Output is deterministic for identical inputs. No side effects.
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need structured analysis or classification
        of inputs against established frameworks or standards.

    When NOT to use:
        Not suitable for real-time production decision-making without
        human review of results.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl():
        return err

    deficiency = []
    if ph < 6.0:
        deficiency.append("Low pH — apply lime")
    if ph > 7.5:
        deficiency.append("High pH — apply sulfur")
    if nitrogen_ppm < 40:
        deficiency.append("Nitrogen low — apply N fertilizer")
    if phosphorus_ppm < 30:
        deficiency.append("Phosphorus low — apply P fertilizer")
    if potassium_ppm < 150:
        deficiency.append("Potassium low — apply K fertilizer")

    return {
        "field_id": field_id,
        "ph": ph,
        "nutrients": {"n": nitrogen_ppm, "p": phosphorus_ppm, "k": potassium_ppm},
        "deficiencies": deficiency,
        "recommendation": "Apply fertilizer per soil test"
        if deficiency
        else "Nutrients adequate",
    }


@mcp.tool()
def irrigation_schedule(
    crop: str,
    eto_mm: float,
    soil_capacity_mm: float,
    days_since_water: int,
    api_key: str = "",
) -> str:
    """Calculate irrigation schedule using FAO-56 evapotranspiration.

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need structured analysis or classification
        of inputs against established frameworks or standards.

    When NOT to use:
        Not suitable for real-time production decision-making without
        human review of results.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl():
        return err

    crop_coefficients = {
        "corn": 1.15,
        "wheat": 1.05,
        "soybean": 1.0,
        "cotton": 1.1,
        "rice": 1.2,
    }
    kc = crop_coefficients.get(crop.lower(), 1.0)
    etc = eto_mm * kc
    depletion = days_since_water * etc

    water_now = depletion > (soil_capacity_mm * 0.5)
    return {
        "crop": crop,
        "eto_mm": eto_mm,
        "etc_mm": round(etc, 2),
        "depletion_mm": round(depletion, 2),
        "water_now": water_now,
        "recommendation": "Irrigate today"
        if water_now
        else f"Wait {max(1, int((soil_capacity_mm * 0.5 - depletion) / etc))} days",
    }


if __name__ == "__main__":
    mcp.run()
