import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

import plotly.express as px
import datetime

# import numpy as np
# import requests

from pandas_datareader import data
import datetime
from yield_curve_fr import fr_yield_curve_range_chart
from yield_curve_us import us_yield_curve_range_chart
from scpi import scpi_net_sub_chart
from reit_stocks import fr_prop_index_chart
from indexation import index_chart
from euro_c_spreads import get_table
from yield_curves import get_curve, get_10, get_5
from swap import get_swap
from p_layout import layout
from bond_composite import composite

RERUN_HOUR = 0
LAST_RERUN_DATE = datetime.datetime.now() - datetime.timedelta(days=1, hours=1)

tickers = ['FR0013424876', 'FR0013505260', 'FR0014006ZC4', 'FR0014000D31', 'FR0014004FR9']

def is_rerun():
    n = datetime.datetime.now()
    if n.hour == RERUN_HOUR and (LAST_RERUN_DATE - datetime.datetime.now()) / datetime.timedelta(days=1) >= 1:
        return True
    else:
        return False



@st.cache(persist=True, allow_output_mutation=True, show_spinner=True, ttl=86400)
def get_prices(ticker, days=30, dps=0, pc_ch=False):
    start_date = f"{datetime.datetime.now()-datetime.timedelta(days=days):%Y-%m-%d}"
    end_date = f"{datetime.datetime.now():%Y-%m-%d}"

    df = data.DataReader(ticker, "yahoo", start_date, end_date)
    df["fmtClose"] = df["Adj Close"].apply(lambda x: f"{x:,.{dps}f}")
    df["change"] = df["Adj Close"].pct_change()
    df["change"] = df["change"].apply(lambda x: f"{x:,.2%}")
    if pc_ch:
        ch = f"{df['Adj Close'][-1] - df['Adj Close'][0]:,.2}%"
    else:
        ch = f"{(df['Adj Close'][-1] / df['Adj Close'][0]) - 1:,.2%}"
    return df, ch


@st.cache(persist=True, allow_output_mutation=True, show_spinner=True, ttl=86400)
def yield_curves():
    try:
        fr = layout(fr_yield_curve_range_chart())
        us = layout(us_yield_curve_range_chart())
    except:
        pass
    return fr, us


@st.cache(persist=True, allow_output_mutation=True, show_spinner=True, ttl=86400)
def reits():
    return layout(fr_prop_index_chart(), leg_alt=True)


@st.cache(persist=True, allow_output_mutation=True, show_spinner=True)
def scpi():
    return layout(scpi_net_sub_chart())

# @st.cache(persist=True, allow_output_mutation=True, show_spinner=True, ttl=86400)
def fr_corp_composite(tickers):
    df, fr_c, fr_spr = composite(tickers)
    return df, fr_c, fr_spr


def ind():
    return layout(index_chart(), leg_alt=True)

@st.cache(persist=True, allow_output_mutation=True, show_spinner=True, ttl=86400)
def c_spr():
    return get_table()

st.set_page_config(layout="wide")

st.title("AYIM European dashboard")

yfr, yus = yield_curves()
reits = reits()
scpi = scpi()
ind = ind()

c1, c2, c3 = st.columns([1, 2, 2])

with c1:
    charts = st.checkbox("Charts", value=False)

    df_u, last_u, thirty_day_u = get_10('u.s.')
    df_uk, last_uk, thirty_day_uk = get_10('uk')
    st.metric(
        f"10-year gov: USA | UK", f'{last_u} | {last_uk}', f'{thirty_day_u} | {thirty_day_uk} (30 day)', delta_color="inverse"
    )
    if charts:
        st.area_chart(df_u, height=200)
        st.area_chart(df_uk, height=200)

    df_f, last_f, thirty_day_f = get_10('france')
    df_g, last_g, thirty_day_g = get_10('germany')
    st.metric(
        f"10-year gov: France | Germany", f'{last_f} | {last_g}', f'{thirty_day_f} | {thirty_day_g} (30 day)', delta_color="inverse"
    )
    if charts:
        st.area_chart(df_f, height=200)
        st.area_chart(df_g, height=200)

    _, last_f, thirty_day_f = get_5('france')
    _, last_g, thirty_day_g = get_5('germany')
    st.metric(
        f"5-year gov: France | Germany", f'{last_f} | {last_g}', f'{thirty_day_f} | {thirty_day_g} (30 day)', delta_color="inverse"
    )
    if charts:
        st.area_chart(df_f, height=200)
        st.area_chart(df_g, height=200)

    
    df, last, thirty_day = get_swap()
    st.metric(
        f"5-year Euro IR swap | 30 days", round(last, 2), thirty_day, delta_color="inverse"
    )
    if charts:
        st.area_chart(df, height=200)

    df, fr_c, fr_spr = fr_corp_composite(tickers)
    st.metric(
        f"AYIM French corporate 10 year | spread", f'{fr_c:,.2%} | {fr_spr:,.2%}', '', delta_color="off"
    )
    if charts:
        st.dataframe(df)

    days = 90
    df, ch = get_prices("BTC-USD", days)
    st.metric(f"BitCoin:USD | {days} days", df.iloc[-1, -2], ch)
    if charts:
        st.area_chart(df["Adj Close"], height=200)

    days = 90
    df, ch = get_prices("^GSPC", days)
    st.metric(f"S&P 500 | {days} days", df.iloc[-1, -2], ch)
    if charts:
        st.area_chart(df["Adj Close"], height=200)

    days = 90
    df, ch = get_prices("^FCHI", days)
    st.metric(f"CAC 40 | {days} days", df.iloc[-1, -2], ch)
    if charts:
        st.area_chart(df["Adj Close"], height=200)

    days = 90
    df, ch = get_prices("AMZN", days)
    st.metric(f"Amazon | {days} days", df.iloc[-1, -2], ch)
    if charts:
        st.area_chart(df["Adj Close"], height=200)

    days = 90
    df, ch = get_prices("NFLX", days)
    st.metric(f"Netflix | {days} days", df.iloc[-1, -2], ch)
    if charts:
        st.area_chart(df["Adj Close"], height=200)


with c2:
    st.plotly_chart(yfr, use_container_width=True)
    st.plotly_chart(ind, use_container_width=True)
    st.write('Country spread: 10-year bonds (source: MTS)')
    components.html(c_spr(), width=400, height=600)
    

with c3:
    st.plotly_chart(yus, use_container_width=True)
    st.plotly_chart(reits, use_container_width=True)
    st.plotly_chart(scpi, use_container_width=True)
    
    
