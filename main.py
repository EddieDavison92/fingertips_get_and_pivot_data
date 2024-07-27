import json
import pandas as pd
from tkinter import Tk
from scripts.fetch_initial_data import fetch_and_save_data
from scripts.ui import IndicatorSelectionApp

def main():
    # Fetch and save initial data from the API
    print("Fetching indicator metadata from fingertips API...")
    try:
        fetch_and_save_data()
    except Exception as e:
        print(f"Error fetching initial data: {e}")
        return

    # Load data from saved JSON files
    try:
        area_data_df = pd.read_json('data/helpers/areas.json')
        with open('data/helpers/indicators_data.json', 'r') as f:
            combined_data = json.load(f)
        with open('data/helpers/area_type_indicator_dict.json', 'r') as f:
            area_type_indicator_dict = json.load(f)
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return

    # Create and run the Tkinter UI
    root = Tk()
    app = IndicatorSelectionApp(root, combined_data, area_data_df, area_type_indicator_dict)
    root.mainloop()

if __name__ == "__main__":
    main()
