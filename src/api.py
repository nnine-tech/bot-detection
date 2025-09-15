from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import pandas as pd
import io
from .database import predictions_collection

app = FastAPI()

# Fetch predictions from MongoDB
async def fetch_predictions():
    cursor = predictions_collection.find({"final_prediction": 1})
    results = []
    async for record in cursor:
        record["_id"] = str(record["_id"])  # Convert ObjectId to string
        results.append(record)
    return results

@app.get("/bot-detections/csv")
async def get_bot_detections_csv():
    data = await fetch_predictions()
    df = pd.DataFrame(data)

    # ✅ Group by IP and collect endpoints + timestamps
    df_grouped = df.groupby("ip").agg({
        "timestamp": ["min", "max"],
        "endpoint": lambda x: ";".join(set(x)),  # merge unique endpoints
        "alert": "first"
    }).reset_index()

    # Flatten multi-level column names
    df_grouped.columns = ["ip", "first_seen", "last_seen", "endpoints", "alert"]

    # Convert DataFrame to CSV stream
    stream = io.StringIO()
    df_grouped.to_csv(stream, index=False)
    stream.seek(0)

    return StreamingResponse(
        stream,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=bot_detections.csv"}
    )
