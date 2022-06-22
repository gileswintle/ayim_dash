import pandas as pd
import plotly.express as px
import datetime
import numpy as np
import requests


BOF_KEY = "e9deeee0-7c17-44bf-a0c9-60296e11c51b"


def banque_de_france(
    category="FM",
    series="FM.D.FR.EUR.FR2.BB.FRMOYTEC1.HSTA",
    start="2020-06-30",
    end="2020-06-30",
):
    df = pd.DataFrame(columns=["Value"])
    endpoint = f"https://api.webstat.banque-france.fr/webstat-en/v1/data/{category}/{series}?format=json&detail=dataonly&startPeriod={start}&endPeriod={end}&client_id={BOF_KEY}"

    params = {"accept": "application/json"}
    response = requests.get(endpoint, params=params).json()
    series = response["seriesObs"]

    for i in series:
        series = i["ObservationsSerie"]
        obs = series["observations"]
        for ob in obs:
            entry = ob["ObservationPeriod"]
            df.loc[entry["periodFirstDate"]] = entry["value"]
    if df.empty:
        return np.nan
    if start == end:
        return df.iloc[0, 0]
    else:
        return df


def fr_yield_curve(date):
    codes = [
        "FM.D.FR.EUR.FR2.BB.FRMOYTEC1.HSTA",
        "FM.D.FR.EUR.FR2.BB.FRMOYTEC2.HSTA",
        "FM.D.FR.EUR.FR2.BB.FRMOYTEC3.HSTA",
        "FM.D.FR.EUR.FR2.BB.FRMOYTEC5.HSTA",
        "FM.D.FR.EUR.FR2.BB.FRMOYTEC10.HSTA",
    ]
    names = ["1yr", "2yr", "3yr", "5yr", "10yr"]
    rates = []
    for code, name in zip(codes, names):
        rates.append(banque_de_france(category="FM", series=code, start=date, end=date))
    return names, rates


def fr_yield_curve_range(date):
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
                _, cur_curve = fr_yield_curve(curve)
                curve = datetime.datetime.fromisoformat(curve) - datetime.timedelta(
                    days=1
                )
                curve = curve.strftime("%Y-%m-%d")
            except KeyError:
                pass
        df.loc[name] = cur_curve
    return df


def fr_yield_curve_range_chart(date=False):
    if date == False:
        date = datetime.datetime.now().strftime("%Y-%m-%d")
    df = fr_yield_curve_range(date)
    fig = px.line(df.T, render_mode="svg")
    fig.update_layout(
        title="French treasury yield curve",
        xaxis_title="Maturity",
        yaxis_title="YTM %",
        legend_title="",
        yaxis_tickformat=",.1f",
    )

    return fig


if __name__ == "__main__":
    pass
