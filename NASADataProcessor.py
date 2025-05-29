import os
import pandas as pd
import requests
import json
from tqdm import tqdm

class Processor:
    def __init__(self, output_dir="nasa_power_data", database_file="district_database.csv", merged_file="merged_all_districts.csv", params_file=None):
        self.output_dir = output_dir
        self.database_file = database_file
        self.merged_file = merged_file
        self.base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"
        self.df_database = pd.read_csv(database_file)
        os.makedirs(self.output_dir, exist_ok=True)

        # Define default API parameters
        self.default_params = {
            "start": "20040101",  # YYYYMMDD
            "end": "20240801",
            "community": "ag",
            "parameters": ",".join([
                "ALLSKY_SFC_SW_DWN", "CLRSKY_SFC_SW_DWN", "ALLSKY_SFC_PAR_TOT", "ALLSKY_SFC_UV_INDEX",
                "T2M", "T2MDEW", "TS", "T2M_RANGE", "QV2M", "RH2M", "PRECTOTCORR",
                "PS", "WS2M", "WD2M", "GWETTOP", "GWETROOT", "GWETPROF"
            ]),
            "format": "csv",
            "header": "true"
        }

        # Load or set parameters
        self.params = self.load_params(params_file) if params_file else self.default_params.copy()

    def load_params(self, params_file):
        if not os.path.exists(params_file):
            raise FileNotFoundError(f"JSON file {params_file} not found.")
        with open(params_file, 'r') as file:
            params = json.load(file)
        print(f"✔ Loaded parameters from {params_file}")
        return params

    def save_params(self, output_file="saved_params.json"):
        """Save current parameters to a JSON file."""
        with open(output_file, 'w') as f:
            json.dump(self.params, f, indent=4)
        print(f"✔ Parameters saved to {output_file}")

    def edit_default_params(self, **kwargs):
        """Edit default parameters dynamically."""
        for key, value in kwargs.items():
            if key in self.default_params:
                print(f"✏ Updating parameter: {key} = {value}")
                self.default_params[key] = value
            else:
                print(f"⚠ Warning: '{key}' is not a recognized parameter key.")

    def merge_csv_files(self):
        all_dataframes = []
        csv_files = [os.path.join(self.output_dir, f) for f in os.listdir(self.output_dir) if f.endswith(".csv")]

        for file in tqdm(csv_files, desc="Merging CSVs"):
            df = pd.read_csv(file)
            all_dataframes.append(df)

        if all_dataframes:
            merged_df = pd.concat(all_dataframes, ignore_index=True)
            merged_df.to_csv(self.merged_file, index=False)
            print(f"✔ Merged CSV saved as {self.merged_file}")
        else:
            print("⚠ No CSV files found to merge.")

    def add_location_data(self):
        for file in tqdm(os.listdir(self.output_dir), desc="Adding location data"):
            if file.endswith(".csv"):
                district_name = file.replace(".csv", "")
                district_info = self.df_database[self.df_database["District"] == district_name]

                if district_info.empty:
                    print(f"⚠ No matching district found for {district_name}")
                    continue

                lat, lon = district_info.iloc[0]["Latitude"], district_info.iloc[0]["Longitude"]
                file_path = os.path.join(self.output_dir, file)
                df = pd.read_csv(file_path)

                df.insert(0, "Region", district_name)
                df.insert(1, "Latitude", lat)
                df.insert(2, "Longitude", lon)
                df.to_csv(file_path, index=False)

    def download_nasa_data(self, district, lat, lon):
        params = self.params.copy()
        params["latitude"] = lat
        params["longitude"] = lon
        try:
            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                filename = os.path.join(self.output_dir, f"{district}.csv")
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(response.text)
                return True
            else:
                print(f"❌ Failed for {district} ({lat}, {lon}) - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error downloading {district}: {e}")
            return False

    def download_data_for_all_districts(self):
        success_count = 0
        for _, row in tqdm(self.df_database.iterrows(), total=len(self.df_database), desc="Downloading NASA data"):
            if self.download_nasa_data(row["District"], row["Latitude"], row["Longitude"]):
                success_count += 1
        print(f"✔ Downloaded data for {success_count}/{len(self.df_database)} districts")

    def clean_csv_files(self):
        for file in tqdm(os.listdir(self.output_dir), desc="Cleaning CSV files"):
            if file.endswith(".csv"):
                file_path = os.path.join(self.output_dir, file)
                df = pd.read_csv(file_path, skiprows=25)
                df.to_csv(file_path, index=False)
