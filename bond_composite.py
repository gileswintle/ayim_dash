import requests, datetime
from bs4 import BeautifulSoup
from yield_curves import get_rf
import pandas as pd



def euronext_repay_date(code, exchange='XPAR'):

    url = f"https://live.euronext.com/en//ajax/getFactsheetInfoBlock/BONDS/{code}-{exchange}/fs_instrumentinfo_block"

    payload = ""
    headers = {
        "cookie": "TS01a5de3f=01010d149375e97fce1f83a1bfad22f3c41f36da772cfea775636e47afe818275abe2faf9f",
        "Accept": "*/*",
        "Accept-Language": "en-GB,en;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Cookie": "cookie-agreed-version=1.0.1; cookie-agreed-categories=^%^5B^%^22necessary^%^22^%^2C^%^22performance^%^22^%^5D; cookie-agreed=2; visid_incap_2691598=nzxxTqEqQAi9XFfYveHMvL0QxGIAAAAAQUIPAAAAAAD+ET0tgUt39FfN4haWMtKO; _gcl_au=1.1.635390176.1657016512; _ga=GA1.2.1300778173.1657016512; _hjSessionUser_1305322=eyJpZCI6IjQ2OTg4MWYyLWVhMWUtNTc4Ni1iMzk0LWExNTIwNjE3YzA5ZSIsImNyZWF0ZWQiOjE2NTcwMTY1MTI0MDAsImV4aXN0aW5nIjp0cnVlfQ==; incap_ses_1176_2691598=KDPQcPQWBwUb9jUYG/5REL3Fz2IAAAAA1IlJY7KMJH8UpBdBgoA2HA==; _gid=GA1.2.443853341.1657783743; _hjSession_1305322=eyJpZCI6ImEyZDY4MmQwLWMwNTItNDBlOS04NDIwLWI3NDJjZWQxYTQxOSIsImNyZWF0ZWQiOjE2NTc3ODM3NDM0OTAsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _hjShownFeedbackMessage=true; TS01a5de3f=01010d1493d771ef9e0ab21586b288f71131d01cb47caccaa0293153331c602b46c2a22597; _gat_UA-46900155-5=1; _hjIncludedInSessionSample=0",
        "Referer": "https://live.euronext.com/en/product/bonds/FR0013424876-XPAR/market-information",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": "^\^.Not/A",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "^\^Windows^^"
    }

    r = requests.get(url, data=payload, headers=headers)

    soup = BeautifulSoup(r.text, features="lxml")

    cells = soup.find_all('td')
    for n, s in enumerate(cells):
        if s.text == 'Repayment date':
            repayment_date = cells[n+1].text
    repayment_date = datetime.datetime(year=int(repayment_date[-5:]), month=int(repayment_date[4:6]), day=int(repayment_date[0:3]))

    return repayment_date


def euronext_coupon(code, exchange='XPAR'):

    url = f"https://live.euronext.com/en//ajax/getFactsheetInfoBlock/BONDS/{code}-{exchange}/fs_couponinfo_block"

    payload = ""
    headers = {
        "cookie": "TS01a5de3f=01010d14938f0caadca91202f9d94a1b1e0f78dd0f5559376db633e0518cb37d43c942f008",
        "Accept": "*/*",
        "Accept-Language": "en-GB,en;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Cookie": "cookie-agreed-version=1.0.1; cookie-agreed-categories=^%^5B^%^22necessary^%^22^%^2C^%^22performance^%^22^%^5D; cookie-agreed=2; visid_incap_2691598=nzxxTqEqQAi9XFfYveHMvL0QxGIAAAAAQUIPAAAAAAD+ET0tgUt39FfN4haWMtKO; _gcl_au=1.1.635390176.1657016512; _ga=GA1.2.1300778173.1657016512; _hjSessionUser_1305322=eyJpZCI6IjQ2OTg4MWYyLWVhMWUtNTc4Ni1iMzk0LWExNTIwNjE3YzA5ZSIsImNyZWF0ZWQiOjE2NTcwMTY1MTI0MDAsImV4aXN0aW5nIjp0cnVlfQ==; incap_ses_1176_2691598=KDPQcPQWBwUb9jUYG/5REL3Fz2IAAAAA1IlJY7KMJH8UpBdBgoA2HA==; _gid=GA1.2.443853341.1657783743; _hjSession_1305322=eyJpZCI6ImEyZDY4MmQwLWMwNTItNDBlOS04NDIwLWI3NDJjZWQxYTQxOSIsImNyZWF0ZWQiOjE2NTc3ODM3NDM0OTAsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _hjShownFeedbackMessage=true; TS01a5de3f=01010d1493d771ef9e0ab21586b288f71131d01cb47caccaa0293153331c602b46c2a22597; _gat_UA-46900155-5=1; _hjIncludedInSessionSample=0",
        "Referer": "https://live.euronext.com/en/product/bonds/FR0013424876-XPAR/market-information",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": "^\^.Not/A",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "^\^Windows^^"
    }

    r = requests.get(url, data=payload, headers=headers)

    soup = BeautifulSoup(r.text, features="lxml")

    cells = soup.find_all('td')
    for n, s in enumerate(cells):
        if s.text == 'Interest Rate':
            coupon = cells[n+1].text
        if s.text == 'Interest rate frequency':
            period = cells[n+1].text
    coupon = float(coupon.replace('%', '')) / 100
    return coupon, period


def euronext_issuer(code, exchange='XPAR'):

    url = f"https://live.euronext.com/en//ajax/getFactsheetInfoBlock/BONDS/{code}-{exchange}/fs_issuerinfo_block"

    payload = ""
    headers = {
        "cookie": "TS01a5de3f=015c8de7076ee2f10286336b09e297acc6b0cb0dcc4ca8a7cc62e78f43e66259d6daff108e",
        "Accept": "*/*",
        "Accept-Language": "en-GB,en;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Cookie": "cookie-agreed-version=1.0.1; cookie-agreed-categories=^%^5B^%^22necessary^%^22^%^2C^%^22performance^%^22^%^5D; cookie-agreed=2; visid_incap_2691598=nzxxTqEqQAi9XFfYveHMvL0QxGIAAAAAQUIPAAAAAAD+ET0tgUt39FfN4haWMtKO; _gcl_au=1.1.635390176.1657016512; _ga=GA1.2.1300778173.1657016512; _hjSessionUser_1305322=eyJpZCI6IjQ2OTg4MWYyLWVhMWUtNTc4Ni1iMzk0LWExNTIwNjE3YzA5ZSIsImNyZWF0ZWQiOjE2NTcwMTY1MTI0MDAsImV4aXN0aW5nIjp0cnVlfQ==; incap_ses_1176_2691598=KDPQcPQWBwUb9jUYG/5REL3Fz2IAAAAA1IlJY7KMJH8UpBdBgoA2HA==; _gid=GA1.2.443853341.1657783743; _hjSession_1305322=eyJpZCI6ImEyZDY4MmQwLWMwNTItNDBlOS04NDIwLWI3NDJjZWQxYTQxOSIsImNyZWF0ZWQiOjE2NTc3ODM3NDM0OTAsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _hjShownFeedbackMessage=true; TS01a5de3f=01010d1493d771ef9e0ab21586b288f71131d01cb47caccaa0293153331c602b46c2a22597; _gat_UA-46900155-5=1; _hjIncludedInSessionSample=0",
        "Referer": "https://live.euronext.com/en/product/bonds/FR0013424876-XPAR/market-information",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": "^\^.Not/A",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "^\^Windows^^"
    }

    r = requests.get(url, data=payload, headers=headers)

    soup = BeautifulSoup(r.text, features="lxml")

    issuer = soup.select('body > div > div.card-body > p:nth-child(1) > strong')
    issuer = issuer[0].text

    return issuer


def euronext_price(code, exchange='XPAR'):

    url = f"https://live.euronext.com/en/ajax/getDetailedQuote/{code}-{exchange}"

    payload = "theme_name=euronext_live"
    headers = {
        "cookie": "TS01a5de3f=015c8de707bdbc45e6b2ef5b1f95fb368b5d4c12adf0301103eb6a5d6f153f151a16b60aab",
        "Accept": "*/*",
        "Accept-Language": "en-GB,en;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "cookie-agreed-version=1.0.1; cookie-agreed-categories=^%^5B^%^22necessary^%^22^%^2C^%^22performance^%^22^%^5D; cookie-agreed=2; visid_incap_2691598=nzxxTqEqQAi9XFfYveHMvL0QxGIAAAAAQUIPAAAAAAD+ET0tgUt39FfN4haWMtKO; _gcl_au=1.1.635390176.1657016512; _ga=GA1.2.1300778173.1657016512; _hjSessionUser_1305322=eyJpZCI6IjQ2OTg4MWYyLWVhMWUtNTc4Ni1iMzk0LWExNTIwNjE3YzA5ZSIsImNyZWF0ZWQiOjE2NTcwMTY1MTI0MDAsImV4aXN0aW5nIjp0cnVlfQ==; incap_ses_1176_2691598=KDPQcPQWBwUb9jUYG/5REL3Fz2IAAAAA1IlJY7KMJH8UpBdBgoA2HA==; _gid=GA1.2.443853341.1657783743; _hjIncludedInSessionSample=0; _hjSession_1305322=eyJpZCI6ImEyZDY4MmQwLWMwNTItNDBlOS04NDIwLWI3NDJjZWQxYTQxOSIsImNyZWF0ZWQiOjE2NTc3ODM3NDM0OTAsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _hjShownFeedbackMessage=true; TS01a5de3f=01010d14930a63e20276e93d3d98eb5a1f59a3d6442a09e480f3b8f6d3d2447922ba9138df",
        "Origin": "https://live.euronext.com",
        "Referer": "https://live.euronext.com/en/product/bonds/FR0013424876-XPAR/market-information",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": "^\^.Not/A",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "^\^Windows^^"
    }

    r = requests.post(url, data=payload, headers=headers)

    soup = BeautifulSoup(r.text, features="lxml")
    price_span = soup.select('body > div > div > div.data-header > div > div.data-header__col.data-header__col-right.bg-white > div > h5:nth-child(1) > span:nth-child(2)')
    price = float(price_span[0].text)

    bond_id = soup.select('#header-instrument-name > strong')
    bond_id = bond_id[0].text

    return bond_id, price

def calc_ytm(price, coupon, term, period, face_value=100):

    if period == 'Annual':
        ytm = coupon * 100 / price + (100 / price)**(1/term) - 1 

    if period == 'Quarterly':
        q_coupon = coupon * 100 / 4
        ytm = (1 + q_coupon / price)**3 - 1 + q_coupon / price + (100 / price)**(1/term) - 1 

    return ytm

def composite(tickers):
    df = pd.DataFrame(columns=['bond_id', 'issuer', 'coupon', 'repayment_date', 'term', 'price', 'ytm', 'rf', 'spread', 'ten_yr_equiv'])
    for ticker in tickers:
        print('Processing: ', ticker)
        if ticker[:2] == 'FR':
            country = 'france'
        if ticker[:2] == 'DE':
            country = 'germany'
        issuer = euronext_issuer(ticker)
        bond_id, price = euronext_price(ticker)
        coupon, period = euronext_coupon(ticker)
        repayment_date = euronext_repay_date(ticker)
        term = (repayment_date - datetime.datetime.now()) / datetime.timedelta(days=365)
        ytm = calc_ytm(price, coupon, term, period, face_value=100)
        rf = get_rf(term * 12, country) / 100
        spread = ytm - rf
        ten_yr_equiv = (get_rf(120, country) / 100 ) + spread
        df.loc[ticker] = bond_id, issuer, coupon, repayment_date, term, price, ytm, rf, spread, ten_yr_equiv
    df.loc['Average'] = df.mean(axis=0)
    df.to_excel('bond_composite.xlsx')
    ten_yr_composite = df.iloc[-1, -1]
    spread = df.iloc[-1, -2]

    return df, ten_yr_composite, spread

if __name__ == "__main__":

    tickers = ['FR0013424876', 'FR0013505260', 'FR0014006ZC4', 'FR0014000D31', 'FR0014004FR9']

    # print(euronext_price('FR0013424876'))
    # print(euronext_info('FR0013424876'))
    # print(euronext_repay_date('FR0013424876'))
    # print(euronext_coupon('FR0013424876'))
    # print(euronext_issuer('FR0013424876'))

    print(composite(tickers))
    