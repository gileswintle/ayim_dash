from pandas_datareader.data import DataReader as dr
import pandas as pd
import numpy as np
import plotly.express as px
import datetime, requests
from datetime import date, timedelta
from bs4 import BeautifulSoup

from time_series_utils import *

def bonds(start="2020-01-02", end=False):
    if end == False:
        end = start
    syms = [
        "FR0013424876 ",

    ]
    df = dr(syms, "yahoo", start=start, end=end)["Adj Close"]
    if df.empty:
        return [np.nan]
    names = dict(
        zip(
            syms,
            [
                "Vivendi",
 
            ],
        )
    )
    df = df.rename(columns=names)
    df = df.interpolate()
    if start == end:
        return df.iloc[0, :]
    else:
        return df

# https://www.alphavantage.co/documentation/
def av():
	key = '3BIGD4WQ7S60E8XM'
	ticker = 'IBM'
	url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=5min&apikey={key}'
	r = requests.get(url)
	data = r.json()
	print(data)


headers = {
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
	'accept' : '*/*',
	'referer': 'https://live.euronext.com/en/product/bonds/FR0013424876-XPAR/market-information',
	'host': 'live.euronext.com',
	'cookie': 'cookie-agreed-version=1.0.1',
	'connection': 'keep-alive'
}

def euronext():
	# ticker = 'FR0013424876'
	# r = requests.get(f'https://live.euronext.com/en/product/bonds/FR0013424876-XPAR', headers=headers)
	# soup = BeautifulSoup(r.text, 'html.parser')
	from selenium import webdriver
	from webdriver_manager.chrome import ChromeDriverManager
	# from selenium.webdriver.chrome.options import Options

	# options = Options()
	# options.add_argument("no-sandbox")
	# options.add_argument("headless")
	# options.add_argument("start-maximized")
	# options.add_argument("window-size=1900,1080")

	driver = webdriver.Chrome(ChromeDriverManager().install())

	url = "https://live.euronext.com/en/product/bonds/FR0013424876-XPAR/market-information"
	browser = driver
	browser.get(url)
	import time
	time.sleep(1)
	html = browser.page_source
	soup = BeautifulSoup(html, 'lxml')
	# for d in soup.find_all('td'):
	# 	print(d)
	# 	if 'class' in d.attrs:
	# 		if 'table-success' in d['class']:
	# 			print(d)
	price = soup.select('#detailed_quote_holder > div > div > div.data-header > div > div.data-header__col.data-header__col-right.bg-white > div > h5:nth-child(1) > span:nth-child(2)')
	print(price[0].text)

def ff():
	url = 'https://www.boerse-frankfurt.de/bond/fr0013424876-vivendi-se-1-125-19-28'
	r = requests.get(url)
	soup = BeautifulSoup(r.text)

	price = soup.select('body > app-root > app-wrapper > div > div.content-wrapper > app-bond > div.ng-star-inserted > div:nth-child(3) > div.col-12.col-lg-6.ar-half-pr-lg.ar-mt > app-price-information > div > div > div > div > table > tbody > tr:nth-child(4) > td.widget-table-cell.text-right')
	print(price)

def en2():
	headers = {
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
	'accept' : '*/*',
	'referer': 'https://live.euronext.com/en/product/bonds/FR0013424876-XPAR/market-information',
	'host': 'live.euronext.com',
	'cookie': 'cookie-agreed-version=1.0.1',
	'connection': 'keep-alive',
	'sec-fetch-mode': 'cors',
	'sec-fetch-site': 'same-origin',
	'cookie': 'cookie-agreed-version=1.0.1; cookie-agreed-categories=%5B%22necessary%22%2C%22performance%22%5D; cookie-agreed=2; _hjShownFeedbackMessage=true; _hjFirstSeen=1; _hjIncludedInSessionSample=0; TS01a5de3f=01010d14936e38cd5f36f2d932c6ae495dd66b8531e0a3a3e96721aaff2d7dcc6262afaab6',

}
	payload = {'theme_name': 'euronext_live'}
	r = requests.post('https://live.euronext.com/en/ajax/getDetailedQuote/FR0013424876-XPAR', params=payload, headers=headers)
	print('HERE', r.headers)

def br():
	ticker = 'FR0013424876' 
	url = f'https://www.boursorama.com/bourse/obligations/cours/1rP{ticker}/'
	r = requests.get(url)
	soup = BeautifulSoup(r.text, "html.parser")
	price = soup.select('#main-content > div > section.l-quotepage > header > div > div > div.c-faceplate__company > div.c-faceplate__info > div > div.c-faceplate__price.c-faceplate__price--inline > span.c-instrument.c-instrument--last')
	print(price[0].text)

if __name__ == "__main__":
	euronext()

	# <div class="data-header__row head_detail_bottom head_detail__height bg-ui-grey-4">
	# 																										<h5 class="col">
	# 										<span class="text-ui-grey-1 data-12 font-weight-bold">Best Bid</span>
	# 										<span>86.95</span>
	# 									</h5>
	# 									<h5 class="col">
	# 										<span class="text-ui-grey-1 data-12 font-weight-bold">Best Ask</span>
	# 										<span>200.00</span>
	# 									</h5>
	# 									<div class="col">
	# 																						<span class="text-ui-grey-1 data-10">30/06/2022 - 16:14
	# 												&nbsp;CET</span>
	# 																				</div>

																	
	# 																<div class="icons__column icons__column--column-direction">
	# 									<ul class="icons__listing">
	# 										<li>
	# 											<button type="button" class="btn btn-link p-0 ml-auto mr-2" role="button" data-toggle="popover" data-placement="bottom" data-trigger="focus" data-html="true" data-content="Prices for the latest traded session are displayed unadjusted." data-original-title="" title="">
	# 												<svg viewBox="0 0 24 24" width="24" height="24" role="presentation" class="">
	# 													<use xlink:href="/themes/custom/euronext_live/frontend-library/public/assets//spritemap.svg#info"></use>
	# 												</svg>
	# 											</button>
	# 										</li>
	# 									</ul></div>
									

	# 							</div>