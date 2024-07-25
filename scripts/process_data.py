import pandas as pd
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_and_pivot_data(data_filepath):
    # Load the raw data with all columns as strings
    logging.info(f"Loading data from {data_filepath}")
    df = pd.read_csv(data_filepath, dtype=str, low_memory=False)
    logging.info(f"Columns in the dataset: {df.columns.tolist()}")

    # Ensure 'Category' column exists and fill NaN values with an empty string
    df['Category'] = df.get('Category', '').fillna('')
    logging.info(f"Ensured 'Category' column")

    # Filter data where Area Type is 'GPs'
    logging.info("Filtering data where Area Type is 'GPs'")
    df_gps = df[df['Area Type'] == 'GPs'].copy()
    logging.info(f"Filtered data shape: {df_gps.shape}")

    # Find the max Time period for each Area Name and Indicator
    logging.info("Finding the max Time period for each Area Name and Indicator")
    df_gps['Time period'] = df_gps['Time period'].astype(str)  # Ensure 'Time period' is string for comparison
    max_periods = df_gps.groupby(['Area Name', 'Indicator Name', 'Category'])['Time period'].transform('max')
    df_latest = df_gps[df_gps['Time period'] == max_periods]
    logging.info(f"Data shape after filtering by max time period: {df_latest.shape}")

    # Manually pivot the data
    logging.info("Manually pivoting the data")
    pivoted_data = {}
    for index, row in df_latest.iterrows():
        area_code = row['Area Code']
        area_name = row['Area Name']
        indicator = row['Indicator Name']
        category = row['Category']
        time_period = row['Time period']
        value = row['Value']
        count = row.get('Count', '')
        denominator = row.get('Denominator', '')

        key = (area_code, area_name)
        if key not in pivoted_data:
            pivoted_data[key] = {}

        suffix = f"{indicator}_{category}" if category else indicator
        pivoted_data[key][f"Value_{suffix}"] = value
        pivoted_data[key][f"Time period_{suffix}"] = time_period

        # Only include Count and Denominator if they are not empty
        if count and count != '':
            pivoted_data[key][f"Count_{suffix}"] = count
        if denominator and denominator != '':
            pivoted_data[key][f"Denominator_{suffix}"] = denominator

    # Convert the pivoted data to a DataFrame
    pivoted_df = pd.DataFrame.from_dict(pivoted_data, orient='index').reset_index()
    pivoted_df.columns = ['Area Code', 'Area Name'] + list(pivoted_df.columns[2:])
    logging.info(f"Pivoted DataFrame shape: {pivoted_df.shape}")

    # Remove columns with all NaN or empty values
    pivoted_df = pivoted_df.dropna(axis=1, how='all')
    logging.info(f"Data shape after dropping empty columns: {pivoted_df.shape}")

    logging.info("Data processing complete")
    return pivoted_df

# Ensure the directory exists
os.makedirs('data/processed', exist_ok=True)

# Filepaths
data_filepath = 'data/raw/fingertips_data.csv'
output_filepath = 'data/processed/fingertips_data.csv'

# Process and pivot the collected data
processed_data = process_and_pivot_data(data_filepath)
processed_data.to_csv(output_filepath, index=False)
logging.info(f"Saved to '{output_filepath}'.")
