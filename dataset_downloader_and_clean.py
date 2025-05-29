import requests
import os
import pandas as pd

# Define the base URL for the NASA POWER API
BASE_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

# Define parameters (excluding location-specific ones)
PARAMS = {
    "start": "20040101", #YYYYMMDD
    "end": "20240801",
    "community": "ag",
    "parameters": "ALLSKY_SFC_SW_DWN,CLRSKY_SFC_SW_DWN,ALLSKY_SFC_PAR_TOT,ALLSKY_SFC_UV_INDEX," 
                  "T2M,T2MDEW,TS,T2M_RANGE,QV2M,RH2M,PRECTOTCORR,PS,WS2M,WD2M,GWETTOP,GWETROOT,GWETPROF",
    "format": "csv",
    "header": "true"
}

# Read locations from CSV file
df = pd.read_csv("district_database.csv")

# Output directory
OUTPUT_DIR = "nasa_power_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Loop through locations and download data
def download_nasa_data(district, lat, lon):
    params = PARAMS.copy()
    params["latitude"] = lat
    params["longitude"] = lon
    
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        filename = f"{OUTPUT_DIR}/{district}.csv"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(response.text)
        print(f"Data saved: {filename}")
    else:
        print(f"Failed to retrieve data for {district} ({lat}, {lon}) - Status Code: {response.status_code}")

# Run the download function for all districts
for _, row in df.iterrows():
    download_nasa_data(row["District"], row["Latitude"], row["Longitude"])

# Remove first 25 rows from all CSV files in nasa_power_data folder
def clean_csv_files():
    for file in os.listdir(OUTPUT_DIR):
        if file.endswith(".csv"):
            file_path = os.path.join(OUTPUT_DIR, file)
            df = pd.read_csv(file_path, skiprows=25)
            df.to_csv(file_path, index=False)
            print(f"Cleaned and saved: {file_path}")

# Execute the cleaning function
clean_csv_files()
