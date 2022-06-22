import requests
from bs4 import BeautifulSoup



def get_table():
	r = requests.get('https://www.mtsmarkets.com/european-bond-spreads')

	soup = BeautifulSoup(r.text)

	tabs = []
	for i in soup.find_all('div'):
	    if 'class' in i.attrs:
	        if 'data-tabs-table-wrapper' in i['class']:
	            for t in i.find_all('table'):
	                if 'class' in i.attrs:
	                    if 'data-tabs-table' in t['class']:
	                        tabs.append(t)
	                        
	html = tabs[2].decode()

	css = '''
	<style>


	table {
    border-collapse: collapse;
    width: 100%;
    border: 1px solid #ddd;
    font-size: 10px;
    font-family: Arial;
  }
  
  table th, table td {
    text-align: left; 
    padding: 3px;
  }
  
  table tr {
    border-bottom: 1px solid #ddd;
  }
  
  table tr.header{
    background-color: #f1f1f1;
  }
  
  table tr.header-b{
    /* Add a grey background color to the table header and on hover */
    background-color: #f1f1f1;
    font-weight: bold;
  }
  

  </style>

	'''
	
	return css + html