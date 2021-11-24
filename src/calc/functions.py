import math
from typing import Any, Dict, Optional

import plotly.graph_objects as go
import streamlit as st


def round_decimals_down(number: float, decimals: int = 2):
    """
    Returns a value rounded down to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.ceil(number)

    factor = 10 ** decimals
    return math.floor(number * factor) / factor


def create_plotly_table(data: Dict[str, Optional[Any]]):
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=list(data.keys()),
                    line_color="white",
                    fill_color="white",
                    font=dict(size=12, color="black"),
                    align="left",
                ),
                cells=dict(
                    values=[data.get(k) for k in data.keys()],
                    align="left",
                    fill=dict(color=[["#F9F9F9", "#FFFFFF"] * 5]),
                ),
            )
        ]
    )

    fig.update_layout(
        autosize=False,
        height=150,
        margin=dict(
            l=20,
            r=20,
            b=10,
            t=30,
        ),
    )

    st.write(fig)


def local_css(file_name: str) -> str:
    with open(file_name) as f:
        st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)


def percentage_format(x: float) -> str:
    return f"{x:.0%}"
