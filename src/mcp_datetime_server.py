"""
ĆWICZENIE 3 (1 pkt) — serwer MCP z datą i czasem. Port 8002.

Dwa narzędzia:
  - get_current_date     -> "YYYY-MM-DD"
  - get_current_datetime -> "YYYY-MM-DDTHH:MM:SS" (ISO 8601, do sekund)

Uruchom w osobnym terminalu:  uv run python src/mcp_datetime_server.py
"""

import datetime

from fastmcp import FastMCP

mcp = FastMCP("Date and time")


@mcp.tool(description='Get the current date in the format "Year-Month-Day" (YYYY-MM-DD).')
def get_current_date() -> str:
    return datetime.date.today().isoformat()


@mcp.tool(
    description="Get the current date and time in ISO 8601 format up to seconds "
    "(YYYY-MM-DDTHH:MM:SS)."
)
def get_current_datetime() -> str:
    # bez mikrosekund -> do sekund
    return datetime.datetime.now().replace(microsecond=0).isoformat()


if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8002)
