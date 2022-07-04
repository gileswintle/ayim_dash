import requests
import pandas as pd
from bs4 import BeautifulSoup

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}


def get_swap():
	r = requests.get('https://www.investing.com/rates-bonds/eur-5-years-irs-interest-rate-swap-historical-data', headers=headers)

	soup = BeautifulSoup(r.text, 'html.parser')
	t = soup.select('#curr_table')
	t = t[0].decode()
	df = pd.read_html(t)
	df = df[0]
	df.set_index('Date', inplace=True)
	df.index = pd.to_datetime(df.index)
	df.drop(columns=['Open', 'High', 'Low', 'Change %'], inplace=True)
	last = round(df.iloc[0, 0], 2)
	thirty_day = round(last - df.iloc[-1, 0], 2)
	print(df)

	return df, last, thirty_day

if __name__ == "__main__":
	get_swap()
