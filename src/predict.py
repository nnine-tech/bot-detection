import pickle
import pandas as pd
from src.database import features_collection, predictions_collection

async def predict_and_save():
    # Load model
    with open("rf_model.pkl", "rb") as f:
        model = pickle.load(f)

    # Fetch all features
    cursor = features_collection.find({})
    features = await cursor.to_list(length=None)
    print("📊 Features fetched:", len(features))

    records_to_insert = []
    for feature in features:
        # Prepare ML input
        X = {k: v for k, v in feature.items()
             if k not in ['_id','ip','timestamp','method','endpoint','referrer','user_agent']}
        if not X:  # Skip if no usable features
            continue

        X_df = pd.DataFrame([X])
        ml_pred = model.predict(X_df)[0]
        final_pred = 1 if ml_pred > 0 else 0
        alert_msg = "Possible bot" if final_pred else None

        # Ensure timestamp is serializable
        ts = feature.get("timestamp")
        if ts is not None:
            ts = pd.to_datetime(ts).to_pydatetime()

        records_to_insert.append({
            "ip": feature.get("ip"),
            "timestamp": ts,
            "endpoint": feature.get("endpoint"),
            "ml_pred": int(ml_pred),
            "final_prediction": final_pred,
            "alert": alert_msg
        })

    print("📝 Prepared records:", len(records_to_insert))

    if records_to_insert:
        try:
            result = await predictions_collection.insert_many(records_to_insert, ordered=False)
            print(f"✅ Inserted {len(result.inserted_ids)} predictions")
            count = await predictions_collection.count_documents({})
            print("📦 Predictions collection count:", count)
        except Exception as e:
            import traceback
            print("❌ Error inserting predictions:", e)
            traceback.print_exc()
    else:
        print("⚠️ No records prepared for insertion")
