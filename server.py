#!/usr/bin/env python3
"""Agriculture Robotics MCP Server — Farm automation governance and safety."""

import sys, os
sys.path.insert(0, os.path.expanduser('~/clawd/meok-labs-engine/shared'))
from auth_middleware import check_access

import json
from datetime import datetime, timezone
from collections import defaultdict
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("agriculture-robotics", instructions="MEOK AI Labs MCP Server")

FREE_DAILY_LIMIT = 15
_usage = defaultdict(list)
def _rl(c="anon"):
    now = datetime.now(timezone.utc)
    _usage[c] = [t for t in _usage[c] if (now-t).total_seconds() < 86400]
    if len(_usage[c]) >= FREE_DAILY_LIMIT: return json.dumps({"error": f"Limit {FREE_DAILY_LIMIT}/day"})
    _usage[c].append(now); return None

@mcp.tool()
def robot_safety_check(robot_type: str, max_speed_ms: float, has_emergency_stop: bool, api_key: str = "") -> str:
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(): return err

    risks = []
    if max_speed_ms > 2.0:
        risks.append("Speed exceeds safe threshold for human-robot collaboration")
    if not has_emergency_stop:
        risks.append("Missing emergency stop — non-compliant with ISO 18497")
    return {"robot_type": robot_type, "risks": risks, "compliant": len(risks) == 0}

@mcp.tool()
def spray_plan_calculator(field_ha: float, chemical_l_per_ha: float, buffer_m: float, api_key: str = "") -> str:
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(): return err

    total = field_ha * chemical_l_per_ha
    safe = buffer_m >= 5.0
    return {"total_litres": round(total, 2), "buffer_compliant": safe, "warnings": [] if safe else ["Increase buffer zone to 5m minimum"]}

@mcp.tool()
def harvest_optimization(crop_type: str, moisture_percent: float, weather_forecast: str, api_key: str = "") -> str:
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(): return err

    ready = moisture_percent < 20 and "rain" not in weather_forecast.lower()
    return {"crop": crop_type, "harvest_ready": ready, "moisture": moisture_percent, "recommendation": "Proceed" if ready else "Delay 24-48h"}

@mcp.tool()
def drone_flight_plan(field_bounds: list, max_altitude_m: float, has_geo_fence: bool, api_key: str = "") -> str:
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(): return err

    within_caa = max_altitude_m <= 120
    return {"altitude_ok": within_caa, "geo_fence_enabled": has_geo_fence, "flight_authorized": within_caa and has_geo_fence}

if __name__ == "__main__":
    mcp.run()
