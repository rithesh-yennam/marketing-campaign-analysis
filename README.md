# Marketing Campaign Performance Analysis

**By Rithesh Yennam**

![Python](https://img.shields.io/badge/Python-3.9+-blue) ![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-green) ![MySQL](https://img.shields.io/badge/MySQL-SQL%20Analysis-orange) ![Scikit--learn](https://img.shields.io/badge/Scikit--learn-ML-red) ![PowerBI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow) ![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-purple)

---

## About This Project

I built this project to analyze marketing campaign performance using real-world and synthetic data. The goal was to understand which channels, campaigns, and customer segments drive the best results — and to build machine learning models that can predict customer subscription behavior.

This project covers the complete data analytics workflow:
- Data cleaning & preprocessing
- MySQL / SQL analysis & customer segmentation
- KPI computation & visualization
- Machine learning classification models
- Power BI dashboard reporting

---

## What I Did

- Cleaned and preprocessed 41,188 real bank client records — handled unknown values, removed duplicates, detected outliers, and engineered 6 new features
- Wrote 12 SQL queries in MySQL for customer segmentation, campaign response analysis, and aggregation reporting
- Generated a synthetic marketing dataset with 1,000 campaign records across 5 channels and 5 regions
- Computed key marketing KPIs: ROAS, ROI, CTR, CVR, CPC
- Built multi-panel executive dashboards using Matplotlib
- Trained and compared 3 ML classification models — Random Forest achieved AUC 0.95
- Exported 8 clean CSV files formatted for Power BI dashboard building

---

## Tools & Technologies

| Tool | Purpose |
|---|---|
| Python | Core programming language |
| Pandas & NumPy | Data wrangling and feature engineering |
| MySQL / SQL | Customer segmentation and aggregation queries |
| Matplotlib | Dashboard and chart creation |
| Scikit-learn | Machine learning models and evaluation |
| Power BI | Interactive campaign performance dashboard |

---

## Project Structure

```
marketing-campaign-analysis/
|
|-- run_all.py                <- Runs the full pipeline in one command
|
|-- data_cleaning.py          <- Step 1: Data cleaning & feature engineering
|-- sql_analysis.py           <- Step 2: MySQL queries on real dataset
|-- sql_queries.sql           <- Step 2: Pure SQL script (12 queries)
|-- generate_data.py          <- Step 3: Synthetic dataset generation
|-- analysis.py               <- Step 4: KPI calculations and summaries
|-- visualize.py              <- Step 5: Marketing dashboard charts
|-- bank_analysis.py          <- Step 6: EDA on bank dataset
|-- bank_visualize.py         <- Step 7: Bank campaign visualizations
|-- bank_ml.py                <- Step 8: ML model training and evaluation
|-- powerbi_export.py         <- Step 9: Exports data for Power BI
|
|-- data/
|   |-- bank_marketing.csv         <- Raw UCI bank dataset (41,188 records)
|   |-- bank_marketing_clean.csv   <- Cleaned dataset after Step 1
|   |-- marketing_data.csv         <- Synthetic marketing data
|   |-- outlier_report.csv         <- IQR outlier detection results
|   |-- cleaning_summary.csv       <- Before/after cleaning summary
|   |-- sql_q1_overall.csv         <- SQL query results
|   |-- sql_q2_education.csv
|   |-- sql_q3_job.csv
|   |-- sql_q4_monthly.csv
|   |-- bank_model_results.csv
|   |-- bank_feature_importance.csv
|
|-- powerbi_data/
|   |-- fact_campaign.csv          <- Main 41K row fact table for Power BI
|   |-- dim_job_performance.csv
|   |-- dim_monthly_performance.csv
|   |-- dim_age_demographics.csv
|   |-- dim_education.csv
|   |-- dim_call_duration.csv
|   |-- dim_prev_outcome.csv
|   |-- kpi_summary.csv
|
|-- outputs/
    |-- data_cleaning.png          <- Cleaning report charts
    |-- sql_analysis.png           <- SQL results visualized
    |-- dashboard_main.png         <- Marketing KPI dashboard
    |-- channel_efficiency.png     <- Funnel & CTR/CVR charts
    |-- budget_quarterly.png       <- Spend vs revenue
    |-- bank_dashboard.png         <- Bank campaign overview
    |-- bank_deep_dive.png         <- Education & economics analysis
    |-- bank_ml.png                <- ML model results
```

---

## Step 1 — Data Cleaning & Preprocessing

I performed a full 8-step cleaning pipeline on the raw bank marketing dataset:

| Step | Action | Result |
|---|---|---|
| 1 | Load raw data | 41,188 rows x 21 columns |
| 2 | Check null values | No nulls found |
| 3 | Handle unknown values | 12,718 unknowns replaced with column mode |
| 4 | Remove duplicates | 14 duplicate rows removed |
| 5 | Validate data types | All types confirmed correct |
| 6 | Outlier detection (IQR) | Duration capped at 99th percentile (1,271s) |
| 7 | Feature engineering | 6 new features created |
| 8 | Save clean dataset | 41,174 rows x 28 columns |

**New features I engineered:**

| Feature | Description |
|---|---|
| age_group | Age bucketed: 18-25, 26-35, 36-45, 46-55, 56-65, 65+ |
| duration_category | Call length: Very Short / Short / Medium / Long / Very Long |
| season | Month mapped to Spring / Summer / Autumn / Winter |
| previously_contacted | Binary: 1 if client contacted before (pdays != 999) |
| campaign_intensity | Contact frequency: Single / Low / Medium / High |
| subscribed | Binary target: 1 = yes, 0 = no |

---

## Step 2 — SQL Analysis (MySQL)

I wrote 12 SQL queries in MySQL syntax to extract business insights.
All queries are in `sql_queries.sql` and can be run directly in MySQL Workbench.

```sql
-- Q1: Overall Campaign Success Rate
SELECT
    COUNT(*)                                        AS total_contacts,
    SUM(subscribed)                                 AS total_subscribed,
    ROUND(SUM(subscribed) * 100.0 / COUNT(*), 2)   AS success_rate_pct,
    ROUND(AVG(duration), 0)                         AS avg_call_duration_sec
FROM marketing_campaign;

-- Q2: Customer Segmentation by Education
SELECT
    education,
    COUNT(*)                                        AS total_customers,
    SUM(subscribed)                                 AS subscribed,
    ROUND(SUM(subscribed) * 100.0 / COUNT(*), 2)   AS conversion_rate_pct
FROM marketing_campaign
GROUP BY education
ORDER BY conversion_rate_pct DESC;

-- Q3: Campaign Response by Job Category
SELECT
    job,
    COUNT(*)                                        AS total_contacts,
    SUM(subscribed)                                 AS subscribed,
    ROUND(SUM(subscribed) * 100.0 / COUNT(*), 2)   AS conversion_rate_pct,
    ROUND(AVG(duration), 0)                         AS avg_call_sec
FROM marketing_campaign
GROUP BY job
ORDER BY conversion_rate_pct DESC;

-- Q4: Monthly Campaign Performance
SELECT
    month,
    COUNT(*)                                        AS total_contacts,
    SUM(subscribed)                                 AS subscriptions,
    ROUND(SUM(subscribed) * 100.0 / COUNT(*), 2)   AS conversion_pct
FROM marketing_campaign
GROUP BY month
ORDER BY subscriptions DESC;
```

**All 12 queries are in `sql_queries.sql`** — covering job, education, age group,
monthly trends, call duration, previous outcome, season, housing loan, and economic indicators.

---

## Step 3 — Synthetic Marketing Dataset

I generated a realistic 1,000-record marketing dataset using NumPy with real channel behavior patterns.

| Column | Description |
|---|---|
| Channel | Email, Social Media, Google Ads, Influencer, SEO |
| Campaign | Summer Sale, Black Friday, New Year, Spring Launch, Brand Awareness |
| Region | North, South, East, West, Central |
| Budget | Ad spend per campaign |
| Impressions, Clicks, Conversions | Funnel metrics |
| CTR, CVR, CPC, ROAS, ROI | KPIs I calculated |

**What I found:**
- Email had the highest ROAS (292x) with 15% click-through rate
- Google Ads generated the most impressions but at higher cost
- Black Friday and New Year campaigns peaked in Q4

---

## Step 4 — Bank Marketing Dataset (UCI)

**Source:** UCI Machine Learning Repository
**Size:** 41,188 records | **Goal:** Predict if client subscribes to term deposit (yes/no)

| Feature Type | Examples |
|---|---|
| Client demographics | Age, job, marital status, education |
| Campaign details | Contact type, month, call duration |
| Previous contact history | Days since last contact, prior outcome |
| Economic indicators | Euribor rate, employment rate, consumer confidence |

**Key things I discovered:**
- Only 11.3% of clients subscribed — heavily imbalanced dataset
- Call duration is the strongest predictor — under 1 min = 0% conversion, over 10 min = 48%+
- Clients contacted in March, September, October converted 2-3x more than average
- Students (31%) and retired clients (25%) had the highest subscription rates by job
- Previous campaign success leads to 65% conversion on re-contact — 6x the baseline

---

## Step 5 — ML Model Results

I trained 3 models and compared them:

| Model | AUC | Precision | Recall | F1 |
|---|---|---|---|---|
| Logistic Regression | 0.79 | 0.50 | 0.60 | 0.54 |
| **Random Forest** | **0.95** | **0.47** | **0.92** | **0.62** |
| Gradient Boosting | 0.95 | 0.69 | 0.58 | 0.63 |

**Top features by importance:**
1. `duration` — call duration (47% importance)
2. `euribor3m` — 3-month Euribor interest rate
3. `nr_employed` — number of employees (economic indicator)
4. `emp_var_rate` — employment variation rate
5. `age` — client age

---

## Step 6 — Power BI Dashboard

I exported 8 pre-aggregated CSV files to `powerbi_data/` folder for Power BI.

**Dashboard pages I designed:**

| Page | Visuals |
|---|---|
| Campaign Overview | KPI cards, donut chart, conversion by job |
| Customer Demographics | Age group bars, education breakdown, loan filters |
| Campaign Performance | Monthly trend line, duration impact, previous outcome |
| Purchase Behavior | Scatter plot, treemap, campaign intensity analysis |

**DAX Measures I used:**

```
Conversion Rate =
    DIVIDE(SUM(fact_campaign[subscribed]), COUNT(fact_campaign[subscribed]))

Subscription Count =
    COUNTROWS(FILTER(fact_campaign, fact_campaign[y] = "yes"))

Avg Call Duration (mins) =
    AVERAGE(fact_campaign[duration]) / 60
```

---

## How to Run

```bash
# Install required libraries
pip install pandas numpy matplotlib scikit-learn

# For MySQL support (optional)
pip install mysql-connector-python

# Run everything at once
python run_all.py
```

Or run step by step:

```bash
python data_cleaning.py    # Step 1 - Clean & engineer features
python sql_analysis.py     # Step 2 - Run MySQL/SQL queries
python generate_data.py    # Step 3 - Create synthetic dataset
python analysis.py         # Step 4 - Compute KPIs
python visualize.py        # Step 5 - Generate marketing charts
python bank_analysis.py    # Step 6 - Analyse bank dataset
python bank_visualize.py   # Step 7 - Bank visualizations
python bank_ml.py          # Step 8 - Train ML models
python powerbi_export.py   # Step 9 - Export for Power BI
```

**To use MySQL instead of SQLite:**
Open `sql_analysis.py` and update the credentials at the top:
```python
MYSQL_HOST     = 'localhost'
MYSQL_USER     = 'root'
MYSQL_PASSWORD = 'your_password'
MYSQL_DATABASE = 'marketing_campaign_db'
```

---

## Key Business Insights I Derived

1. **Email is the most efficient marketing channel** — highest ROAS (292x) despite the lowest spend
2. **Call quality matters more than quantity** — calls over 10 minutes convert at 48% vs 0% under 1 minute
3. **Students and retirees are underserved segments** — they convert at 2-3x the average rate
4. **Previous campaign success is the best predictor** — re-targeting converts at 65% vs 11% baseline
5. **Economic conditions affect subscriptions** — higher Euribor rates correlate with fewer sign-ups
6. **Q4 campaigns outperform all quarters** — Black Friday and New Year drive 35% of annual revenue
7. **March, September, October are the best months** to run bank campaigns

---

## Output Charts

| Chart | Description |
|---|---|
| data_cleaning.png | 6-panel cleaning report — unknowns, outliers, new features |
| sql_analysis.png | 4 SQL query results visualized |
| dashboard_main.png | Main marketing KPI dashboard |
| channel_efficiency.png | CTR vs CVR, conversion funnel |
| budget_quarterly.png | Spend vs revenue, quarterly breakdown |
| bank_dashboard.png | Bank overview — job, age, month, duration |
| bank_deep_dive.png | Education, prior contact, economic factors |
| bank_ml.png | ROC curves, confusion matrix, feature importance |

---

*Developed by Rithesh Yennam | Data Analytics Portfolio Project*
*Tools: Python, Pandas, MySQL, Scikit-learn, Matplotlib, Power BI*
