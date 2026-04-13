"""
fetch_data.py
Downloads internet usage and GDP per capita data for OECD countries
from the World Bank API and saves raw CSVs to data/raw/
"""

import requests
import pandas as pd
import os

RAW_DIR = "data/raw"
os.makedirs(RAW_DIR, exist_ok=True)

# OECD country codes (38 members)
OECD_COUNTRIES = [
    "AUS","AUT","BEL","CAN","CHL","COL","CRI","CZE","DNK","EST",
    "FIN","FRA","DEU","GRC","HUN","ISL","IRL","ISR","ITA","JPN",
    "KOR","LVA","LTU","LUX","MEX","NLD","NZL","NOR","POL","PRT",
    "SVK","SVN","ESP","SWE","CHE","TUR","GBR","USA"
]

START_YEAR = 2005
END_YEAR = 2020

def fetch_worldbank(indicator, countries, start, end):
    """Fetch data from World Bank API for given indicator and countries."""
    country_str = ";".join(countries)
    url = (
        f"https://api.worldbank.org/v2/country/{country_str}/indicator/{indicator}"
        f"?date={start}:{end}&format=json&per_page=10000"
    )
    print(f"Fetching {indicator}...")
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    
    if len(data) < 2 or not data[1]:
        print(f"  No data returned for {indicator}")
        return pd.DataFrame()
    
    records = []
    for item in data[1]:
        records.append({
            "country": item["country"]["value"],
            "country_code": item["countryiso3code"],
            "year": int(item["date"]),
            "value": item["value"]
        })
    
    df = pd.DataFrame(records)
    df = df.dropna(subset=["value"])
    print(f"  Got {len(df)} records")
    return df


def main():
    # 1. Internet usage (% of individuals using internet)
    df_internet = fetch_worldbank("IT.NET.USER.ZS", OECD_COUNTRIES, START_YEAR, END_YEAR)
    df_internet.rename(columns={"value": "internet_usage_pct"}, inplace=True)
    df_internet.to_csv(f"{RAW_DIR}/internet_usage.csv", index=False)
    print(f"  Saved internet_usage.csv ({len(df_internet)} rows)")

    # 2. GDP per capita (current USD)
    df_gdp = fetch_worldbank("NY.GDP.PCAP.CD", OECD_COUNTRIES, START_YEAR, END_YEAR)
    df_gdp.rename(columns={"value": "gdp_per_capita_usd"}, inplace=True)
    df_gdp.to_csv(f"{RAW_DIR}/gdp_per_capita.csv", index=False)
    print(f"  Saved gdp_per_capita.csv ({len(df_gdp)} rows)")

    # 3. Merge datasets
    df_merged = pd.merge(
        df_internet[["country", "country_code", "year", "internet_usage_pct"]],
        df_gdp[["country_code", "year", "gdp_per_capita_usd"]],
        on=["country_code", "year"],
        how="inner"
    )
    df_merged.sort_values(["country", "year"], inplace=True)
    df_merged.to_csv("data/processed/oecd_internet_gdp.csv", index=False)
    print(f"\nMerged dataset: {len(df_merged)} rows, {df_merged['country'].nunique()} countries")
    print("Saved to data/processed/oecd_internet_gdp.csv")
    print("\nDone!")


if __name__ == "__main__":
    main()
