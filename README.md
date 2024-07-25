# Overview

This repository contains scripts for downloading and processing health indicator data from the Fingertips API. The scripts are designed to fetch data for specified indicators, process it to retain relevant information, and generate a comprehensive report.

## Scripts

### 1. `download_indicators.py`

This script downloads health indicator data from the Fingertips API.

**Key Features:**
- Fetches data for a list of specified indicators.
- Downloads data in batches to manage large data sizes.
- Saves the fetched data as a CSV file.

**Usage:**

Ensure the required Python packages are installed:

```
pip install requests pandas
```
Run the script:
```
python scripts/download_indicators.py
```
Details:
  Indicators: You can modify the list of indicators to fetch by updating the indicators list in the script.
  Functionality: The script fetches data in batches and saves it to data/raw/fingertips_data.csv.

### 2. `process_data.py`

This script processes the downloaded health indicator data to generate a comprehensive report.

Key Features:

-- Filters data to include only relevant area types.
-- Pivots the data to create a structured report.
-- Removes columns with all empty values.
-- Saves the processed data as a CSV file.

Usage:

Ensure the required Python packages are installed:

```
pip install pandas
```
Run the script:

```
python scripts/process_data.py
```
Details:
    Functionality: The script processes the raw data, filtering and pivoting it to create a final report.
    Output: The processed data is saved to data/processed/fingertips_data.csv.

### Directory Structure
  data/raw/: Contains the raw data fetched from the Fingertips API.
  data/processed/: Contains the processed data ready for analysis.

### Notes
  Ensure you have the necessary permissions to create directories and save files in the specified paths.
  Modify the list of indicators in download_indicators.py to tailor the data fetched as per your requirements.

## License
  This repository is dual licensed under the Open Government v3 & MIT. All code and outputs are subject to Crown Copyright.
