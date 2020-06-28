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


first_price = 0
saved_price = 0

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

    # If there's no data found, skip to the next iteration
    if symbol.history(period="5d").empty:
        continue

    close_price = pd.to_numeric(symbol.history(
        period="5d").Close.array)

    day_count = 0
    first_price = close_price[0]
    lowest_price = first_price

    for index, price in enumerate(close_price, start=0):
        print(index, price)

        # If price of the next day dropped, then increse the count by 1, and save the price as the lowest price
        if lowest_price >= price:
            day_count += 1
            lowest_price = price

        # else start count from 0 again, and save the lowest_price as the day's price!!!
        else:
            day_count = 0
            lowest_price = price

        if day_count == 5:
            # print("The price dropped for 5 days!!!")
            # print(ticker)
            # print("lowest_price is " + str(lowest_price))
            # print("day_count is " + str(day_count))

            sql = "INSERT INTO price_info (Ticker, first_close, last_close) VALUES (%s, %s, %s)"
            val = (ticker, float(first_price), float(price))
            mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")
