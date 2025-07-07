import mysql.connector
import pandas as pd
import yfinance as yf
import numpy as np
import joblib
from datetime import datetime
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def getdb_connection():
    try:
        conn=mysql.connector.connect(
            user="root",
            password="Pranav1501$",
            host="",
            database="Sentiment_db"
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Database connection error {e}")
        return None

def scores_table(conn):

    cursor=conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INT AUTO_INCREMENT PRIMARY KEY,
            asset VARCHAR(100) NOT NULL,
            score FLOAT NOT NULL,
            prediction INT NOT NULL,
            created_at VARCHAR(50) NOT NULL
        )
    """)

    conn.commit()
    cursor.close()
    print("Created scores table")

def fetch_embeddings(conn):

    query = "SELECT id, asset, embedding FROM embeddings"
    try:
        df=pd.read_sql(query,conn)

        df['embedding']=df['embedding'].apply(lambda x: np.fromstring(x.strip('[]'),sep=','))
        return df
    except Exception as e:
        print(f"Error fetching embeddings {e}")
        return pd.DataFrame()
    
def fetch_price(assets,period="5d"):
    labels={}
    for asset in assets:
        try:
            ticker=yf.Ticker(asset)
            prices=ticker.history(period=period)["Close"]

            labels[asset]=(prices.pct_change().shift(-1)>0).astype(int).values[-len(prices):]
        except Exception as e:
            print(f"Error fetching prices {e}")
            labels[asset]=[]
    return labels

def aggregate_embeddings(df):

    df_agg=df.groupby("asset")['embedding'].apply(lambda x : np.mean(np.stack(x),axis=0)).reset.index()

def train_classifier(X,y,test_size=0.2):
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=test_size,random_state=42)
    model=LogisticRegression(max_iter=1000)
    model.fit(X_train,y_train)
    y_pred=model.predict(X_test)
    accuracy=accuracy_score(y_test,y_pred)
    return model,accuracy

def store_scores(conn,df_agg,scores,predictions):
    cursor=conn.cursor()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for i, (asset, score, pred) in enumerate(zip(df_agg['asset'], scores, predictions)):
        try:
            cursor.execute(
                "INSERT INTO scores (asset, score, prediction, created_at) VALUES (%s, %s, %s, %s)",
                (asset, float(score), int(pred), current_time)
            )
        except mysql.connector.Error as e:
            print(f"Error storing scores {e}")
    
    conn.commit()
    cursor.close()

    print(f"Stored {len(df_agg)} scores in MySQL.")

def main():
    conn=getdb_connection()
    if not conn:
        return
    
    scores_table(conn)

    df=fetch_embeddings(conn)
    if df.empty:
        print("No embeddings found")
        conn.close()
        return
    
    df_agg=aggregate_embeddings(df)
    assets=df_agg['asset'].tolist()

    labels_dict=fetch_price(assets,period='5d')
    valid_assets = [asset for asset in assets if len(labels_dict[asset]) > 0]
    if not valid_assets:
        print("No valid data found")
        conn.close()
        return
    
    X=np.stack(df_agg[df_agg['asset'].isin(valid_assets)]['embedding'])
    y = np.array([labels_dict[asset][-1] for asset in valid_assets])
    if len(X)<2:
        print("Insufficient data for training")
        conn.close()
        return
    
    model,accuracy=train_classifier(X,y)
    print(f"Accuracy : {accuracy : 2%}")


    joblib.dump(model,"classifier_model.pkl")
    print("Saved model")

    scores=model.predict_proba(X)[:,1]
    predictions=model.predict(X)
    store_scores(conn, df_agg[df_agg['asset'].isin(valid_assets)], scores, predictions)

if __name__ == "__main__":
    main()








