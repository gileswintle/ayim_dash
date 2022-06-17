import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
# import plotly.express as px
import datetime
# import numpy as np
# import requests

from pandas_datareader import data
import datetime



def get_prices(ticker, days=30, dps=0):
    start_date = f'{datetime.datetime.now()-datetime.timedelta(days=days):%Y-%m-%d}'
    end_date = f'{datetime.datetime.now():%Y-%m-%d}'


    df = data.DataReader(ticker, 'yahoo', start_date, end_date) 
    df['fmtClose'] = df['Adj Close'].apply(lambda x : f'{x:,.{dps}f}')
    df['change'] = df['Adj Close'].pct_change()
    df['change'] = df['change'].apply(lambda x : f'{x:,.2%}')
    ch = f"{(df['Adj Close'][-1] / df['Adj Close'][0]) - 1:,.2%}"
    return df, ch



# colors = px.colors.qualitative.Alphabet

st.set_page_config(layout="wide")

st.title("AYIM dashboard")

c1, c2 = st.columns(2)

with c1:

    days = 90
    df, ch = get_prices('BTC-USD', days)
    st.metric(f'BitCoin:USD | {days} days', df.iloc[-1, -2], ch)
    # st.area_chart(df['Adj Close'], height=200)

    days = 90
    df, ch = get_prices('^TNX', days, dps=2)
    st.metric(f'10 year US T-bill | {days} days', df.iloc[-1, -2], ch, delta_color="inverse")
    # st.area_chart(df['Adj Close'], height=200)

    days = 90
    df, ch = get_prices('^GSPC', days)
    st.metric(f'S&P 500 | {days} days', df.iloc[-1, -2], ch)
    # st.area_chart(df['Adj Close'], height=200)

with c2:
    days = 90
    df, ch = get_prices('^FCHI', days)
    st.metric(f'CAC 40 | {days} days', df.iloc[-1, -2], ch)
    # st.area_chart(df['Adj Close'], height=200)


    days = 90
    df, ch = get_prices('AMZN', days)
    st.metric(f'Amazon | {days} days', df.iloc[-1, -2], ch)
    # st.area_chart(df['Adj Close'], height=200)

    days = 90
    df, ch = get_prices('NFLX', days)
    st.metric(f'Netflix | {days} days', df.iloc[-1, -2], ch)
    # st.area_chart(df['Adj Close'], height=200)