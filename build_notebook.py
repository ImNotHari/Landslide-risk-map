import json

cells = []

def add_markdown(text):
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.split("\n")]
    })

def add_code(code):
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in code.split("\n")]
    })

add_markdown("# Step 1: Initial Inspection of Global Landslide Catalog\nThis notebook performs an initial inspection of the NASA GLC dataset without modifying or cleaning the data.")

add_code("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set visualization style
sns.set_theme(style="whitegrid")

# Load the dataset
df = pd.read_csv("Global_Landslide_Catalog_Export_rows.csv")""")

add_markdown("## 1. Basic Dataset Information")
add_code("""print(f"Number of rows: {len(df)}")
print(f"Number of columns: {len(df.columns)}")""")

add_markdown("## 2. Data Types")
add_code("""print(df.dtypes)""")

add_markdown("## 3. Missing Values")
add_code("""missing_counts = df.isnull().sum()
missing_percentages = (missing_counts / len(df)) * 100

missing_df = pd.DataFrame({
    'Missing Values': missing_counts,
    'Percentage (%)': missing_percentages
})
print(missing_df)""")

add_markdown("## 4. Duplicates")
add_code("""print(f"Duplicate rows: {df.duplicated().sum()}")
print(f"Duplicate event_id values: {df.duplicated(subset=['event_id']).sum()}")""")

add_markdown("## 5. Ranges (Date, Latitude, Longitude)")
add_code("""df['event_date_parsed'] = pd.to_datetime(df['event_date'], errors='coerce')
print(f"Date range: {df['event_date_parsed'].min()} to {df['event_date_parsed'].max()}")
print(f"Latitude range: {df['latitude'].min()} to {df['latitude'].max()}")
print(f"Longitude range: {df['longitude'].min()} to {df['longitude'].max()}")""")

add_markdown("## 6. Unique Geographical Entities")
add_code("""print(f"Number of unique countries: {df['country_name'].nunique()}")
print(f"Number of unique administrative divisions: {df['admin_division_name'].nunique()}")""")

add_markdown("## 7. Categorical Variables")
add_code("""print(f"Unique landslide_category values:\\n{df['landslide_category'].unique()}\\n")
print(f"Unique landslide_trigger values:\\n{df['landslide_trigger'].unique()}\\n")
print(f"Unique landslide_size values:\\n{df['landslide_size'].unique()}\\n")
print(f"Unique landslide_setting values:\\n{df['landslide_setting'].unique()}")""")

add_markdown("## 8. Basic Numerical Statistics")
add_code("""display(df.describe())""")

add_markdown("## 9. Visualizations")

add_code("""# Geographic distribution of events
plt.figure(figsize=(12, 6))
plt.scatter(df['longitude'], df['latitude'], alpha=0.3, s=10, c='red')
plt.title('Geographic Distribution of Landslides')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid(True)
plt.show()""")

add_code("""# Landslides by year
plt.figure(figsize=(12, 5))
df['year'] = df['event_date_parsed'].dt.year
sns.countplot(data=df, x='year', palette='viridis')
plt.title('Landslides by Year')
plt.xlabel('Year')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()""")

add_code("""# Landslides by month
plt.figure(figsize=(10, 5))
df['month'] = df['event_date_parsed'].dt.month
sns.countplot(data=df, x='month', palette='magma')
plt.title('Landslides by Month')
plt.xlabel('Month (1=Jan, 12=Dec)')
plt.ylabel('Count')
plt.show()""")

add_code("""# Landslide trigger distribution
plt.figure(figsize=(12, 6))
sns.countplot(data=df, y='landslide_trigger', order=df['landslide_trigger'].value_counts().index, palette='rocket')
plt.title('Landslide Trigger Distribution')
plt.xlabel('Count')
plt.ylabel('Trigger')
plt.show()""")

add_code("""# Landslide size distribution
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x='landslide_size', order=df['landslide_size'].value_counts().index, palette='mako')
plt.title('Landslide Size Distribution')
plt.xlabel('Size')
plt.ylabel('Count')
plt.show()""")

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.10.12"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open("step1_initial_inspection.ipynb", "w") as f:
    json.dump(notebook, f, indent=2)
