from bs4 import BeautifulSoup
import requests, json

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}


def get_swap():
	r = requests.get('https://www.chathamfinancial.com/technology/european-market-rates', headers=headers)
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


