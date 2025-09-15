import pandas as pd
from src.database import features_collection
import asyncio

async def extract_and_save_features(parsed_df):
    if parsed_df.empty:
        print(" No new logs to process")
        return

    rows = []
    for _, entry in parsed_df.iterrows():
        rows.append({
            "ip": entry["ip"],
            "timestamp": entry["time"],
            "method": entry["method"],
            "endpoint": entry["url"],
            "status": int(entry["status"]),
            "bytes_sent": int(entry.get("size", 0)),
            "referrer": entry.get("referrer", "-"),
            "user_agent": entry.get("user_agent", "-"),
        })

    df = pd.DataFrame(rows)

    # Convert timestamp to timezone-aware datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d/%b/%Y:%H:%M:%S %z', errors='coerce')
    df = df.dropna(subset=['timestamp'])

    # Feature engineering
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['is_night'] = ((df['hour'] < 6) | (df['hour'] > 22)).astype(int)
    df['is_api_call'] = df['endpoint'].str.contains('/api/', case=False, na=False).astype(int)
    df['is_admin_call'] = df['endpoint'].str.contains('/admin/', case=False, na=False).astype(int)
    df['endpoint_length'] = df['endpoint'].str.len()
    df['is_error'] = df['status'].apply(lambda x: 1 if x >= 400 else 0)
    df['is_success'] = df['status'].apply(lambda x: 1 if 200 <= x < 300 else 0)
    df['is_redirect'] = df['status'].apply(lambda x: 1 if 300 <= x < 400 else 0)
    df['ua_length'] = df['user_agent'].str.len()
    df['ua_is_missing'] = (df['user_agent'] == '-').astype(int)
    bot_keywords = ['bot','crawler','spider','scraper','curl','python','java','wget','httpclient','go-http','ruby']
    df['ua_has_bot_like_keyword'] = df['user_agent'].str.contains('|'.join(bot_keywords), case=False, na=False).astype(int)
    browser_keywords = ['mozilla','chrome','safari','firefox','edge','webkit']
    df['ua_has_browser_keyword'] = df['user_agent'].str.contains('|'.join(browser_keywords), case=False, na=False).astype(int)
    df['referrer_is_missing'] = (df['referrer'] == '-').astype(int)
    df['referrer_is_internal'] = (~df['referrer'].str.contains('http', case=False, na=False) & (df['referrer'] != '-')).astype(int)

    # Prepare records for insertion
    records = df.to_dict("records")
    if records:
        for feature in records:
            try:
                await features_collection.update_one(
                    {"ip": feature["ip"], "timestamp": feature["timestamp"], "endpoint": feature["endpoint"]},
                    {"$setOnInsert": feature},
                    upsert=True
                )
            except Exception as e:
                print("⚠️ Error saving feature:", e)
        print(f" {len(records)} features processed and saved to MongoDB")
