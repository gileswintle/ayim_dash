from bs4 import BeautifulSoup
import requests, json


def get_swap():
	r = requests.get('https://www.chathamfinancial.com/technology/european-market-rates')
	soup = BeautifulSoup(r.text, 'html.parser')
	for d in soup.find_all('div'):
		if 'data-config' in d.attrs:
			c = d['data-config']
			c = json.loads(c)
			title = c['chartTitle']
			if title == '3-month EURIBOR swaps':
				t = d.find_next('table')
				td = t.find_all('td')
				print(td)
	
	


if __name__ == "__main__":
	get_swap()


