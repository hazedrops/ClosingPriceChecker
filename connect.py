import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="itjeans2000",
    database="stockdb",
)

mycursor = mydb.cursor()

# sql = """CREATE TABLE IF NOT EXISTS closing_info (ID int AUTO_INCREMENT PRIMARY KEY, Ticker VARCHAR(255), close FLOAT(4))"""
sql = """CREATE TABLE IF NOT EXISTS price_info (ID int AUTO_INCREMENT PRIMARY KEY, Ticker VARCHAR(255), first_close FLOAT(4), last_close FLOAT(4))"""

print(sql)

mycursor.execute(sql)
