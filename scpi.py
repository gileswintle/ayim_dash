import pandas as pd
import numpy as np
import plotly.express as px
import datetime, requests
from datetime import date, timedelta

from time_series_utils import *


SCPI_NET_SUBS = pd.DataFrame(columns=["net_subs"])
SCPI_NET_SUBS.loc["2015"] = 4.275477418
SCPI_NET_SUBS.loc["2016"] = 5.561838971
SCPI_NET_SUBS.loc["2017"] = 6.331316781
SCPI_NET_SUBS.loc["2018"] = 5.109482403
SCPI_NET_SUBS.loc["2019"] = 8.606244359
SCPI_NET_SUBS.loc["2020"] = 6.031629206
SCPI_NET_SUBS.loc["2021"] = 7.369799502


def scpi_net_sub_chart(df=SCPI_NET_SUBS):

    labels = ["-"]
    for n, v in enumerate(df["net_subs"].iloc[1:]):
        delta = v / df["net_subs"].iloc[n] - 1
        labels.append(f"{delta:+.0%}")

    fig = px.bar(df, x=df.index, y="net_subs")
    fig.update_layout(
        title=f"SCPI net new subscriptions",
        xaxis_title="Year",
        yaxis_title="Bn Euros",
        legend_title="",
        yaxis_tickformat=",.0f",
    )
    fig.update_traces(
        marker_color="#000fff",
        text=labels,
        textposition="outside",
        textfont=dict(
            family="arial",
            size=10,
            color="#000fff",
        ),
    )

    min_y = 0 if min(df["net_subs"]) > 0 else min(df["net_subs"])
    fig.layout.yaxis.update(range=[min_y, max(df["net_subs"]) * 1.1])

    return fig


if __name__ == "__main__":
    pass
