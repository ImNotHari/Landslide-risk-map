import pandas as pd
import numpy as np
import os
import shutil

# Ensure directories exist
os.makedirs('data/raw', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)

# Define file paths
original_csv = 'Global_Landslide_Catalog_Export_rows.csv'
raw_csv = 'data/raw/Global_Landslide_Catalog_Export_rows.csv'
processed_csv = 'data/processed/cleaned_global_landslides.csv'
report_file = 'data/processed/data_quality_report.txt'

# Copy to raw if not there
if os.path.exists(original_csv) and not os.path.exists(raw_csv):
    shutil.copy(original_csv, raw_csv)

# Load data
df = pd.read_csv(raw_csv)
original_row_count = len(df)

report_lines = []
report_lines.append(f"--- Data Quality Report ---")
report_lines.append(f"Original Row Count: {original_row_count}")
report_lines.append("\n--- Cleaning Operations ---")

def log_operation(action, reason, affected_rows):
    msg = f"\nAction: {action}\nReason: {reason}\nAffected Rows: {affected_rows}"
    print(msg)
    report_lines.append(msg)

# 1. Invalid or missing latitude/longitude & Impossible geographic coordinates
invalid_coords_mask = df['latitude'].isnull() | df['longitude'].isnull() | (df['latitude'] < -90) | (df['latitude'] > 90) | (df['longitude'] < -180) | (df['longitude'] > 180)
invalid_coords_count = invalid_coords_mask.sum()
df = df[~invalid_coords_mask]
log_operation(
    "Removed rows with invalid or missing latitude/longitude.",
    "Machine learning geospatial models require precise coordinates.",
    invalid_coords_count
)

# 2. Invalid dates
invalid_dates_mask = pd.to_datetime(df['event_date'], errors='coerce').isnull()
invalid_dates_count = invalid_dates_mask.sum()
df = df[~invalid_dates_mask]
df['event_date'] = pd.to_datetime(df['event_date'], errors='coerce').dt.strftime('%Y-%m-%d')
log_operation(
    "Removed rows with unparseable event_date and standardized format to YYYY-MM-DD.",
    "Temporal analysis requires valid dates. Unparseable dates cannot be imputed reliably.",
    invalid_dates_count
)

# 3. Duplicate rows
duplicates_mask = df.duplicated()
duplicates_count = duplicates_mask.sum()
df = df.drop_duplicates()
log_operation(
    "Removed duplicate rows.",
    "Redundant data biases model training.",
    duplicates_count
)

# 4. Duplicate event IDs
duplicate_event_ids_mask = df.duplicated(subset=['event_id'], keep='first')
duplicate_event_ids_count = duplicate_event_ids_mask.sum()
df = df.drop_duplicates(subset=['event_id'], keep='first')
log_operation(
    "Removed rows with duplicate event_id values (kept first).",
    "Each event should be unique to avoid data leakage.",
    duplicate_event_ids_count
)

# 5. Inconsistent categorical values (and filling NaNs in them)
categorical_cols = ['landslide_category', 'landslide_trigger', 'landslide_size', 'landslide_setting']
affected_categorical = 0
for col in categorical_cols:
    mask = df[col].isnull() | df[col].str.lower().isin(['other', 'unknown'])
    affected_categorical += mask.sum()
    df[col] = df[col].fillna('unknown').str.lower()
    df.loc[df[col] == 'other', col] = 'unknown'

log_operation(
    "Standardized categorical columns (category, trigger, size, setting) to lowercase and merged 'NaN' and 'other' into 'unknown'.",
    "Reduces dimensionality and consolidates ambiguous labels.",
    affected_categorical
)

# 6. Missing values in severe/sparse columns
cols_to_drop = ['event_time', 'notes', 'storm_name', 'photo_link']
affected_drop = len(df) # affects all rows
df = df.drop(columns=cols_to_drop, errors='ignore')
log_operation(
    f"Dropped highly missing columns: {cols_to_drop}.",
    "These columns lack sufficient data (>80% missing) to provide statistical value.",
    affected_drop
)

# 7. Missing values in numerical variables (fatalities, injuries)
missing_fatalities = df['fatality_count'].isnull().sum()
df['fatality_count'] = df['fatality_count'].fillna(0)
missing_injuries = df['injury_count'].isnull().sum()
df['injury_count'] = df['injury_count'].fillna(0)
log_operation(
    "Imputed missing fatality_count and injury_count with 0.",
    "Missing records for casualties likely indicate zero casualties. Better to preserve rows than discard them.",
    missing_fatalities + missing_injuries
)

# 8. Incorrect numerical data types
df['fatality_count'] = df['fatality_count'].astype(int)
df['injury_count'] = df['injury_count'].astype(int)
df['event_id'] = df['event_id'].astype(int)
log_operation(
    "Converted fatality_count, injury_count, and event_id to integer.",
    "Counts and IDs cannot be fractional.",
    len(df)
)

# 9. Fill missing geographic divisions
geo_cols = ['country_name', 'country_code', 'admin_division_name', 'gazeteer_closest_point']
affected_geo = df[geo_cols].isnull().sum().sum()
df[geo_cols] = df[geo_cols].fillna('unknown')
log_operation(
    "Imputed missing geopolitical identifiers (country, admin division, gazeteer) with 'unknown'.",
    "Missing geo-tags shouldn't force removal of rows since lat/lon exists and can be reverse-geocoded in the future.",
    affected_geo
)

final_row_count = len(df)
rows_removed = original_row_count - final_row_count

report_lines.append("\n--- Final Summary ---")
report_lines.append(f"Final Row Count: {final_row_count}")
report_lines.append(f"Rows Removed: {rows_removed}")

# Write output CSV
df.to_csv(processed_csv, index=False)

# Write report
with open(report_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(report_lines))

print(f"\nPipeline complete. Data saved to {processed_csv}")
print(f"Report saved to {report_file}")
