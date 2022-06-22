from pandas_datareader.data import DataReader as dr
import pandas as pd
import numpy as np
import plotly.express as px
import datetime, requests
from datetime import date, timedelta

from time_series_utils import *

import plotly


def yield_curve_us(start="2020-01-02", end=False):
    if end == False:
        end = start
    syms = ["DGS1", "DGS2", "DGS3", "DGS5", "DGS10"]
    df = dr(syms, "fred", start=start, end=end)
    if df.empty:
        return [np.nan]
    names = dict(zip(syms, ["1yr", "2yr", "3yr", "5yr", "10yr"]))
    df = df.rename(columns=names)
    df = df.interpolate()
    if start == end:
        return df.iloc[0, :]
    else:
        return df


def us_yield_curve_range(date):
    df = pd.DataFrame(columns=["1yr", "2yr", "3yr", "5yr", "10yr"])
    date_ = datetime.datetime.fromisoformat(date)
    curves = [
        date_,
        date_ - datetime.timedelta(days=90),
        date_ - datetime.timedelta(days=180),
        date_ - datetime.timedelta(days=360),
    ]
    curves = [d.strftime("%Y-%m-%d") for d in curves]
    names = [f"t={date}", "t-90 days", "t-180 days", "t-360 days"]
    for curve, name in zip(curves, names):
        cur_curve = [np.nan]
        while pd.isnull(
            cur_curve[0]
        ):  # keep running is API returns and error, wind back one day if no values for the date chosen
            try:
                cur_curve = yield_curve_us(start=curve)
                curve = datetime.datetime.fromisoformat(curve) - datetime.timedelta(
                    days=1
                )
                curve = curve.strftime("%Y-%m-%d")
            except KeyError:
                pass
        df.loc[name] = cur_curve
    return df


def us_yield_curve_range_chart(date=False, save_file=False):
    if date == False:
        date = datetime.datetime.now().strftime("%Y-%m-%d")
    df = us_yield_curve_range(date)
    print(df)
    fig = px.line(df.T, render_mode="svg")
    fig.update_layout(
        title="US treasury yield curve",
        xaxis_title="Maturity",
        yaxis_title="YTM %",
        legend_title="",
        yaxis_tickformat=",.1f",
    )

    return fig


if __name__ == "__main__":
    pass
