import fingertips_py as ftp
import pandas as pd
import json
import os

def fetch_and_save_data():
    """
    Fetch and save initial data for indicators and areas from the API.
    
    The data is saved to the 'data/helpers' directory.
    """
    os.makedirs('data/helpers', exist_ok=True)

    try:
        # Fetch area types for all indicators
        area_data = ftp.get_all_areas_for_all_indicators()
        area_json_data = {str(indicator_id): [str(area_type_id) for area_type_id in area_types if area_type_id is not None]
                          for indicator_id, area_types in area_data.items()}

        # Fetch metadata for all indicators
        metadata = ftp.get_metadata_for_all_indicators()
        flattened_metadata = []
        if isinstance(metadata, dict):
            for key, item in metadata.items():
                if isinstance(item, dict):  # Ensure each item is a dictionary
                    descriptive = item.get('Descriptive', {})
                    flattened_item = {
                        'IndicatorId': str(key),
                        'Name': descriptive.get('Name', None),
                        'DataSource': descriptive.get('DataSource', None)
                    }
                    flattened_metadata.append(flattened_item)
                else:
                    print("Unexpected item format:", item)
        else:
            print("Unexpected metadata format.")
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    metadata_df = pd.DataFrame(flattened_metadata)
    metadata_df['IndicatorId'] = metadata_df['IndicatorId'].astype(str)

    combined_data = []
    area_type_indicator_dict = {}
    for indicator_id, area_types in area_json_data.items():
        metadata_row = metadata_df.loc[metadata_df['IndicatorId'] == indicator_id]
        if not metadata_row.empty:
            name = metadata_row.iloc[0]['Name']
            data_source = metadata_row.iloc[0]['DataSource']
            combined_data.append({
                'IndicatorId': indicator_id,
                'AreaTypes': area_types,
                'Name': name,
                'DataSource': data_source
            })
            for area_type in area_types:
                if area_type not in area_type_indicator_dict:
                    area_type_indicator_dict[area_type] = []
                area_type_indicator_dict[area_type].append(indicator_id)

    try:
        # Save combined data to JSON file
        with open('data/helpers/indicators_data.json', 'w') as json_file:
            json.dump(combined_data, json_file, indent=4)
        
        # Fetch and save all areas
        areas = ftp.get_all_areas()
        areas_df = pd.DataFrame(areas)
        areas_df.to_csv('data/helpers/areas.csv', index=False)
        areas_df.to_json('data/helpers/areas.json', orient='records')

        # Save area type indicator dictionary to JSON file
        with open('data/helpers/area_type_indicator_dict.json', 'w') as f:
            json.dump(area_type_indicator_dict, f)

        print("Fetched indicator and area metadata and saved helper files in data/helpers")
    except Exception as e:
        print(f"Error saving data: {e}")
