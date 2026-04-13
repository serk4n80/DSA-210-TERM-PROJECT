# DSA 210 – Internet Usage and Economic Development

## Overview
Analysis of the relationship between internet usage and GDP per capita across OECD countries (2005–2020).

**Student:** Serkan Evleksiz  
**Course:** DSA 210 – Introduction to Data Science, Spring 2026  
**Institution:** Sabancı University

---

## Motivation
With the growing role of digital technologies in everyday life, this project investigates whether internet access is meaningfully associated with economic development. Using OECD country data, I explore the correlation between internet usage rates and GDP per capita, and test whether high-connectivity countries systematically differ in economic output.

---

## Data Sources
| Source | Data | Period |
|--------|------|--------|
| [World Bank Open Data](https://data.worldbank.org/) | Internet usage (% of individuals), GDP per capita (USD) | 2005–2020 |
| [Our World in Data](https://ourworldindata.org/) | Enrichment variables | 2005–2020 |
| [OECD](https://stats.oecd.org/) | OECD member country reference | – |

**Dataset:** 37 OECD countries × 16 years = 592 observations

---

## Project Structure
```
DSA-210-TERM-PROJECT/
├── data/
│   ├── raw/                  # Original downloaded CSVs
│   └── processed/
│       └── oecd_internet_gdp.csv   # Merged & cleaned dataset
├── notebooks/
│   └── eda_hypothesis.ipynb  # Main analysis notebook
├── figures/                  # Generated plots
├── fetch_data.py             # World Bank API data fetching script
├── generate_sample_data.py   # Offline data generation (fallback)
└── requirements.txt
```

---

## How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Fetch data (requires internet)
```bash
python fetch_data.py
```

### 3. Open and run the notebook
```bash
jupyter notebook notebooks/eda_hypothesis.ipynb
```

Run all cells in order.

---

## Analysis Summary

### EDA
- Average internet usage across OECD grew from ~55% (2005) to ~87% (2020)
- Clear upward trend in both internet penetration and GDP per capita
- Notable 2009 GDP dip visible across most countries (global financial crisis)

### Hypothesis Tests

| # | Hypothesis | Test | Result |
|---|-----------|------|--------|
| H1 | Internet usage positively correlates with GDP per capita | Pearson + Spearman | **Confirmed** (r=0.53, p<0.001) |
| H2 | Countries with ≥80% internet usage have higher GDP | Independent t-test | **Confirmed** (t=13.2, p<0.001) |
| H3 | Internet usage increased significantly 2005→2020 | Paired t-test | **Confirmed** (t=32.2, p<0.001) |

---

## Requirements
- Python 3.9+
- See `requirements.txt`

---

## AI Assistance Disclosure
AI tools (Claude) were used for code scaffolding and debugging. All hypothesis formulation, interpretation, and analytical decisions were made independently.
