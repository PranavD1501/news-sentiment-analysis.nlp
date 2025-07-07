import mysql.connector
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from datetime import datetime


def getdb_connection():
    try:
        conn=mysql.connector.connect(
            user="root",
            password="Pranav1501$",
            host="localhost",
            database="Sentiment_db"

        )
        return conn
    except mysql.connector.Error as e:
        print(f"Database connection error {e}")
        return None

def create_embeddings(conn):

    cursor=conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS embeddings (
            id INT PRIMARY KEY,
            asset VARCHAR(100) NOT NULL,
            embedding TEXT NOT NULL,
            created_at VARCHAR(50) NOT NULL
        )
    """)

    conn.commit()
    cursor.close()
    print("Created embeddings table")

def fetch_data(conn):

    query = "SELECT id, asset, text FROM raw_data"
    try:
        df=pd.read_sql(query,conn)
        return df
    except Exception as e:
        print(f"Error fetching data {e}")
        return pd.DataFrame()

def generate_embeddings(texts):
    try:
        model=SentenceTransformer('all-MiniLM-L6-v2')
        embeddings=model.encode(texts,show_progreess_bar=True)
        return embeddings
    except Exception as e:
        print(f"Error generating embeddings {e}")
        return None
    
def store_embeddings(conn,df,embeddings):
    cursor=conn.cursor()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for i,(index,row) in enumerate(df.iterrows()):
        try:
            embedding_str=np.array2string(embeddings[i],separator=',',max_line_width=10000)
            cursor.execute(
                "INSERT INTO embeddings (id, asset, embedding, created_at) VALUES (%s, %s, %s, %s)",
                (row['id'], row['asset'], embedding_str, current_time)
            )
        except Exception as e:
            print(f"Error while storing {e}")
    
    conn.commit()
    cursor.close()
    print("Stored embeddings in MySQL")

def main():
    conn=getdb_connection
    if not conn:
        return
    
    create_embeddings(conn)

    df=fetch_data(conn)
    if df.empty:
        print("No data found in raw table")
        conn.close()
        return
    
    texts=df['text'].tolist()
    embeddings=generate_embeddings(texts)
    if embeddings is None:
        print("Failed to generate embeddings")
        conn.close()
        return
    
    store_embeddings(conn,df,embeddings)
    
if __name__=="__main__":
    main()









    

                

    
