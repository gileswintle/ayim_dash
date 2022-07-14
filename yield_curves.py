import requests
import pandas as pd
from bs4 import BeautifulSoup

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}


def get_curve(country):
	r = requests.get(f'https://www.investing.com/rates-bonds/{country}-government-bonds', headers=headers)

	soup = BeautifulSoup(r.text, 'html.parser')
	t = soup.select('#cross_rates_container')
	t = t[0].decode()
	df = pd.read_html(t)
	df = df[0]
	df.set_index('Name', inplace=True)
	df.drop(columns=['Unnamed: 0', 'Prev.', 'High', 'Low', 'Chg.', 'Chg. %', 'Time', 'Unnamed: 9'], inplace=True)
	df.columns=['yield']
	terms = []
	for i in df.index:
		n = i.index(' ')
		t_str = i[n+1:]
		t = i[-1]
		n = int(t_str[:-1])
		n = n * 12 if t == 'Y' else n
		terms.append(n)
	df['term'] = terms
	df.set_index('term', inplace=True)
	# print(df)
	return df

def get_rf(term_months, country):
	df = get_curve(country)
	for n, i in enumerate(df.index):
		if term_months >= i:
			lower = i
			upper = df.index[n+1]
	inc = round((term_months - lower) / (upper - lower), 2)
	rf = round(df.loc[lower, 'yield']  + (inc * (df.loc[upper, 'yield'] - df.loc[lower, 'yield'])), 2)
	# print(df, 'between', lower, upper, inc, rf)
	return rf

def get_10(country):
	r = requests.get(f'https://www.investing.com/rates-bonds/{country}-10-year-bond-yield-historical-data', headers=headers)

	soup = BeautifulSoup(r.text, 'html.parser')
	t = soup.select('#results_box')
	t = t[0].decode()
	df = pd.read_html(t)
	df = df[0]
	df.set_index('Date', inplace=True)
	df.index = pd.to_datetime(df.index)
	df.drop(columns=['Open', 'High', 'Low', 'Change %'], inplace=True)
	last = round(df.iloc[0, 0], 2)
	thirty_day = round(last - df.iloc[-1, 0], 2)
	# print(df)
	return df, last, thirty_day

def get_5(country):
	r = requests.get(f'https://www.investing.com/rates-bonds/{country}-5-year-bond-yield-historical-data', headers=headers)

	soup = BeautifulSoup(r.text, 'html.parser')
	t = soup.select('#results_box')
	t = t[0].decode()
	df = pd.read_html(t)
	df = df[0]
	df.set_index('Date', inplace=True)
	df.index = pd.to_datetime(df.index)
	df.drop(columns=['Open', 'High', 'Low', 'Change %'], inplace=True)
	last = round(df.iloc[0, 0], 2)
	thirty_day = round(last - df.iloc[-1, 0], 2)
	# print (df)
	return df, last, thirty_day

if __name__ == "__main__":
	# get_5('france')
	# get_curve('france')
	get_rf(65, 'france')