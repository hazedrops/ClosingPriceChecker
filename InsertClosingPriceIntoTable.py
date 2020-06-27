import pandas as pd
from pandas_datareader import data as pdr
from datetime import date, datetime, timedelta
import yfinance as yf
import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pickle
import requests
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="itjeans2000",
    database="stockdb"
)

mycursor = mydb.cursor()

my_url = 'http://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

# Opening up connection, grabbing the page
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# HTML parsing
page_soup = soup(page_html, "html.parser")

# Grab the s&p 500 table & table rows
sp_table = page_soup.find("table", attrs={"class": "wikitable"})

tickers = []

for row in sp_table.findAll('tr')[1:]:
    name = row.findAll('td')[0].a.text
    tickers.append(name)

for ticker in tickers:
    symbol = yf.Ticker(ticker)

    close_price = pd.to_numeric(symbol.history(
        period="5d").Close.array)

    for price in close_price:
        sql = "INSERT INTO closing_info (Ticker, close) VALUES (%s, %s)"
        val = (ticker, float(price))
        mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")
