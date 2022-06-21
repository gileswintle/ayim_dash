from pandas_datareader.data import DataReader as dr
import pandas as pd
import numpy as np
import plotly.express as px
import datetime, requests
from datetime import date, timedelta

from time_series_utils import *



def fr_property_stocks(start='2020-01-02', end=False):
    if end == False:
        end = start
    syms = ['GFC.PA', 'LI.PA', 'URW.AS', "BLND.L", "LAND.L", 'ARE', 'BXP', '^FCHI',  '^GSPC', '^IXIC']
    df = dr(syms, 'yahoo', start=start, end=end)['Adj Close']
    if df.empty:
        return [np.nan]
    names = dict(zip(syms, ['Gecina', 'Klepierre (Retail)', 'Unibail (Retail/Office)', 'British Land', 'Land Securities',  
    'Alexandria (Life Sciences)', 'Boston Properties (Office)','CAC40',  'S&P500', 'NASDAQ']))
    df = df.rename(columns=names)
    df = df.interpolate()
    if start == end:
        return df.iloc[0, :]
    else:
        return df

def fr_prop_index(start='2020-03-10', end='2021-03-10'):
    df = fr_property_stocks(start=start, end=end)
    col_nos = [x for x in range(len(df.columns))]
    print(col_nos)
    df = rebase_ind(df, col_nos=col_nos)
    return df

def fr_prop_index_chart(start=False, end=False, days=90):
    if end == False:
        end = datetime.datetime.now()
        end = end.strftime("%Y-%m-%d")
    if days:
        start = datetime.datetime.fromisoformat(end) - datetime.timedelta(days=days)
        start = start.strftime("%Y-%m-%d")
    else:
        days = (datetime.datetime.fromisoformat(end) - datetime.datetime.fromisoformat(start)) / datetime.timedelta(days=1)

    df = fr_prop_index(start=start, end=end)
    print(df)
    yaxis_max = df.max().max()
    yaxis_min = df.min().min()
    dist = max(yaxis_max - 100, 100 - yaxis_min)
    yaxis_set_max = 100 + dist * 1.1
    yaxis_set_min = 100 - dist * 1.1


    fig = px.line(df, render_mode="svg")
    fig.update_layout(
        title=f"Listed real estate (index over {days} days)",
        xaxis_title="Date",
        yaxis_title="Index",
        legend_title="",
        yaxis_tickformat=',.0f',
        yaxis_range=[yaxis_set_min, yaxis_set_max],
    )
    fig.update_layout(
        shapes=[
            dict(
                type="rect",
                xref="x",
                yref="y",
                x0=df.index.min(),
                y0=0,
                x1=df.index.max(),
                y1=100,
                fillcolor="lightgray",
                opacity=0.4,
                line_width=0,
                layer="below"
            ),
        ]
    )
    return fig

if __name__ == "__main__":
    pass