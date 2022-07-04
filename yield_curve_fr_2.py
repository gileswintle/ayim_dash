import requests
import pandas as pd
from bs4 import BeautifulSoup

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}


def get_curve():
	r = requests.get('https://www.investing.com/rates-bonds/france-government-bonds', headers=headers)

	soup = BeautifulSoup(r.text, 'html.parser')
	t = soup.select('#cross_rates_container')
	t = t[0].decode()
	df = pd.read_html(t)
	df = df[0]
	df.set_index('Name', inplace=True)
	df.drop(columns=['Unnamed: 0', 'Prev.', 'High', 'Low', 'Chg.', 'Chg. %', 'Time', 'Unnamed: 9'], inplace=True)
	ten = df.loc['France 10Y', 'Yield']
	five = df.loc['France 5Y', 'Yield']
	# print(df)

	return df, five, ten

def get_10():
	r = requests.get('https://www.investing.com/rates-bonds/france-10-year-bond-yield-historical-data', headers=headers)

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

def get_5():
	r = requests.get('https://www.investing.com/rates-bonds/france-5-year-bond-yield-historical-data', headers=headers)

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
	get_5()