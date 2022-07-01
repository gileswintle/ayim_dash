import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# import plotly.express as px
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
from swap import get_swap
from p_layout import layout


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
    fr = layout(fr_yield_curve_range_chart())
    us = layout(us_yield_curve_range_chart())
    return fr, us


@st.cache(persist=True, allow_output_mutation=True, show_spinner=True, ttl=86400)
def reits():
    return layout(fr_prop_index_chart(), leg_alt=True)


@st.cache(persist=True, allow_output_mutation=True, show_spinner=True)
def scpi():
    return layout(scpi_net_sub_chart())


# @st.cache(persist=True, allow_output_mutation=True, show_spinner=True)
def bbb(days=90):
    df = pd.read_excel("data/bonds.xlsx")
    df.set_index("Date", inplace=True)
    df = df.iloc[-90:, 4]
    df = df.rename("Euro BBB")
    dte = datetime.datetime.now() - datetime.timedelta(days=days)
    for n in range(5):
        try:
            dte = pd.Timestamp((dte - datetime.timedelta(days=n)).date())
            st_val = df.loc[dte]
            break
        except KeyError:
            pass
    df = df.loc[dte : df.index[-1]]
    ch = f"{df.iloc[-1] - df.loc[dte]:,.2}%"
    return df, ch


# @st.cache(persist=True, allow_output_mutation=True, show_spinner=True)
def frt():
    df = pd.read_excel("data/bonds.xlsx")
    df.set_index("Date", inplace=True)
    df = df.iloc[-90:, 0]
    df = df.rename("OAT")
    dte = datetime.datetime.now() - datetime.timedelta(days=days)
    for n in range(5):
        try:
            dte = pd.Timestamp((dte - datetime.timedelta(days=n)).date())
            st_val = df.loc[dte]
            break
        except KeyError:
            pass
    df = df.loc[dte : df.index[-1]]
    ch = f"{df.iloc[-1] - df.loc[dte]:,.2}%"
    return df, ch


# # @st.cache(persist=True, allow_output_mutation=True, show_spinner=True)
# def swap():
#     df = pd.read_excel("data/bonds.xlsx")
#     df.set_index("Date", inplace=True)
#     df = df.iloc[-90:, 3]
#     df = df.rename("5y IR swap")
#     dte = datetime.datetime.now() - datetime.timedelta(days=days)
#     for n in range(5):
#         try:
#             dte = pd.Timestamp((dte - datetime.timedelta(days=n)).date())
#             st_val = df.loc[dte]
#             break
#         except KeyError:
#             pass
#     df = df.loc[dte : df.index[-1]]
    
#     _, last = get_swap()
#     ch = f"{last - df.loc[dte]:,.2}%"

#     return df, ch, last

@st.cache(persist=True, allow_output_mutation=True, show_spinner=True, ttl=86400)
def swap():
    df, last = get_swap()
    ch = f"{last - df.iloc[-1,0]:,.2}%"
    return df, ch, last

# @st.cache(persist=True, allow_output_mutation=True, show_spinner=True)
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

    days = 90
    df, ch = get_prices("^TNX", days, dps=2, pc_ch=True)
    st.metric(
        f"10-year US T-bill | {days} days", df.iloc[-1, -2], ch, delta_color="inverse"
    )
    if charts:
        st.area_chart(df["Adj Close"], height=200)

    days = 90
    df, ch = frt()
    st.metric(
        f"10-year French T-bill | {days} days", df.iloc[-1], ch, delta_color="inverse"
    )
    if charts:
        st.area_chart(df, height=200)

    days = 30
    df, ch, last = swap()
    st.metric(
        f"5-year Euro IR swap | {days} days", round(last, 2), ch, delta_color="inverse"
    )
    if charts:
        st.area_chart(df, height=200)

    days = 90
    df, ch = bbb()
    st.metric(
        f"10-year BBB Euro area | {days} days", df.iloc[-1], ch, delta_color="inverse"
    )
    if charts:
        st.area_chart(df, height=200)

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
    
    
from bond_composite import euronext
euronext()
