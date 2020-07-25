import pandas as pd
from pandas_datareader import data as pdr
import numpy as np
from datetime import date, datetime, timedelta
import yfinance as yf
from yahoo_finance import Share as sr
import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import requests
import mysql.connector
import csv

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="itjeans2000",
    database="stockdb"
)

mycursor = mydb.cursor()

first_price = 0
saved_price = 0

# Company class


class companies:
    def __init__(self, ticker, company):
        self.ticker = ticker
        self.company = company


# creating list
company_list = []

with open('companylist.csv', 'r') as csvfile:

    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV)

    for col in readCSV:
        tk = col[0]
        c_name = col[1]
        company_list.append(companies(tk, c_name))

length = len(company_list)

for i in range(length):

    symbol = yf.Ticker(company_list[i].ticker)

    print("TICKER: " + company_list[i].ticker)
    try:
        mc = pdr.get_quote_yahoo(company_list[i].ticker)['marketCap']
        mCap = mc.array[0]

        av = pdr.get_quote_yahoo(company_list[i].ticker)[
            'averageDailyVolume3Month']
        aVol = av.array[0]
        print(aVol)

        # If there's no data found, skip to the next iteration
        if symbol.history(period="8d").empty:
            continue

        close_price = pd.to_numeric(symbol.history(
            period="8d").Close.array)

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
                first_price = price

        if day_count >= 4:

            print(day_count)

            per_drop = (first_price - price) / first_price * 100

            if per_drop >= 3:
                print(per_drop)
                sql = "INSERT INTO price_info (Ticker, Company, first_close, last_close, dec_percent, days, market_cap, average_vol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                val = (company_list[i].ticker, company_list[i].company,
                       float(first_price), float(price), float(per_drop), int(day_count), int(mCap), int(aVol))
                mycursor.execute(sql, val)

                print(mydb.commit())

    except:
        pass

if mycursor.rowcount == -1:
    print("0 record inserted!")
