import pandas as pd
from pandas_datareader import data
from datetime import date, datetime, timedelta
import yfinance as yf
import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pickle
import requests

my_url = 'http://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

# Opening up connection, grabbing the page
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# HTML parsing
page_soup = soup(page_html, "html.parser")

# Grab the s&p 500 table & table rows
sp_table = page_soup.find("table", attrs={"class": "wikitable"})
# sp_table_data = sp_table.tbody.find_all("tr")

tickers = []

for row in sp_table.findAll('tr')[1:]:
    name = row.findAll('td')[0].a.text
    #print("Name: " + name)
    tickers.append(name)

print(tickers)

for ticker in tickers:
    symbol = yf.Ticker(ticker)
    close_price = pd.to_numeric(symbol.history(period="5d").Close.array)
    # print(symbol.history(period="5d").Close.array)

    # Print close prices for the last 5 days of the each sp500 tickers
    for price in close_price:
        print("Ticker: " + ticker + " Close Price: " + str(price))
