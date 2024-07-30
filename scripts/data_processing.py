import fingertips_py as ftp
import pandas as pd
import re
import os
import warnings
from tqdm import tqdm

def clean_data_source(source):
    """
    Remove URLs and other unwanted characters from the data source string.
    
    Parameters:
    source (str): The data source string to clean.
    
    Returns:
    str: The cleaned data source string.
    """
    source = re.sub(r'<[^>]+>', '', source or "Unknown Source")
    source = source.strip().split('\n')[0].split('. ')[0]
    return (source[:125] + '...') if len(source) > 125 else source

def clean_indicator_name(name):
    """
    Clean the indicator name by removing illegal characters and formatting, used for cleaning file names.
    
    Parameters:
    name (str): The indicator name to clean.
    
    Returns:
    str: The cleaned indicator name.
    """
    name = ' '.join(name.split())
    name = name.replace('%', 'percent')
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    return name

def download_and_process_data(indicator_ids, area_type_id, indicators, combine=False, keep_latest=False, delete_empty_columns=False):
    """
    Download and process data for given indicator IDs and area type ID.
    
    Parameters:
    indicator_ids (list): List of indicator IDs to download data for.
    area_type_id (int): Area type ID to filter data.
    indicators (list): List of indicator metadata.
    combine (bool): Whether to combine all data into a single file. Default is False.
    keep_latest (bool): Whether to keep only the latest data. Default is False.
    delete_empty_columns (bool): Whether to delete columns that contain all NaN or Null values. Default is False.
    """
    data_frames = []
    for indicator_id in tqdm(indicator_ids, desc="Downloading indicators"):
        indicator_name = next((ind['Name'] for ind in indicators if ind['IndicatorId'] == indicator_id), None)
        print(f"\nFetching data for Indicator ID: {indicator_id}, Indicator Name: {indicator_name}")

        # Suppress warnings for fingertips_py to avoid dtype mismatch clutter
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                data = ftp.retrieve_data.get_data_by_indicator_ids(indicator_id, area_type_id, parent_area_type_id=None, profile_id=None, include_sortable_time_periods=True, is_test=False)
            except Exception as e:
                print(f"Error fetching data for Indicator ID {indicator_id}: {e}")
                continue

        df = pd.DataFrame(data)

        if df.empty:
            print(f"No data found for Indicator ID {indicator_id} ({indicator_name})")
        else:
            if keep_latest:
                df = df[df['Time period Sortable'] == df['Time period Sortable'].max()]
                print(f"Keeping latest data for '{indicator_name}', period: {df['Time period'].iloc[0]}")

            if not combine and delete_empty_columns:
                before_cols = df.columns.tolist()
                df.dropna(axis=1, how='all', inplace=True)
                after_cols = df.columns.tolist()
                deleted_cols = list(set(before_cols) - set(after_cols))
                if deleted_cols:
                    print(f"Deleted {len(deleted_cols)} columns in {indicator_name} (ID: {indicator_id}): {', '.join(deleted_cols)}")

            if not combine:
                filename = f"data/processed/{clean_indicator_name(indicator_name).replace(' ', '_')}_{indicator_id}_area_{area_type_id}.csv"
                try:
                    df.to_csv(filename, index=False)
                    print(f"Data saved to {filename}")
                except Exception as e:
                    print(f"Error saving data to {filename}: {e}")
            data_frames.append(df)
    
    if combine and data_frames:
        print("Combining dataframes...")
        combined_df = pd.concat(data_frames, ignore_index=True)

        if delete_empty_columns:
            before_cols = combined_df.columns.tolist()
            combined_df.dropna(axis=1, how='all', inplace=True)
            after_cols = combined_df.columns.tolist()
            deleted_cols = list(set(before_cols) - set(after_cols))
            if deleted_cols:
                print(f"Deleted {len(deleted_cols)} columns in combined data: {', '.join(deleted_cols)}")

        combined_filename = 'data/processed/combined_fingertips_data.csv'
        try:
            combined_df.to_csv(combined_filename, index=False)
            print(f"Combined data saved to {combined_filename}")
        except Exception as e:
            print(f"Error saving combined data to {combined_filename}: {e}")
