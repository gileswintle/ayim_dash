import plotly.express as px


def layout(fig, title=False, leg=True, leg_alt=False):
    """
    add title and reduce margins
    """

    if title:
        fig.update_layout(
            title={
                "text": title,
                "y": 0.97,
                "x": 0.02,
                "xanchor": "left",
                "yanchor": "top",
            },
        )
    fig.update_layout(
        margin=dict(l=10, r=10, t=30, b=10),
        height=400,
    )
    if leg:
        fig.update_layout(
            legend=dict(
                bordercolor="rgb(100,100,100)",
                borderwidth=0,
                itemclick="toggleothers",  # when you are clicking an item in legend all that are not in the same group are hidden
                x=0,
                y=1 if leg_alt else 0,
                bgcolor="rgb(255, 255, 255, 0.4)",
            ),
            showlegend=True,
        )
    else:
        fig.update_layout(showlegend=False)
    return fig
