import requests
import pandas as pd
from io import StringIO
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# List of indicators
indicators = [1679,93553,92588,91280] # Add more indicators here, note each indicator returns about 12MB of data

def fetch_indicator_data(indicator_ids):
    url = f"https://fingertips.phe.org.uk/api/all_data/csv/by_indicator_id?indicator_ids={indicator_ids}"
    logging.info(f"Fetching data for indicators: {indicator_ids}")
    response = requests.get(url)
    if response.status_code == 200:
        logging.info(f"Successfully fetched data for indicators: {indicator_ids}")
        return response.content.decode('utf-8')
    else:
        logging.error(f"Failed to fetch data for indicators: {indicator_ids} with status code: {response.status_code}")
        return None

# Ensure the directory exists
os.makedirs('data/raw', exist_ok=True)

# Batch size for fetching data
batch_size = 5
dataframes = []

# Fetch data in batches
logging.info("Starting data fetching in batches")
for i in range(0, len(indicators), batch_size):
    batch = indicators[i:i+batch_size]
    indicator_ids = ','.join(map(str, batch))
    csv_data = fetch_indicator_data(indicator_ids)
    if csv_data:
        df = pd.read_csv(StringIO(csv_data))
        dataframes.append(df)

# Save the fetched data to a CSV file
if dataframes:
    raw_data = pd.concat(dataframes)
    raw_data.to_csv('data/raw/fingertips_data.csv', index=False)
    logging.info("Data fetching complete. Saved to 'data/raw/fingertips_data.csv'.")
else:
    logging.error("No data fetched to process.")
