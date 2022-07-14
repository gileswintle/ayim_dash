import datetime, requests, time, math
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from yield_curves import get_rf

from time_series_utils import *


BONDS = {'Vivendi'}


# https://www.alphavantage.co/documentation/
def alphavantage(ticker):
	key = '3BIGD4WQ7S60E8XM'
	url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=5min&apikey={key}'
	r = requests.get(url)
	data = r.json()
	return data


def euronext(ticker):
	if ticker[:2] == 'FR':
		country = 'france'
		
	if ticker[:2] == 'DE':
		country = 'germany'
		
	driver = webdriver.Chrome(ChromeDriverManager().install())
	url = f"https://live.euronext.com/en/product/bonds/{ticker}-XPAR/market-information"
	print(url)
	browser = driver
	browser.get(url)
	time.sleep(2)
	html = browser.page_source
	soup = BeautifulSoup(html, 'html.parser')
	issuer = soup.select('#fs_issuerinfo_block > div > div.card-body > p:nth-child(1) > strong')
	issuer = issuer[0].text
	issuer = issuer.title()
	price = soup.select('#detailed_quote_holder > div > div > div.data-header > div > div.data-header__col.data-header__col-right.bg-white > div > h5:nth-child(1) > span:nth-child(2)')
	price = float(price[0].text)
	repayment_date = soup.select('#fs_instrumentinfo_block > div > div.card-body > div > table > tbody > tr:nth-child(4) > td:nth-child(2) > strong')
	repayment_date = repayment_date[0].text
	repayment_date = datetime.datetime(year=int(repayment_date[-4:]), month=int(repayment_date[3:5]), day=int(repayment_date[0:2]))
	term = (repayment_date - datetime.datetime.now()) / datetime.timedelta(days=365)
	i = soup.select('#fs_couponinfo_block > div > div.card-body > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > strong')
	i = float(i[0].text.replace('%', ''))/100
		
	num_pay = math.floor(term*4)
	coupon = i * 100
	q_coupon = coupon / 4

	ytm = (1 + q_coupon / price)**3 - 1 + q_coupon / price + (100 / price)**(1/term) - 1 
	rf = get_rf(term * 12, country) / 100
	spread = ytm - rf
	ten_yr_equiv = (get_rf(120, country) / 100 ) + spread

	return issuer, i, term, price, ytm, rf, spread, ten_yr_equiv

def euronext_mult(tickers):
	df = pd.DataFrame(columns=['issuer', 'coupon', 'term', 'price', 'ytm', 'rf', 'spread', '10yr equivalent'])
	for n, ticker in enumerate(tickers):
		data = euronext(ticker)
		# print(data)
		df.loc[n] = data
	df.set_index('issuer', inplace=True)
	df.loc['Average'] = df.mean(axis=0)
	df.to_excel('bond_composite.xlsx')
	return df

	# compare with risk free at same term to give spread

if __name__ == "__main__":
	tickers = ['FR0013424876', 'FR0013505260', 'FR0014006ZC4', 'FR0014000D31', 'FR0014004FR9']

	print(euronext_mult(tickers))



