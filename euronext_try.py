import datetime, requests, time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

from time_series_utils import *




def euronext_2():
	url = "https://live.euronext.com/en/product/bonds/FR0013424876-XPAR"
	headers = [
            {
              "name": "Accept",
              "value": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
            },
            {
              "name": "Accept-Encoding",
              "value": "gzip, deflate, br"
            },
            {
              "name": "Accept-Language",
              "value": "en-GB,en;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6"
            },
            {
              "name": "Cache-Control",
              "value": "max-age=0"
            },
            {
              "name": "Connection",
              "value": "keep-alive"
            },
            {
              "name": "Cookie",
              "value": "cookie-agreed-version=1.0.1; cookie-agreed-categories=%5B%22necessary%22%2C%22performance%22%5D; cookie-agreed=2; _ga=GA1.2.50813507.1656604857; _gid=GA1.2.1493930251.1656604857; _gcl_au=1.1.1448788204.1656604972; _hjSessionUser_1305322=eyJpZCI6IjgzYzVmOGRlLTYyMzQtNWIwMC05N2ZmLTEyYTJjOWY2MDdkNyIsImNyZWF0ZWQiOjE2NTY2MDQ5NzIwNzYsImV4aXN0aW5nIjp0cnVlfQ==; _hjAbsoluteSessionInProgress=0; _hjSession_1305322=eyJpZCI6IjRiM2NlMDcyLTAwZGEtNDA0Yy1hZjcxLTkxMTUwZDlkNTY1YyIsImNyZWF0ZWQiOjE2NTY2ODg2MTQxMTgsImluU2FtcGxlIjpmYWxzZX0=; _hjIncludedInSessionSample=0; _hjShownFeedbackMessage=True; TS01a5de3f=015c8de707a6a2571639a2c7b437502173cf4e8b9ba7c3b895a1b087154aca1719db7561b7"
            },
            {
              "name": "Host",
              "value": "live.euronext.com"
            },
            {
              "name": "If-None-Match",
              "value": "\"1656688613-gzip\""
            },
            {
              "name": "Referer",
              "value": "https://live.euronext.com/en/product/bonds/FR0013424876-XPAR/market-information"
            },
            {
              "name": "Sec-Fetch-Dest",
              "value": "document"
            },
            {
              "name": "Sec-Fetch-Mode",
              "value": "navigate"
            },
            {
              "name": "Sec-Fetch-Site",
              "value": "same-origin"
            },
            {
              "name": "Sec-Fetch-User",
              "value": "?1"
            },
            {
              "name": "Upgrade-Insecure-Requests",
              "value": "1"
            },
            {
              "name": "User-Agent",
              "value": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
            },
            {
              "name": "sec-ch-ua",
              "value": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"102\", \"Google Chrome\";v=\"102\""
            },
            {
              "name": "sec-ch-ua-mobile",
              "value": "?0"
            },
            {
              "name": "sec-ch-ua-platform",
              "value": "\"Windows\""
            }
          ]
	headers = {d['name'] : d['value'] for d in headers}
	cookies = [
            {
              "name": "cookie-agreed-version",
              "value": "1.0.1",
              "path": "/",
              "domain": "live.euronext.com",
              "expires": "2022-10-07T17:26:39.000Z",
              "httpOnly": False,
              "secure": False
            },
            {
              "name": "cookie-agreed-categories",
              "value": "%5B%22necessary%22%2C%22performance%22%5D",
              "path": "/",
              "domain": "live.euronext.com",
              "expires": "2022-10-07T17:26:39.000Z",
              "httpOnly": False,
              "secure": False
            },
            {
              "name": "cookie-agreed",
              "value": "2",
              "path": "/",
              "domain": "live.euronext.com",
              "expires": "2022-10-07T17:26:39.000Z",
              "httpOnly": False,
              "secure": False
            },
            {
              "name": "_ga",
              "value": "GA1.2.50813507.1656604857",
              "path": "/",
              "domain": ".euronext.com",
              "expires": "2024-06-30T15:16:53.000Z",
              "httpOnly": False,
              "secure": False
            },
            {
              "name": "_gid",
              "value": "GA1.2.1493930251.1656604857",
              "path": "/",
              "domain": ".euronext.com",
              "expires": "2022-07-02T15:16:53.000Z",
              "httpOnly": False,
              "secure": False
            },
            {
              "name": "_gcl_au",
              "value": "1.1.1448788204.1656604972",
              "path": "/",
              "domain": ".euronext.com",
              "expires": "2022-09-28T16:02:51.000Z",
              "httpOnly": False,
              "secure": False
            },
            {
              "name": "_hjSessionUser_1305322",
              "value": "eyJpZCI6IjgzYzVmOGRlLTYyMzQtNWIwMC05N2ZmLTEyYTJjOWY2MDdkNyIsImNyZWF0ZWQiOjE2NTY2MDQ5NzIwNzYsImV4aXN0aW5nIjp0cnVlfQ==",
              "path": "/",
              "domain": ".euronext.com",
              "expires": "2023-07-01T15:16:54.000Z",
              "httpOnly": False,
              "secure": True,
              "sameSite": "Lax"
            },
            {
              "name": "_hjAbsoluteSessionInProgress",
              "value": "0",
              "path": "/",
              "domain": ".euronext.com",
              "expires": "2022-07-01T15:51:23.000Z",
              "httpOnly": False,
              "secure": True,
              "sameSite": "Lax"
            },
            {
              "name": "_hjSession_1305322",
              "value": "eyJpZCI6IjRiM2NlMDcyLTAwZGEtNDA0Yy1hZjcxLTkxMTUwZDlkNTY1YyIsImNyZWF0ZWQiOjE2NTY2ODg2MTQxMTgsImluU2FtcGxlIjpmYWxzZX0=",
              "path": "/",
              "domain": ".euronext.com",
              "expires": "2022-07-01T15:51:23.000Z",
              "httpOnly": False,
              "secure": True,
              "sameSite": "Lax"
            },
            {
              "name": "_hjIncludedInSessionSample",
              "value": "0",
              "path": "/",
              "domain": "live.euronext.com",
              "expires": "2022-07-01T15:31:54.000Z",
              "httpOnly": False,
              "secure": True,
              "sameSite": "Lax"
            },
            {
              "name": "_hjShownFeedbackMessage",
              "value": "True",
              "path": "/",
              "domain": "live.euronext.com",
              "expires": "2022-07-02T15:16:54.000Z",
              "httpOnly": False,
              "secure": True,
              "sameSite": "Lax"
            },
            {
              "name": "TS01a5de3f",
              "value": "015c8de707a6a2571639a2c7b437502173cf4e8b9ba7c3b895a1b087154aca1719db7561b7",
              "path": "/",
              "domain": "live.euronext.com",
              "expires": "1969-12-31T23:59:59.000Z",
              "httpOnly": False,
              "secure": True
            }
          ]
	cookies = {d['name'] : d['value'] for d in cookies}
	r = requests.get(url, headers=headers, cookies=cookies)
	with open('test.html', 'w') as f:
		f.write(r.text)




if __name__ == "__main__":
	euronext_2()

