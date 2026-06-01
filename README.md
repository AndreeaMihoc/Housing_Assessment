# HousingAnywhere — Madrid Market Analysis

## Overview
A data analysis project examining the performance of HousingAnywhere's Madrid rental marketplace over a three-year period (2023–2025).

This project was completed as part of a Senior Data Analyst technical assessment and covers demand analysis, revenue trends, seasonality patterns, supply dynamics, and pricing insights.

---

## The Story
Madrid is attracting more visitors every year but the platform is losing them at every step of the funnel.

While revenue grew +37% between 2023 and 2025, booking growth was only +17%. Supply grew +75% but listing utilisation declined from 42.7% to 28.5%. Rising rents (+20.8%) may be pricing out the core tenant audience of international students and young professionals.

---

## Data Sources
Four CSV datasets covering Madrid and Berlin (2023–2025):

| File | Contents |
|---|---|
| `data_demand.csv` | Visitors, Searchers, Applicants |
| `data_key_outcomes.csv` | Bookings, Revenue |
| `data_monetisation.csv` | Commission rate, Booking fee, Avg rent |
| `data_supply.csv` | Available listings, Created listings |

---

## Methodology
- **SQL** used to join all four datasets on composite key 
  (city + month + landlord_type + listing_type)
- **Python** (pandas, matplotlib) for data analysis and visualisations
- **Jupyter Notebook** for end-to-end analysis and storytelling

---

## Key Findings

### 🔻 Funnel Leakage
Visitors grew +58% but bookings only grew +17%.
The platform loses a growing proportion of visitors at every funnel step.

### 📈 Revenue Growing Faster Than Bookings
Revenue grew +37% vs bookings +17%.
Revenue per booking increased from €203 to €238 driven by apartments and rising rents.

### 📅 Academic Calendar Seasonality
Demand peaks in January/February and September/October.
Summer months show a paradox (highest visitors but lowest bookings).

### 🏠 Supply Growing But Utilisation Declining
Available listings grew +75% but utilisation dropped from 42.7% to 28.5%.
Many new listings are not converting into bookings.

### 💶 Rising Rents Creating Affordability Gap
Average rent rose from €1,099 to €1,327 (+20.8%) in two years.
Apartments now average €2,043/month — potentially pricing out the core student audience.

---

## Recommendations

1. **Improve listing quality:** introduce a listing quality score and prioritise high-scoring listings in search results
2. **Align campaigns with academic calendar:** target landlord acquisition in May-July ahead of September peak
3. **Address affordability:** introduce budget-friendly listing categories or incentivise competitive pricing

---

## Files
- `madrid_analysis.ipynb` — full Python notebook with SQL queries, analysis and visualisations
- `HousingAnywhere_Madrid_Data.xlsx` — joined dataset (5 sheets)

---

## Tools Used
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=flat)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=flat&logo=mysql&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat&logo=jupyter&logoColor=white)

---
