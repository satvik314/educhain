"""
Rendering helpers for visual (chart-based) questions.

Matplotlib / pandas are imported lazily so they're only required when a user
actually renders a visual question (``pip install educhain[visual]``).
"""

from __future__ import annotations

import base64
import io
from typing import Any, Dict, List, Optional


def render_graph(instruction: Dict[str, Any]) -> Optional[str]:
    """Render a ``graph_instruction`` dict to a base64-encoded PNG.

    Returns the base64 string, or ``None`` if rendering failed.
    """
    try:
        import matplotlib

        matplotlib.use("Agg")  # headless / notebook-safe
        import matplotlib.pyplot as plt
    except ImportError:
        raise ImportError(
            "matplotlib is required to render visual questions. "
            "Install with:  pip install educhain[visual]"
        )

    gtype = instruction.get("type")
    buffer = io.BytesIO()
    try:
        if gtype == "table":
            import pandas as pd

            try:
                import dataframe_image as dfi

                df = pd.DataFrame(instruction["data"])
                dfi.export(df, buffer, table_conversion="matplotlib")
            except ImportError:
                # Fall back to a matplotlib table if dataframe_image is absent.
                df = pd.DataFrame(instruction["data"])
                fig, ax = plt.subplots(figsize=(10, 0.6 * (len(df) + 1)))
                ax.axis("off")
                tbl = ax.table(
                    cellText=df.values, colLabels=df.columns, loc="center"
                )
                tbl.auto_set_font_size(False)
                tbl.set_fontsize(10)
                if instruction.get("title"):
                    ax.set_title(instruction["title"])
                fig.tight_layout()
                fig.savefig(buffer, format="png", bbox_inches="tight")
                plt.close(fig)
        else:
            plt.figure(figsize=(10, 8))
            _render_chart(plt, gtype, instruction)
            plt.tight_layout()
            plt.savefig(buffer, format="png")
            plt.close()
    except Exception as exc:  # noqa: BLE001
        print(f"Error generating visualization: {exc}")
        return None

    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("utf-8")


def _render_chart(plt, gtype: str, ins: Dict[str, Any]) -> None:
    if gtype == "bar":
        plt.bar(ins["x_labels"], ins["y_values"], color="skyblue")
        plt.ylabel(ins.get("y_label", ""))
        plt.title(ins.get("title", ""))
        plt.grid(axis="y", linestyle="--", alpha=0.7)
    elif gtype == "line":
        y_values: List[Any] = ins["y_values"]
        if y_values and isinstance(y_values[0], list):
            labels = ins.get("labels", [f"Series {i+1}" for i in range(len(y_values))])
            for i, ys in enumerate(y_values):
                plt.plot(ins["x_labels"], ys, marker="o", label=labels[i])
            plt.legend()
        else:
            plt.plot(ins["x_labels"], y_values, marker="o", color="b")
        plt.ylabel(ins.get("y_label", ""))
        plt.title(ins.get("title", ""))
        plt.grid(axis="y", linestyle="--", alpha=0.7)
    elif gtype == "pie":
        plt.pie(
            ins["sizes"],
            labels=ins["labels"],
            autopct="%1.1f%%",
            startangle=90,
        )
        plt.title(ins.get("title", ""))
    elif gtype == "scatter":
        plt.scatter(ins["x_values"], ins["y_values"], color="r", alpha=0.7)
        plt.ylabel(ins.get("y_label", ""))
        plt.title(ins.get("title", ""))
        plt.grid(axis="both", linestyle="--", alpha=0.7)
    else:
        raise ValueError(f"Unsupported graph type: {gtype}")


def display_visual_question(question, instruction: Dict[str, Any]) -> Optional[str]:
    """Render a chart and (in IPython) display it inline with the question."""
    img_b64 = render_graph(instruction)
    if img_b64:
        try:
            from IPython.display import HTML, display

            display(HTML(f'<img src="data:image/png;base64,{img_b64}" style="max-width:500px;">'))
        except Exception:
            pass  # not in a notebook; the base64 is still returned
    return img_b64


__all__ = ["render_graph", "display_visual_question"]
