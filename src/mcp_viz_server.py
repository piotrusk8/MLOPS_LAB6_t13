"""
ĆWICZENIE 4 (1 pkt) — serwer MCP do wizualizacji. Port 8003.

Końcówka line_plot: rysuje wykres liniowy z podanych danych (Matplotlib)
i zwraca obraz PNG zakodowany w base64.

  Wymagane:    data       -> jedna lub więcej list liczb
  Opcjonalne:  title, x_label, y_label, legend (bool)

Uruchom w osobnym terminalu:  uv run python src/mcp_viz_server.py
Test klientem:                uv run python src/test_viz_client.py
"""

import base64
import io
from typing import Annotated

import matplotlib

matplotlib.use("Agg")  # backend bez okienka (serwer)
import matplotlib.pyplot as plt  # noqa: E402
from fastmcp import FastMCP  # noqa: E402

mcp = FastMCP("Visualization")


@mcp.tool(
    description="Create a line plot from one or more series of numbers and return it "
    "as a base64-encoded PNG image."
)
def line_plot(
    data: Annotated[
        list[list[float]],
        "One or more series, each a list of numbers, e.g. [[1,2,3],[3,2,1]].",
    ],
    title: Annotated[str, "Plot title."] = "",
    x_label: Annotated[str, "X axis label."] = "",
    y_label: Annotated[str, "Y axis label."] = "",
    legend: Annotated[bool, "Whether to show the legend."] = False,
) -> str:
    # pozwól też na pojedynczą listę liczb -> opakuj w listę serii
    if data and not isinstance(data[0], (list, tuple)):
        data = [data]  # type: ignore[list-item]

    fig, ax = plt.subplots(figsize=(8, 5))
    for i, series in enumerate(data):
        ax.plot(range(len(series)), series, marker="o", label=f"series {i + 1}")

    if title:
        ax.set_title(title)
    if x_label:
        ax.set_xlabel(x_label)
    if y_label:
        ax.set_ylabel(y_label)
    if legend:
        ax.legend()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=100, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("ascii")


if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8003)
