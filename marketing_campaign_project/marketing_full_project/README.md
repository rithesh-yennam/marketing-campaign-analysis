# 📊 Marketing Campaign Performance Analysis

**Python · Pandas · Scikit-learn · Matplotlib · Machine Learning**

> End-to-end marketing analytics pipeline with real-world bank campaign data, KPI dashboards, and ML classification models — built for a data analyst portfolio.

---

## Project Overview

This project demonstrates a complete data analytics workflow across two datasets:

1. **Synthetic Marketing Dataset** — 1,000 campaign records across 5 channels, 5 campaigns, and 5 regions (generated with realistic patterns)
2. **UCI Bank Marketing Dataset** — 41,188 real client contact records predicting term deposit subscription

---

## Skills Demonstrated

| Skill | Tools Used |
|---|---|
| Data wrangling & cleaning | Pandas, NumPy |
| KPI computation | ROAS, ROI, CTR, CVR, CPC |
| Exploratory Data Analysis | Groupby, aggregation, segmentation |
| Data visualization | Matplotlib, multi-panel dashboards |
| Machine Learning (Regression) | RandomForest, GradientBoosting |
| Machine Learning (Classification) | LogisticRegression, RandomForest, GradientBoosting |
| Model evaluation | AUC-ROC, Precision-Recall, Confusion Matrix, Cross-validation |
| Feature engineering | Label encoding, binning, date features |

---

## Dataset 1 — Synthetic Marketing Data

| Feature | Description |
|---|---|
| Channel | Email, Social Media, Google Ads, Influencer, SEO |
| Campaign | Summer Sale, Black Friday, New Year, Spring Launch, Brand Awareness |
| Region | North, South, East, West, Central |
| Budget | Ad spend per campaign record |
| Impressions / Clicks / Conversions | Funnel metrics |
| Revenue | Attributed revenue |
| **Derived KPIs** | CTR, CVR, CPC, ROAS, ROI |

**Key Results:**
- Email delivers the highest ROAS (292×) with 15% CTR
- Google Ads drives volume (highest impressions + spend)
- Q4 campaigns (Black Friday / New Year) generate peak revenue

---

## Dataset 2 — Bank Marketing (UCI)

**Source:** UCI Machine Learning Repository — Bank Marketing Dataset  
**Records:** 41,188 client contacts | **Target:** Subscribed to term deposit (yes/no)

| Feature Type | Examples |
|---|---|
| Client info | Age, job, marital status, education |
| Campaign info | Contact type, month, call duration, number of contacts |
| Previous campaign | Days since last contact, previous outcome |
| Economic context | Employment rate, Euribor rate, consumer confidence |

**Key Findings:**
- Overall subscription rate: **11.3%** (heavily imbalanced)
- Longer call duration → dramatically higher conversion (1 min = 5% vs 10+ min = 60%+)
- Clients contacted in **March, September, October** convert at 2–3× the average rate
- Previous campaign **success** → 65% conversion on follow-up
- **Retired** and **students** show highest conversion rates by job category

---

## ML Model Performance (Bank Dataset)

| Model | AUC | Precision | Recall | F1 |
|---|---|---|---|---|
| Logistic Regression | ~0.79 | ~0.50 | ~0.60 | ~0.54 |
| **Random Forest** | **~0.93** | **~0.70** | **~0.55** | **~0.62** |
| Gradient Boosting | ~0.92 | ~0.68 | ~0.57 | ~0.62 |

Top predictors: `duration`, `euribor3m`, `nr.employed`, `poutcome`, `age`

---

## Project Structure

```
marketing-campaign-analysis/
│
├── run_all.py               ← Run this to execute the full pipeline
│
├── generate_data.py         ← Synthetic dataset generation
├── analysis.py              ← Marketing KPI computation & summaries
├── visualize.py             ← Marketing dashboard charts
├── bank_analysis.py         ← Bank dataset EDA
├── bank_visualize.py        ← Bank campaign visualizations
├── bank_ml.py               ← ML classification (3 models)
│
├── data/
│   ├── bank_marketing.csv   ← Raw bank dataset (UCI)
│   ├── marketing_data.csv   ← Generated marketing data
│   ├── channel_summary.csv
│   ├── campaign_summary.csv
│   ├── monthly_trend.csv
│   ├── bank_by_job.csv
│   ├── bank_by_month.csv
│   ├── bank_feature_importance.csv
│   └── bank_model_results.csv
│
└── outputs/
    ├── dashboard_main.png       ← Marketing executive dashboard
    ├── channel_efficiency.png   ← CTR/CVR funnel charts
    ├── budget_quarterly.png     ← Spend vs revenue scatter
    ├── bank_dashboard.png       ← Bank campaign overview
    ├── bank_deep_dive.png       ← Education, economics analysis
    └── bank_ml.png              ← ML model results (ROC, CM, PR)
```

---

## How to Run

```bash
# 1. Install dependencies
pip install pandas numpy matplotlib scikit-learn

# 2. Run the full pipeline (all steps)
python run_all.py

# Or run individual steps:
python generate_data.py    # Create synthetic data
python analysis.py         # Compute KPIs
python visualize.py        # Generate marketing charts
python bank_analysis.py    # Analyse bank dataset
python bank_visualize.py   # Bank visualizations
python bank_ml.py          # Train & evaluate ML models
```

---

## Key Business Insights

1. **Email marketing has 4× better ROAS** than paid channels despite lower spend
2. **Call duration is the #1 predictor** of bank subscription — quality > quantity
3. **Euribor rate inversely correlates** with subscriptions — economic context matters
4. **Previous campaign success** boosts next campaign conversion by 6× (65% vs 11%)
5. **Q4 seasonality** is real — Black Friday and New Year campaigns drive 35% of annual revenue
6. **Retired and student segments** are undercontacted but convert at 2× average rate

---

*Project by [Your Name] · Tools: Python, Pandas, Scikit-learn, Matplotlib*
