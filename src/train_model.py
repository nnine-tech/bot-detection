import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from src.database import features_collection
import asyncio

def label_bot(row):
    if row['status'] >= 400 and row['ua_has_bot_like_keyword'] == 1 and row['referrer_is_missing'] == 1:
        return 2
    elif row['status'] >= 400 or row['ua_has_bot_like_keyword'] == 1 or row['referrer_is_missing'] == 1:
        return 1
    else:
        return 0

async def train_and_save_model():
    cursor = features_collection.find({})
    df = pd.DataFrame([doc async for doc in cursor])
    if df.empty:
        print(" No data to train model")
        return None

    df['is_malicious_ip'] = df.apply(label_bot, axis=1)

    X = df.drop(columns=['_id','ip','timestamp','method','endpoint','referrer','user_agent','is_malicious_ip'], errors='ignore')

    y = df['is_malicious_ip']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(" Classification Report:\n", classification_report(y_test, y_pred))

    with open("rf_model.pkl", "wb") as f:
        pickle.dump(model, f)
    print(" Model saved as rf_model.pkl")
    return model
