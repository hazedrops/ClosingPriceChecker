import pandas as pd
from pandas_datareader import data as pdr
import numpy as np
from datetime import date, datetime, timedelta
import yfinance as yf
from yahoo_finance import Share as sr
import csv
import smtplib

# import the corresponding modules
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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

t_date = datetime.now().strftime("%m_%d_%Y")
f_name = t_date + '_price_info.csv'

length = len(company_list)

with open(f_name, 'w', newline='') as csvfile:
    fieldnames = ['Ticker', 'Company', 'First_Close', 'Last_Close', 'Dec_Percent', 'Days_Dropped', 'Market_Cap', 'Aaverage_Vol', 'epsForward', 'sharesOutstanding',
                  'trailingPE', 'priceToBook', 'bookValue', 'trailingAnnualDividendYield', '52WkLowChangePercent', '52WkHighChangePercent']

    writer = csv.DictWriter(
        csvfile, fieldnames=fieldnames, extrasaction='raise')

    writer.writeheader()

    for i in range(length):
        tkr = company_list[i].ticker
        comp = company_list[i].company

        symbol = yf.Ticker(tkr)

        print("TICKER: " + tkr)
        try:
            mc = pdr.get_quote_yahoo(tkr)['marketCap']
            mCap = mc.array[0]

            av = pdr.get_quote_yahoo(tkr)[
                'averageDailyVolume3Month']
            aVol = av.array[0]

            ef = pdr.get_quote_yahoo(tkr)['epsForward']
            epsF = ef.array[0]

            so = pdr.get_quote_yahoo(tkr)['sharesOutstanding']
            sOut = so.array[0]

            tp = pdr.get_quote_yahoo(tkr)['trailingPE']
            tPE = tp.array[0]

            ptb = pdr.get_quote_yahoo(tkr)['priceToBook']
            pTB = ptb.array[0]

            bv = pdr.get_quote_yahoo(tkr)['bookValue']
            bVal = bv.array[0]

            tady = pdr.get_quote_yahoo(tkr)['trailingAnnualDividendYield']
            tADY = tady.array[0]

            ftwl = pdr.get_quote_yahoo(tkr)['fiftyTwoWeekLowChangePercent']
            ftwLow = ftwl.array[0]

            ftwh = pdr.get_quote_yahoo(tkr)['fiftyTwoWeekHighChangePercent']
            ftwHigh = ftwh.array[0]

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
                print(per_drop)

                if per_drop >= 3:
                    writer.writerow({'Ticker': tkr, 'Company': comp, 'First_Close': first_price, 'Last_Close': price, 'Dec_Percent': per_drop, 'Days_Dropped': day_count, 'Market_Cap': mCap, 'Aaverage_Vol': aVol, 'epsForward': epsF,
                                     'sharesOutstanding': sOut, 'trailingPE': tPE, 'priceToBook': pTB, 'bookValue': bVal, 'trailingAnnualDividendYield': tADY, '52WkLowChangePercent': ftwLow, '52WkHighChangePercent': ftwHigh})

        except:
            pass


def send_email(fname):
    smtp_server = 'smtp.live.com'
    port = 587
    sender = 'MY_EMAIL'

    receiver = 'RECEIVER_EMAIL'

    password = 'MY_PASSWORD'

    file_name = fname
    message = MIMEMultipart('alternative')
    message['Subject'] = 'Todays Price Info File'
    message['From'] = sender
    message['To'] = receiver
    print(message.attach(MIMEText('Sending an attachment', 'plain')))

    with open(file_name, 'rb') as attachment:
        file_part = MIMEBase('application', 'octet-stream')
        file_part.set_payload(attachment.read())

        encoders.encode_base64(file_part)
        file_part.add_header(
            'Content-Disposition',

            'attachment; filename=' + str(file_name)
        )

        message.attach(file_part)

        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()
        server.starttls()  # Secure the connection
        server.ehlo()

        server.login(sender, password)

        server.sendmail(sender, receiver, message.as_string())

    print('Hey Email Has Been Sent!')

    server.quit()


send_email(f_name)
