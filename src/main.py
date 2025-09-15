import os
import pandas as pd
import asyncio
from src.extractor import extract_and_save_features
from src.train_model import train_and_save_model
from src.predict import predict_and_save
from src.log_parser import parse_log_file

LOG_FILES = [
    os.path.join("data", "access.log"),
    os.path.join("data", "access.log.1"),
]

async def main():
    print("🔹 Parsing logs...")
    parsed_dfs = [parse_log_file(f) for f in LOG_FILES if os.path.exists(f)]
    if not parsed_dfs:
        print(" No log files found")
        return

    combined_df = pd.concat(parsed_dfs, ignore_index=True)
    print(f" {len(combined_df)} rows parsed from logs")

    # Extract features & save to MongoDB
    print(" Extracting features...")
    await extract_and_save_features(combined_df)

    # Train model
    print(" Training model...")
    model = await train_and_save_model()
    if model:
        # Predict & save results
        print(" Predicting and saving results...")
        await predict_and_save()

    print(" Bot detection pipeline completed!")

if __name__ == "__main__":
    asyncio.run(main())
