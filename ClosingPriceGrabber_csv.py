import pandas as pd
from pandas_datareader import data as pdr
from datetime import date, datetime, timedelta
import yfinance as yf
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
        # print(tk + " + " + c_name)
        company_list.append(companies(tk, c_name))

length = len(company_list)

# # Get the date of 100 day ago
# p = datetime.today() - timedelta(days=100)

for i in range(length):
    print(company_list[i].ticker + " : " + company_list[i].company)

    symbol = yf.Ticker(company_list[i].ticker)

    # past_price = pd.to_numeric(symbol.history(
    #     period='1d', start=p, end=p)['Close'].Close_price)

    # print(past_price)

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
            first_price = price
            lowest_price = price

    if day_count >= 4:
        # print("The price dropped for 5 days!!!")
        # print(ticker)
        # print("lowest_price is " + str(lowest_price))
        # print("day_count is " + str(day_count))
        print(day_count)

        per_drop = (first_price - price) / first_price * 100

        if per_drop >= 3:
            sql = "INSERT INTO price_info (Ticker, Company, first_close, last_close, dec_percent, days) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (company_list[i].ticker, company_list[i].company,
                   float(first_price), float(price), float(per_drop), int(day_count))
            mycursor.execute(sql, val)

            mydb.commit()

if mycursor.rowcount == -1:
    print("0 record inserted!")
