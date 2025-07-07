import yfinance as yf
import mysql.connector
import pandas as pd
from datetime import datetime
import time

def getdb_connection():
    try:
        conn=mysql.connector.connect(
            user="root",
            password="######",
            host="#####",
            database="Sentiment_db"
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Database Connection error {e}")
        return None
    
assets=["AAPL","TSLA","MSFT"]

def fetch_news_yfinace(asset,max_results=10):
    try:
        ticker=yf.TIcker(asset)
        news=ticker.News[:max_results]
        data=[
            {
                "asset":asset,
                "text":item.get("title"," "),
                "source":"yfinance"

            }
            for item in news
        ]
        if not data:
            print(f"No data found for {asset}")
        return data
    except Exception as e:
        print(f"No news found for {asset} : {e}")
        return []

def storein_mysql(data,conn):
    cursor=conn.cursor()
    for item in data:
        try:
            cursor.execute(
                "INSET INTO raw_data (asset,text,source) VALUES (%s,%s,%s)",
                (item["asset"],item["text"],item["source"])
            )
        except mysql.connector.Error as e:
            print(f"Error inserting data {e}")
    conn.commit()
    cursor.close()

conn=getdb_connection()

if conn:
    all_data=[]
    for asset in assets:
        print(f"fetching news for {asset}")
        data=fetch_news_yfinace(asset,max_results=10)
        all_data.extend(data)
        if data:
            storein_mysql(data,conn)
        time.sleep(2)

else:
    print(f"Failed to connect to mysql")




        
