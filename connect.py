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

print(sql1)

mycursor.execute(sql1)

sql2 = "CREATE TABLE IF NOT EXISTS price_info (ID int AUTO_INCREMENT PRIMARY KEY, Ticker VARCHAR(255), Company VARCHAR(255), first_close FLOAT(4), last_close FLOAT(4), dec_percent FLOAT(4));"

print(sql2)

mycursor.execute(sql2)
