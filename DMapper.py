
import tkinter as tk
from tkinter import filedialog, messagebox
from charset_normalizer import from_path
import pandas as pd
import os

class DestinationMapperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Destination Mapping Tool")
        
        # Use a light pastel background
        self.root.configure(bg="#F0F8FF")

        # Variables to hold file paths
        self.airports_path_var = tk.StringVar()
        self.city_map_path_var = tk.StringVar()
        self.data_path_var = tk.StringVar()
        self.output_folder_var = tk.StringVar()

        # Create the layout
        self.create_widgets()

    def create_widgets(self):
        # A frame to hold all widgets, also with pastel background
        main_frame = tk.Frame(self.root, bg="#F0F8FF")
        main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Title Label
        title_label = tk.Label(
            main_frame, 
            text="Select necessary files and output folder:",
            bg="#F0F8FF", 
            fg="#333333",
            font=("Arial", 12, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 15), sticky="w")

        # Row 1: Airport Mapping
        tk.Label(main_frame, text="Airports -> Country CSV:", bg="#F0F8FF", font=("Arial", 10)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(main_frame, textvariable=self.airports_path_var, width=50, font=("Arial", 10)).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(main_frame, text="Browse...", command=self.browse_airports_csv, font=("Arial", 9), bg="#E6F7FF").grid(row=1, column=2, padx=5, pady=5)

        # Row 2: City Mapping
        tk.Label(main_frame, text="City -> Country CSV:", bg="#F0F8FF", font=("Arial", 10)).grid(row=2, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(main_frame, textvariable=self.city_map_path_var, width=50, font=("Arial", 10)).grid(row=2, column=1, padx=5, pady=5)
        tk.Button(main_frame, text="Browse...", command=self.browse_city_csv, font=("Arial", 9), bg="#E6F7FF").grid(row=2, column=2, padx=5, pady=5)

        # Row 3: Data CSV
        tk.Label(main_frame, text="Source CSV (with 'Destination' col):", bg="#F0F8FF", font=("Arial", 10)).grid(row=3, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(main_frame, textvariable=self.data_path_var, width=50, font=("Arial", 10)).grid(row=3, column=1, padx=5, pady=5)
        tk.Button(main_frame, text="Browse...", command=self.browse_data_csv, font=("Arial", 9), bg="#E6F7FF").grid(row=3, column=2, padx=5, pady=5)

        # Row 4: Output Folder
        tk.Label(main_frame, text="Output Folder:", bg="#F0F8FF", font=("Arial", 10)).grid(row=4, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(main_frame, textvariable=self.output_folder_var, width=50, font=("Arial", 10)).grid(row=4, column=1, padx=5, pady=5)
        tk.Button(main_frame, text="Browse...", command=self.browse_output_folder, font=("Arial", 9), bg="#E6F7FF").grid(row=4, column=2, padx=5, pady=5)

        # Row 5: Map Destinations button
        map_button = tk.Button(main_frame, text="Map Destinations", command=self.map_destinations, 
                               font=("Arial", 11, "bold"), fg="#ffffff", bg="#3498db", width=18, pady=5)
        map_button.grid(row=5, column=0, columnspan=3, pady=(20, 0))

        # Make columns expand horizontally if window is resized
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

    def browse_airports_csv(self):
        path = filedialog.askopenfilename(
            title="Select the airports_to_code_mapping CSV",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if path:
            self.airports_path_var.set(path)

    def browse_city_csv(self):
        path = filedialog.askopenfilename(
            title="Select the city_to_country_mapping CSV",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if path:
            self.city_map_path_var.set(path)

    def browse_data_csv(self):
        path = filedialog.askopenfilename(
            title="Select the source CSV with 'Destination' column",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if path:
            self.data_path_var.set(path)

    def browse_output_folder(self):
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.output_folder_var.set(folder)

    def map_destinations(self):
        airports_path = self.airports_path_var.get().strip()
        city_map_path = self.city_map_path_var.get().strip()
        data_path = self.data_path_var.get().strip()
        output_folder = self.output_folder_var.get().strip()

        # Basic validations
        if not (airports_path and city_map_path and data_path and output_folder):
            messagebox.showerror("Error", "Please specify all required paths.")
            return

        if not os.path.isfile(airports_path):
            messagebox.showerror("Error", f"Airports file not found:\n{airports_path}")
            return

        if not os.path.isfile(city_map_path):
            messagebox.showerror("Error", f"City mapping file not found:\n{city_map_path}")
            return

        if not os.path.isfile(data_path):
            messagebox.showerror("Error", f"Data CSV not found:\n{data_path}")
            return

        if not os.path.isdir(output_folder):
            # Attempt to create folder if not existing
            try:
                os.makedirs(output_folder)
            except Exception as e:
                messagebox.showerror("Error", f"Unable to create output folder:\n{output_folder}\n{str(e)}")
                return

        # Load Data
        try:
            # Read file with encoding
            result = from_path(data_path).best()
            data = pd.read_csv(data_path, encoding=result.encoding)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read data CSV:\n{data_path}\n{str(e)}")
            return

        if 'Destination' not in data.columns:
            messagebox.showerror("Error", "'Destination' column not found in your data CSV.")
            return

        # Load city mapping
        try:
            city_df = pd.read_csv(city_map_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read city-country mapping:\n{city_map_path}\n{str(e)}")
            return

        if not {'name', 'Country'}.issubset(city_df.columns):
            messagebox.showerror("Error", "City mapping CSV must contain 'name' and 'Country' columns.")
            return

        city_country_dict = dict(zip(city_df["name"], city_df["Country"]))

        # Load airport mapping
        try:
            airports_df = pd.read_csv(airports_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read airports mapping:\n{airports_path}\n{str(e)}")
            return

        if not {'IATA', 'Country'}.issubset(airports_df.columns):
            messagebox.showerror("Error", "Airports CSV must contain 'IATA' and 'Country' columns.")
            return

        airport_to_country_dict = dict(zip(airports_df["IATA"], airports_df["Country"]))

        # Perform mapping
        data['MappedDestination'] = (
            data['Destination']
            .map(city_country_dict)
            .fillna(data['Destination'].map(airport_to_country_dict))
            .fillna(data['Destination'])
        )

        # Generate output file path
        original_file_name = os.path.basename(data_path)
        file_name, file_extension = os.path.splitext(original_file_name)
        new_file_name = f"{file_name}_updated_dest{file_extension}"
        new_file_path = os.path.join(output_folder, new_file_name)

        # Save updated CSV
        try:
            data.to_csv(new_file_path, index=False)
            messagebox.showinfo("Success", f"Updated file saved to:\n{new_file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to write updated CSV:\n{new_file_path}\n{str(e)}")
            return

def run_app():
    root = tk.Tk()
    root.minsize(600, 320)  # a bit bigger starting window
    app = DestinationMapperApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_app()