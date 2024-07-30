import tkinter as tk
from tkinter import ttk, messagebox, font
from scripts.data_processing import download_and_process_data, clean_data_source, clean_indicator_name

class IndicatorSelectionApp:
    def __init__(self, root, combined_data, area_data_df, area_type_indicator_dict):
        """
        Initialize the Indicator Selection App.
        
        Parameters:
        root (Tk): The root Tkinter window.
        combined_data (list): The combined data for indicators.
        area_data_df (DataFrame): DataFrame containing area data.
        area_type_indicator_dict (dict): Dictionary mapping area types to indicator IDs.
        """
        self.root = root
        self.area_types = self.get_area_types(area_data_df, area_type_indicator_dict)
        self.indicators = combined_data

        # Calculate dynamic height
        area_types_count = len(self.area_types)
        min_height = max(600, 300 + (area_types_count * 20))

        self.root.title("Fingertips Data Downloader")
        self.root.geometry(f"1000x{min_height}")
        self.root.minsize(1000, min_height)  # Prevent the window from being resized to less than 1000x(min_height)

        self.selected_area_type = tk.StringVar(value="")  # No default selection

        self.create_widgets()

    def get_area_types(self, area_data_df, area_type_indicator_dict):
        """
        Get list of area types from area data and indicator dictionary.
        
        Parameters:
        area_data_df (DataFrame): DataFrame containing area data.
        area_type_indicator_dict (dict): Dictionary mapping area types to indicator IDs.
        
        Returns:
        list: List of area types.
        """
        area_types = []
        for col in area_data_df.columns:
            area_type_id = str(col)  # Ensure area_type_id is a string
            if area_type_id in area_type_indicator_dict:  # Only include area types with indicators
                area_types.append(f"{area_data_df[col][1]} (ID: {col})")
        return sorted(area_types)

    def create_widgets(self):
        """Create the widgets for the Tkinter UI."""
        bold_font = font.Font(weight="bold")

        self.top_frame = tk.Frame(self.root, padx=10, pady=10)
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Adjust the width allocation by setting expand=False for left_frame and expand=True for right_frame
        self.left_frame = tk.Frame(self.top_frame, relief=tk.SOLID, borderwidth=1, padx=10, pady=10)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5, expand=False)

        self.right_frame = tk.Frame(self.top_frame, relief=tk.SOLID, borderwidth=1, padx=10, pady=10)
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.bottom_frame = tk.Frame(self.root, padx=10, pady=10)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        self.area_label = tk.Label(self.left_frame, text="Select Area Type:", font=bold_font)
        self.area_label.pack(anchor='w')

        self.area_canvas = tk.Canvas(self.left_frame)
        self.area_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.area_frame = tk.Frame(self.area_canvas)
        self.area_canvas.create_window((0, 0), window=self.area_frame, anchor="nw")

        self.radio_buttons = []
        for area_type in self.area_types:
            radio = tk.Radiobutton(self.area_frame, text=area_type, variable=self.selected_area_type, value=area_type, command=self.load_indicators)
            radio.pack(anchor='w')
            self.radio_buttons.append(radio)

        self.selected_area_type.set("")  # Manually clear all selections

        self.indicator_label = tk.Label(self.right_frame, text="Select Indicators:", font=bold_font)
        self.indicator_label.pack(anchor='w')

        self.loading_label = tk.Label(self.right_frame, text="Please select an area type.", font=("Arial", 10))
        self.loading_label.pack(anchor='w', padx=10, pady=5)

        self.indicator_canvas = tk.Canvas(self.right_frame)
        self.indicator_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.indicator_scrollbar = ttk.Scrollbar(self.right_frame, orient="vertical", command=self.indicator_canvas.yview)
        self.indicator_scrollbar.pack(side=tk.RIGHT, fill="y")

        self.indicator_canvas.configure(yscrollcommand=self.indicator_scrollbar.set)
        self.indicator_canvas.bind('<Configure>', lambda e: self.indicator_canvas.configure(scrollregion=self.indicator_canvas.bbox("all")))
        self.indicator_canvas.bind_all("<MouseWheel>", lambda event: self.on_mouse_wheel(event, self.indicator_canvas))

        self.indicator_frame = tk.Frame(self.indicator_canvas)
        self.indicator_canvas.create_window((0, 0), window=self.indicator_frame, anchor="nw")

        self.indicator_vars = []
        self.indicator_checkboxes = []
        self.indicator_labels = []

        self.create_bottom_widgets()

    def create_bottom_widgets(self):
        """Create the widgets for the bottom frame."""
        self.combine_data_var = tk.BooleanVar()
        self.combine_data_checkbox = tk.Checkbutton(self.bottom_frame, text="Combine Data Before Saving", variable=self.combine_data_var)
        self.combine_data_checkbox.pack(side=tk.LEFT)

        self.latest_data_var = tk.BooleanVar()
        self.latest_data_checkbox = tk.Checkbutton(self.bottom_frame, text="Keep Latest Data Only", variable=self.latest_data_var)
        self.latest_data_checkbox.pack(side=tk.LEFT)

        self.delete_empty_columns_var = tk.BooleanVar()
        self.delete_empty_columns_checkbox = tk.Checkbutton(self.bottom_frame, text="Delete Empty Columns", variable=self.delete_empty_columns_var)
        self.delete_empty_columns_checkbox.pack(side=tk.LEFT)

        self.download_button = tk.Button(self.bottom_frame, text="Download", command=self.download)
        self.download_button.pack(side=tk.RIGHT, padx=5)

        self.select_all_button = tk.Button(self.bottom_frame, text="Select All", command=self.toggle_select_all)
        self.select_all_button.pack(side=tk.RIGHT)

        self.all_selected = False

    def on_mouse_wheel(self, event, canvas):
        """Scroll the canvas on mouse wheel event."""
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def load_indicators(self):
        """Load indicators based on the selected area type."""
        self.loading_label.config(text="Loading...")
        self.loading_label.pack(anchor='w', padx=10, pady=5)  # Ensure it's packed when loading
        self.root.update_idletasks()

        # Clear previous indicators
        for label in self.indicator_labels:
            label.destroy()
        for checkbox in self.indicator_checkboxes:
            checkbox.destroy()
        self.indicator_vars.clear()
        self.indicator_checkboxes.clear()
        self.indicator_labels.clear()

        selected_area_id = self.selected_area_type.get().split("(ID: ")[1].strip(")")

        # Group indicators by DataSource and sort them alphabetically within each group
        indicators_by_source = {}
        for indicator in self.indicators:
            if selected_area_id in indicator['AreaTypes']:
                source = clean_data_source(indicator['DataSource'])
                if source not in indicators_by_source:
                    indicators_by_source[source] = []
                indicators_by_source[source].append(indicator)

        # Create UI elements for each indicator, grouped by DataSource
        for source in sorted(indicators_by_source.keys()):
            source_label = tk.Label(self.indicator_frame, text=f"{source}:", font=font.Font(weight="bold", size=10))
            source_label.pack(anchor='w')
            self.indicator_labels.append(source_label)
            for indicator in sorted(indicators_by_source[source], key=lambda x: x['Name']):
                var = tk.BooleanVar()
                checkbox_text = f"{clean_indicator_name(indicator['Name'])} (ID: {indicator['IndicatorId']})"
                checkbox = tk.Checkbutton(self.indicator_frame, text=checkbox_text, variable=var)
                checkbox.pack(anchor='w')
                self.indicator_vars.append((var, indicator['IndicatorId']))
                self.indicator_checkboxes.append(checkbox)

        self.loading_label.pack_forget()
        self.indicator_canvas.configure(scrollregion=self.indicator_canvas.bbox("all"))

    def toggle_select_all(self):
        """Toggle the selection of all indicators."""
        self.all_selected = not self.all_selected
        for var, _ in self.indicator_vars:
            var.set(self.all_selected)
        self.select_all_button.config(text="Unselect All" if self.all_selected else "Select All")

    def download(self):
        """Submit the selected indicators and download the data."""
        selected_area = self.selected_area_type.get()
        if not selected_area:
            messagebox.showerror("Error", "Please select an area type.")
            return

        selected_indicators = [indicator_id for var, indicator_id in self.indicator_vars if var.get()]
        if not selected_indicators:
            messagebox.showerror("Error", "Please select at least one indicator.")
            return

        print(f"Final selected indicator IDs: {selected_indicators}")
        area_type_id = selected_area.split("(ID: ")[1].strip(")")
        combine = self.combine_data_var.get()
        keep_latest = self.latest_data_var.get()
        delete_empty_columns = self.delete_empty_columns_var.get()

        try:
            download_and_process_data(selected_indicators, area_type_id, self.indicators, combine, keep_latest, delete_empty_columns)
            messagebox.showinfo("Success", "Data downloaded and processed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
