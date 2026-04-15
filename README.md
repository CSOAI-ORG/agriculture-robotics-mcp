# Agriculture Robotics MCP Server

> By [MEOK AI Labs](https://meok.ai) — Agricultural robotics governance, crop safety, and autonomous farm compliance

## Installation

```bash
pip install agriculture-robotics-mcp
```

## Usage

```bash
# Run standalone
python server.py

# Or via MCP
mcp install agriculture-robotics-mcp
```

## Tools

### `robot_safety_check`
Run safety diagnostics on agricultural robot systems per ISO 18497 collaborative robots standard.

**Parameters:**
- `robot_type` (str): Robot type (e.g., tractor, harvester, sprayer)
- `max_speed_ms` (float): Maximum speed in m/s
- `has_emergency_stop` (bool): Whether emergency stop is present

### `spray_plan_calculator`
Calculate spray coverage with EPA drift mitigation and buffer zone compliance.

**Parameters:**
- `field_ha` (float): Field size in hectares
- `chemical_l_per_ha` (float): Chemical application rate
- `buffer_m` (float): Buffer zone in meters
- `wind_speed_ms` (float): Wind speed in m/s

### `harvest_optimization`
Optimize harvest schedule with moisture, weather, and equipment readiness.

**Parameters:**
- `crop_type` (str): Crop type
- `moisture_percent` (float): Current moisture percentage
- `weather_forecast` (str): Weather forecast description
- `equipment_available` (bool): Whether equipment is available

### `drone_flight_plan`
Generate agricultural drone flight plan with CAA/FAA Part 107 compliance.

**Parameters:**
- `field_bounds` (list): Field boundary coordinates
- `max_altitude_m` (float): Maximum altitude in meters
- `has_geo_fence` (bool): Whether geofence is enabled
- `operation_type` (str): Operation type (default 'spraying')

### `soil_analysis`
Analyze soil nutrients (N/P/K, pH) and generate fertilizer recommendations.

**Parameters:**
- `field_id` (str): Field identifier
- `ph` (float): Soil pH
- `nitrogen_ppm` (float): Nitrogen in ppm
- `phosphorus_ppm` (float): Phosphorus in ppm
- `potassium_ppm` (float): Potassium in ppm

### `irrigation_schedule`
Calculate irrigation schedule using FAO-56 evapotranspiration.

**Parameters:**
- `crop` (str): Crop type
- `eto_mm` (float): Reference evapotranspiration in mm
- `soil_capacity_mm` (float): Soil water capacity in mm
- `days_since_water` (int): Days since last watering

## Authentication

Free tier: 15 calls/day. Upgrade at [meok.ai/pricing](https://meok.ai/pricing) for unlimited access.

## License

MIT — MEOK AI Labs
