"""
generate_sample_data.py  
Creates a realistic OECD internet usage + GDP per capita dataset
based on actual World Bank data patterns (2005-2020)
"""
import pandas as pd
import numpy as np
import os

os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

np.random.seed(42)

# Real-world approximate values for 2020 (internet_pct, gdp_usd)
OECD_BASE = {
    "Australia":      ("AUS", 88, 52000),
    "Austria":        ("AUT", 88, 48000),
    "Belgium":        ("BEL", 90, 44000),
    "Canada":         ("CAN", 92, 43000),
    "Chile":          ("CHL", 82, 13000),
    "Colombia":       ("COL", 65, 5800),
    "Czech Republic": ("CZE", 83, 22000),
    "Denmark":        ("DNK", 97, 60000),
    "Estonia":        ("EST", 90, 23000),
    "Finland":        ("FIN", 93, 48000),
    "France":         ("FRA", 85, 39000),
    "Germany":        ("DEU", 90, 46000),
    "Greece":         ("GRC", 78, 17000),
    "Hungary":        ("HUN", 83, 15000),
    "Iceland":        ("ISL", 99, 60000),
    "Ireland":        ("IRL", 91, 80000),
    "Israel":         ("ISR", 87, 43000),
    "Italy":          ("ITA", 74, 31000),
    "Japan":          ("JPN", 90, 40000),
    "South Korea":    ("KOR", 96, 31000),
    "Latvia":         ("LVA", 87, 17000),
    "Lithuania":      ("LTU", 85, 19000),
    "Luxembourg":     ("LUX", 97, 115000),
    "Mexico":         ("MEX", 65, 8500),
    "Netherlands":    ("NLD", 95, 52000),
    "New Zealand":    ("NZL", 90, 41000),
    "Norway":         ("NOR", 97, 67000),
    "Poland":         ("POL", 82, 15000),
    "Portugal":       ("PRT", 78, 21000),
    "Slovakia":       ("SVK", 82, 18000),
    "Slovenia":       ("SVN", 85, 25000),
    "Spain":          ("ESP", 86, 27000),
    "Sweden":         ("SWE", 95, 52000),
    "Switzerland":    ("CHE", 94, 86000),
    "Turkey":         ("TUR", 74, 8600),
    "United Kingdom": ("GBR", 95, 41000),
    "United States":  ("USA", 90, 63000),
}

years = list(range(2005, 2021))
records = []

for country, (code, base_internet, base_gdp) in OECD_BASE.items():
    # Internet usage grows from ~30-70% in 2005 to base_internet in 2020
    start_internet = max(10, base_internet - np.random.uniform(25, 50))
    for i, year in enumerate(years):
        t = i / (len(years) - 1)
        # Logistic-like growth for internet
        internet = start_internet + (base_internet - start_internet) * (t ** 0.6)
        internet += np.random.normal(0, 0.8)
        internet = np.clip(internet, 5, 99)
        
        # GDP grows with some noise and a 2009 crisis dip
        gdp_growth = 1 + np.random.normal(0.025, 0.02)
        if year == 2009:
            gdp_growth -= np.random.uniform(0.04, 0.10)
        elif year == 2010:
            gdp_growth += np.random.uniform(0.01, 0.04)
        
        gdp_start = base_gdp * (0.65 + np.random.uniform(-0.05, 0.05))
        gdp = gdp_start * (gdp_growth ** i)
        gdp += np.random.normal(0, gdp * 0.02)
        gdp = max(gdp, 1000)
        
        records.append({
            "country": country,
            "country_code": code,
            "year": year,
            "internet_usage_pct": round(internet, 2),
            "gdp_per_capita_usd": round(gdp, 2)
        })

df = pd.DataFrame(records)
df.sort_values(["country", "year"], inplace=True)
df.to_csv("data/processed/oecd_internet_gdp.csv", index=False)
print(f"Generated {len(df)} rows for {df['country'].nunique()} countries (2005-2020)")
print(df.head())
