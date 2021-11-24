import numpy as np
import plotly.graph_objects as go


def draw_user_retention(df):
    z = df.values
    x = df.columns
    y = df.index
    annotations = []

    for n, row in enumerate(z):
        for m, val in enumerate(row):
            annotations.append(
                dict(
                    text="{0:.0%}".format(z[n][m]) if not np.isnan(z[n][m]) else "",
                    x=x[m],
                    y=y[n],
                    xref="x1",
                    yref="y1",
                    showarrow=False,
                )
            )

    layout = dict(
        title="Cohorts: User Retention",
        title_x=0.5,
        annotations=annotations,
        yaxis=dict(
            showgrid=False,
            tickmode="array",
            ticktext=y,
            autorange="reversed",
        ),
        xaxis=dict(showgrid=False),
        width=700,
        height=700,
        autosize=False,
    )
    trace = go.Heatmap(x=x, y=y, z=z, colorscale="Viridis")
    fig = go.Figure(data=trace, layout=layout)

    return fig
