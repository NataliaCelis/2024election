import requests
import pandas as pd

# API Key
api_key = "0f85bf128c81ea951f8df68ea1f48e31f673c389"

# API Endpoint and Variables
base_url = "https://api.census.gov/data/2023/acs/acsse"
variables = ",".join([
    "NAME",
    "K200101_001E",  # Total population
    "K200103_001E",  # Median age
    "K201902_001E",  # Median household income
    "K202510_001E",  # Median home value
    "K200201_002E",  # White population
    "K200201_003E",  # Black population
    "K200201_004E",  # Native population
    "K200201_005E",  # Asian population
    "K200301_003E",  # Hispanic population
    "K200301_001E",  # Total Hispanic calculation base
    "K200101_002E",  # Male population
    "K201501_008E",  # Graduate or professional degree
    "K201501_007E",  # Bachelor's degree
    "K201803_002E"   # STEM fields
])

# Geography Filter for North Carolina
state_fips = "37"
geography = "county"

# Construct the API URL
api_url = f"{base_url}?get={variables}&for={geography}:*&in=state:{state_fips}&key={api_key}"

# Make the API Call
response = requests.get(api_url)

# Check Response Status
if response.status_code == 200:
    print("API Call Successful!")
    data = response.json()
else:
    print(f"API Call Failed! Status Code: {response.status_code}")
    exit()

# Convert Data to a DataFrame
columns = data[0]  # First row contains column names
rows = data[1:]    # Remaining rows contain data
df = pd.DataFrame(rows, columns=columns)

# Rename Columns
df.rename(columns={
    "K200101_001E": "pop",
    "K200103_001E": "med_age",
    "K201902_001E": "med_inc",
    "K202510_001E": "med_home_val",
    "K200201_002E": "white_pop",
    "K200201_003E": "black_pop",
    "K200201_004E": "native_pop",
    "K200201_005E": "asian_pop",
    "K200301_003E": "hispanic_pop",
    "K200301_001E": "hispanic_total",
    "K200101_002E": "male_pop",
    "K201501_008E": "masters_plus",
    "K201501_007E": "bachelors_plus",
    "K201803_002E": "stem_fields",
    "NAME": "County_Name"
}, inplace=True)

# Drop Unnecessary Columns
df.drop(columns=["state", "county"], inplace=True)

# Convert Numeric Columns
numeric_columns = [
    "pop", "med_age", "med_inc", "med_home_val", "white_pop", "black_pop",
    "native_pop", "asian_pop", "hispanic_pop", "hispanic_total", "male_pop",
    "masters_plus", "bachelors_plus", "stem_fields"
]
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Save to CSV
output_path = "north_carolina_detailed_demographics.csv"
df.to_csv(output_path, index=False)
print(f"Data saved to {output_path}")

# Display Sample Data
print(df.head())
