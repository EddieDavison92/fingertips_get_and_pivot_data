# Fingertips Data Downloader

Fingertips Data Downloader is a Python application that simplifies the process of downloading and managing public health data from the Fingertips API. The application fetches metadata related to area types and indicators and presents a user-friendly `tkinter` GUI for selecting and downloading relevant datasets.

## Core functionality

* The application downloads metadata via the `fingertips_py` package, joining data related to area types and indicators; building a map of which indicators are available for each area type.
* The `tkinter` GUI allows users to navigate available datasets by area type and select specific indicators to download.

By default, one `.csv` file is downloaded per selected indicator, containing data for all profiles in that area for all available time periods.

**Additional features:**

There are two checkboxes in the bottom-left corner of the GUI that toggle additional functions:

* `Combine Data Before Saving:` Instead of creating individual files for each indicator, combines all of the data frames after the selected indicators have been downloaded, resulting in one concatenated `.csv` file.

- `Keep Latest Data Only:` Applies a filter to the data frame for each indicator to select the most recent period.

![image](https://github.com/user-attachments/assets/565af625-8224-4f6b-99ce-f2df68a0d165)

## **Setup:**

Clone this repository.

**Create a new virtual environment**

```
python -m venv venv
```

**Activate the environment**

```
venv/scripts/activate
```

**Ensure the required Python packages are installed:**

```
pip install -r requirements.txt
```

This installs packages: `fingertips_py`, `pandas`, `tqdm` and `tk` and their subcomponents.

# Usage

**Run `main.py`:**

```
python main.py
```

## Directory Structure

`data/processed/` Contains the downloaded data sets ready for analysis.

`data/helpers/` Contains json and csv files storing the indicator and area type metadata.

`scripts` Contains python files that `main.py` depends on. You do not need to run these.

Directories are created automatically.

## Scripts

The repository contains four python scripts:

`main.py`, initialises the requried metadata from fingertips and launches the tkinter interface, as well as contains the program main loop.

`scripts/data_processing` contains functions used for downloading and cleaning data sets from fingertips.

`scripts/fetch_initial_data` downloads the required metadata for area types and indicator id's, joins those tables and creates helper files.

`scripts/ui` contains functions for the tkinter components including logic for the interactive elements.

## License

  This repository is dual licensed under the Open Government v3 & MIT. All code and outputs are subject to Crown Copyright.
