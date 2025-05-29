import pandas as pd
import numpy as np
import os

locations = {
    "Rangpur": (25.6319, 89.2491),
    "Dinajpur": (25.6212, 88.6353),
    "Panchagarh": (26.1333, 88.4167),
    "Kurigram": (25.8, 88.85),
    "Lalmonirhat": (25.92163, 89.4291077),
    "Nilphamari": (25.9, 88.6333),
    "Gaibandha": (25.3333, 89.1667),
    "Joypurhat": (25.102449, 89.0012524),
    "Thakurgaon": (26.0273613, 88.4577299),
    "Naogaon": (24.8061084, 88.9160439),
    "Bogura": (24.8416791, 89.3290379),
    "Rajshahi": (24.3795917, 88.5649606),
    "Tangail": (24.433, 89.9051),
    "Mymensingh": (24.75, 90.3667),
    "Sherpur": (25.0167, 89.9833),
    "Kishoreganj": (24.4326534, 90.7609991),
    "Manikganj": (23.9833, 89.8667),
    "Dhaka": (23.7808186, 90.3372883),
    "Khulna": (22.8217, 89.5317),
    "Barishal": (22.7085, 90.3545),
    "Jessore": (23, 89.0333),
    "Chittagong": (22.3583, 91.8333),
    "Comilla": (23.4833, 91.1667),
    "Bagerhat": (22.6167, 89.6333),
    "Patuakhali": (22.3667, 90.3333),
    "Narail": (23.1667, 89.3333),
    "Pirojpur": (22.6, 90.0833),
    "Jhenaidah": (23.1667, 89.1667),
    "Magura": (23.25, 89.4167),
    "Satkhira": (22.714607, 89.049574),
    "Pabna": (24.0104993, 89.2290062),
    "Natore": (24.3798526, 88.9278957),
    "Sirajganj": (24.4573428, 89.6788815),
    "Kustia": (23.9455886, 88.8666637),
    "Noakhali": (22.5582479, 90.853962),
    "Rangamati": (22.642732, 92.1525353),
    "Sylhet": (24.8999805, 91.8198361),
    "Habiganj": (24.3786881, 91.3956966)
}


count = 0
for key in locations:
    path = f'/home/tonmoy/Project/1. Research/District_Dataset/{key}.csv'
    
    if os.path.exists(path):
        count += 1
        #print(path)
    else:
        print(f"Path does not exist: {path}")

print(count)

for district, coords in locations.items():
    
    path = f'/home/tonmoy/Project/1. Research/District_Dataset/{district}.csv'
    data = pd.read_csv(path)

    data['Region'] = district
    data['Latitude'] = coords[0]
    data['Longitude'] = coords[1]
    
    data = data[['Region', 'Latitude', 'Longitude', 'YEAR', 'DOY', 'ALLSKY_SFC_SW_DWN', 'CLRSKY_SFC_SW_DWN', 'ALLSKY_SFC_SW_DNI', 'ALLSKY_SFC_SW_DIFF', 'T2M', 'T2MDEW', 'TS', 'T2M_MAX', 'T2M_MIN', 'QV2M', 'RH2M', 'PS', 'WS2M', 'WS2M_MAX', 'WS2M_MIN', 'GWETTOP', 'GWETROOT', 'GWETPROF']]

    file_name = f'/home/tonmoy/Project/1. Research/Refined_Dataset/{district}.csv'
    data.to_csv(file_name, index=False)


# Directory containing the district CSV files
directory = 'Refined_Dataset/'

# List to store data from each CSV file
data_frames = []

# Iterate over each CSV file in the directory
for district in locations.keys():
    file_path = os.path.join(directory, f'{district}.csv')
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Append the DataFrame to the list
    data_frames.append(df)

# Concatenate all DataFrames into a single DataFrame
combined_data = pd.concat(data_frames, ignore_index=True)

# Save the combined DataFrame to a single CSV file
combined_file_path = '/home/tonmoy/Project/1. Research/All_Districts_Combined.csv'
combined_data.to_csv(combined_file_path, index=False)
