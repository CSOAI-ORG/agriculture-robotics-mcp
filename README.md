<div align="center">

# Agriculture Robotics MCP

**MCP server for agriculture robotics mcp operations**

[![PyPI](https://img.shields.io/pypi/v/meok-agriculture-robotics-mcp)](https://pypi.org/project/meok-agriculture-robotics-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

Agriculture Robotics MCP provides AI-powered tools via the Model Context Protocol (MCP).

## Tools

| Tool | Description |
|------|-------------|
| `robot_safety_check` | Run safety diagnostics on agricultural robot systems per ISO 18497 (Collaborativ |
| `spray_plan_calculator` | Calculate spray coverage with EPA drift mitigation and buffer zone compliance. |
| `harvest_optimization` | Optimize harvest schedule with moisture, weather, and equipment readiness. |
| `drone_flight_plan` | Generate agricultural drone flight plan with CAA compliance for Part 107/Part 10 |
| `soil_analysis` | Analyze soil nutrients and generate fertilizer recommendations. |
| `irrigation_schedule` | Calculate irrigation schedule using FAO-56 evapotranspiration. |

## Installation

```bash
pip install meok-agriculture-robotics-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "agriculture-robotics-mcp": {
      "command": "python",
      "args": ["-m", "meok_agriculture_robotics_mcp.server"]
    }
  }
}
```

## Usage with FastMCP

```python
from mcp.server.fastmcp import FastMCP

# This server exposes 6 tool(s) via MCP
# See server.py for full implementation
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
