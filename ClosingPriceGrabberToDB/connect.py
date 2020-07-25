import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="itjeans2000",
    database="stockdb",
)

mycursor = mydb.cursor()

# sql = """CREATE TABLE IF NOT EXISTS closing_info (ID int AUTO_INCREMENT PRIMARY KEY, Ticker VARCHAR(255), close FLOAT(4))"""
sql1 = "DROP TABLE price_info;"
# sql2 = "DROP TABLE nasdaq_price_info;"
# sql3 = "DROP TABLE dow_price_info;"

# print(sql1)

# mycursor.execute(sql1)

sql2 = "CREATE TABLE IF NOT EXISTS price_info(ID int AUTO_INCREMENT PRIMARY KEY, Ticker VARCHAR(255), Company VARCHAR(255), first_close FLOAT(4), last_close FLOAT(4), dec_percent FLOAT(4), days INT(3), market_cap INT(8), average_vol INT(8));"
# );"
# sql4 = "CREATE TABLE IF NOT EXISTS nasdaq_price_info (ID int AUTO_INCREMENT PRIMARY KEY, Ticker VARCHAR(255), Company VARCHAR(255), first_close FLOAT(4), last_close FLOAT(4), dec_percent FLOAT(4));"
# sql6 = "CREATE TABLE IF NOT EXISTS dow_price_info (ID int AUTO_INCREMENT PRIMARY KEY, Ticker VARCHAR(255), Company VARCHAR(255), first_close FLOAT(4), last_close FLOAT(4), dec_percent FLOAT(4));"

queries = [sql1, sql2]
# print(sql2)

for query in queries:
    mycursor.execute(query)
    print(query)
