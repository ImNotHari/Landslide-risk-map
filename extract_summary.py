import pandas as pd
import numpy as np

# Load data
df = pd.read_csv("Global_Landslide_Catalog_Export_rows.csv")

print("--- SUMMARY INFO ---")
print(f"Number of rows: {len(df)}")
print(f"Number of columns: {len(df.columns)}")
print("\nData types:")
print(df.dtypes)
print("\nMissing values:")
print(df.isnull().sum())
print("\nPercentage of missing values:")
print((df.isnull().sum() / len(df)) * 100)
print(f"\nDuplicate rows: {df.duplicated().sum()}")
print(f"Duplicate event_id values: {df.duplicated(subset=['event_id']).sum()}")

# Dates
df['event_date_parsed'] = pd.to_datetime(df['event_date'], errors='coerce')
print(f"\nDate range: {df['event_date_parsed'].min()} to {df['event_date_parsed'].max()}")

print(f"Latitude range: {df['latitude'].min()} to {df['latitude'].max()}")
print(f"Longitude range: {df['longitude'].min()} to {df['longitude'].max()}")

print(f"Number of unique countries: {df['country_name'].nunique()}")
print(f"Number of unique administrative divisions: {df['admin_division_name'].nunique()}")

print(f"\nUnique landslide_category values:\n{df['landslide_category'].unique()}")
print(f"Unique landslide_trigger values:\n{df['landslide_trigger'].unique()}")
print(f"Unique landslide_size values:\n{df['landslide_size'].unique()}")
print(f"Unique landslide_setting values:\n{df['landslide_setting'].unique()}")

print("\nBasic numerical statistics:")
print(df.describe())
