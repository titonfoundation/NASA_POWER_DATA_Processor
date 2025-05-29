````markdown
# 🌍 NASA POWER Data Processor

A lightweight and customizable Python library for downloading, cleaning, and aggregating 20+ years of NASA POWER climate data (temperature, radiation, humidity, soil moisture, etc.) for multiple regions — designed for researchers, data scientists, and environmental analysts.

![NASA](https://img.shields.io/badge/NASA-POWER-blue.svg) ![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg) ![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 🚀 Features

- 📥 Automatically download daily climate data using the [NASA POWER API](https://power.larc.nasa.gov/docs/services/api/)
- 📌 Customize data fields and parameters via JSON
- 🧩 Merge and clean CSV files efficiently
- 📍 Add latitude, longitude, and region metadata using your own database
- 🧼 Strip NASA header rows to get clean DataFrames for ML or analysis

---

## 📦 Installation

Install via `pip` from your local clone:

```bash
git clone https://github.com/titonfoundation/NASA_POWER_DATA_Processor.git
cd NASA_POWER_DATA_Processor
pip install .
````

---

## 🛠 Usage

```python
from nasa_power_data_processor import Processor

# Initialize processor (you can provide a custom params JSON)
processor = Processor(database_file="district_database.csv")

# Download NASA POWER data for all districts in your CSV
processor.download_data_for_all_districts()

# Clean files (removes first 25 rows added by NASA API)
processor.clean_csv_files()

# Add location info to each CSV
processor.add_location_data()

# Merge all CSVs into one
processor.merge_csv_files()
```

---

## 🗂 Expected Input Format

### `district_database.csv`

Must contain the following columns:

| District   | Latitude | Longitude |
| ---------- | -------- | --------- |
| Dhaka      | 23.8103  | 90.4125   |
| Chittagong | 22.3569  | 91.7832   |
| ...        | ...      | ...       |

---

## ⚙ Custom Parameters (Optional)

You can override the default parameters using a JSON file:

```json
{
  "start": "20040101",
  "end": "20240801",
  "parameters": "T2M,PRECTOTCORR,WS2M",
  "format": "CSV",
  "community": "AG"
}
```

Then initialize the processor like this:

```python
processor = Processor(params_file="my_custom_params.json")
```

---

## 📁 Project Structure

```
NASA_POWER_DATA_Processor/
├── nasa_power_data_processor/
│   └── __init__.py
├── setup.py
├── README.md
├── requirements.txt
└── LICENSE
```

---

## 📊 Use Cases

* Agricultural monitoring and drought analysis
* Weather forecasting models
* Machine learning for climate prediction
* GIS and remote sensing integration

---

## ✅ Dependencies

* `pandas`
* `requests`
* `numpy` *(optional)*

Install them with:

```bash
pip install -r requirements.txt
```

---

## 📝 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙌 Acknowledgements

* [NASA POWER Data Access Viewer](https://power.larc.nasa.gov)
* [Open-Meteo API](https://open-meteo.com/) (for possible future integration)

---

## 🤝 Contributing

PRs, feature suggestions, and feedback are welcome! Please open an issue to start a discussion.

---

## 👤 Author

**Tonmoy Paul**
Team Lead – Biomedical & AI Projects @ BIOSE Lab, BRAC University
GitHub: [@titonfoundation](https://github.com/titonfoundation)

---

```
