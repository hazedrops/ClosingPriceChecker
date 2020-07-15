import pandas as pd
from pandas_datareader import data as pdr
from datetime import date, datetime, timedelta
import yfinance as yf
import bs4
from urllib.request import urlopen as uReq
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup as soup
# import pickle
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="itjeans2000",
    database="stockdb"
)

mycursor = mydb.cursor()

response = requests.get(
    'https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average')

first_price = 0
saved_price = 0

if response.status_code == 200:
    print('Web site exists')
else:
    print('Web site does not exist')

page_html = response.content
# print(page_html)

page_soup = soup(page_html, "html.parser")
# print(page_soup)

# Grab the Nasdaq 100 table & table rows
rows = page_soup.find(
    'table', id="constituents").find('tbody').findAll('tr')[1:]


# # print(nasdaq_table)
# print(rows)

# # Company class


class companies:
    def __init__(self, ticker, company):
        self.ticker = ticker
        self.company = company


# creating list
company_list = []

for row in rows:

    c_name = row.findAll('td')[:1][0].text.strip()
    c_tkrstr = row.findAll('td')[1:][1].text.strip()

    s_str = 'NYSE:'

    # print("initial_strings : ", c_tkrstr, "\nsubstring : ", s_str)

    # print(c_tkrstr.startswith(s_str))
    if c_tkrstr.startswith(s_str):
        c_tkr = c_tkrstr.replace(s_str, '').strip()
    else:
        c_tkr = c_tkrstr.strip()

    print(c_name)
    print(c_tkr)

    company_list.append(companies(c_tkr, c_name))

length = len(company_list)

for i in range(length):
    print(company_list[i].ticker + " : " + company_list[i].company)

    symbol = yf.Ticker(company_list[i].ticker)

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
        per_drop = (first_price - price) / first_price * 100

        sql = "INSERT INTO dow_price_info (Ticker, Company, first_close, last_close, dec_percent ) VALUES (%s, %s, %s, %s, %s)"
        val = (company_list[i].ticker, company_list[i].company,
               float(first_price), float(price), float(per_drop))
        mycursor.execute(sql, val)

        mydb.commit()

if mycursor.rowcount == -1:
    print("0 record inserted!")
