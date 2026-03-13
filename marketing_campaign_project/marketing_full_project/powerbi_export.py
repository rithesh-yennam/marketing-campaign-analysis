"""
Marketing Campaign Performance Analysis
Step: Power BI Dashboard — Data Export & Setup
Exports clean, pre-aggregated CSVs optimised for Power BI
Author: Rithesh Yennam
"""
import pandas as pd
import numpy as np
import os

os.makedirs('powerbi_data', exist_ok=True)

print("=" * 60)
print("  POWER BI DATA EXPORT")
print("=" * 60)

df = pd.read_csv('data/bank_marketing_clean.csv')
print(f"\n  Source: bank_marketing_clean.csv ({len(df):,} rows)")

# ── TABLE 1: Main Facts Table ─────────────────────────────────────
facts = df[[
    'age', 'age_group', 'job', 'marital', 'education',
    'housing', 'loan', 'contact', 'month', 'day_of_week',
    'duration', 'duration_category', 'campaign', 'campaign_intensity',
    'poutcome', 'season', 'previously_contacted',
    'emp.var.rate', 'cons.price.idx', 'cons.conf.idx',
    'euribor3m', 'subscribed', 'y'
]].copy()
facts.columns = [c.replace('.', '_') for c in facts.columns]
facts.to_csv('powerbi_data/fact_campaign.csv', index=False)
print(f"\n  [OK] fact_campaign.csv          ({len(facts):,} rows, {len(facts.columns)} cols)")

# ── TABLE 2: Campaign Success by Job ─────────────────────────────
job_agg = df.groupby('job').agg(
    Total_Contacts  =('subscribed','count'),
    Subscribed      =('subscribed','sum'),
    Avg_Duration_Sec=('duration','mean'),
).reset_index()
job_agg['Conversion_Rate_Pct'] = (job_agg['Subscribed'] / job_agg['Total_Contacts'] * 100).round(2)
job_agg['Avg_Duration_Sec'] = job_agg['Avg_Duration_Sec'].round(0)
job_agg.to_csv('powerbi_data/dim_job_performance.csv', index=False)
print(f"  [OK] dim_job_performance.csv    ({len(job_agg)} rows)")

# ── TABLE 3: Monthly Campaign Performance ────────────────────────
month_order = ['jan','feb','mar','apr','may','jun',
               'jul','aug','sep','oct','nov','dec']
monthly = df.groupby('month').agg(
    Total_Contacts  =('subscribed','count'),
    Subscribed      =('subscribed','sum'),
    Avg_Duration    =('duration','mean'),
).reset_index()
monthly['Conversion_Rate_Pct'] = (monthly['Subscribed'] / monthly['Total_Contacts'] * 100).round(2)
monthly['Month_Num'] = monthly['month'].map({m:i+1 for i,m in enumerate(month_order)})
monthly['Month_Label'] = monthly['month'].str.capitalize()
monthly = monthly.sort_values('Month_Num')
monthly.to_csv('powerbi_data/dim_monthly_performance.csv', index=False)
print(f"  [OK] dim_monthly_performance.csv ({len(monthly)} rows)")

# ── TABLE 4: Age Group Demographics ──────────────────────────────
age_agg = df.groupby('age_group', observed=True).agg(
    Total      =('subscribed','count'),
    Subscribed =('subscribed','sum'),
    Avg_Age    =('age','mean'),
).reset_index()
age_agg['Conversion_Rate_Pct'] = (age_agg['Subscribed'] / age_agg['Total'] * 100).round(2)
age_agg['Avg_Age'] = age_agg['Avg_Age'].round(1)
age_agg.to_csv('powerbi_data/dim_age_demographics.csv', index=False)
print(f"  [OK] dim_age_demographics.csv   ({len(age_agg)} rows)")

# ── TABLE 5: Education Analysis ───────────────────────────────────
edu_agg = df.groupby('education').agg(
    Total      =('subscribed','count'),
    Subscribed =('subscribed','sum'),
).reset_index()
edu_agg['Conversion_Rate_Pct'] = (edu_agg['Subscribed'] / edu_agg['Total'] * 100).round(2)
edu_agg.to_csv('powerbi_data/dim_education.csv', index=False)
print(f"  [OK] dim_education.csv          ({len(edu_agg)} rows)")

# ── TABLE 6: Call Duration vs Conversion ─────────────────────────
dur_agg = df.groupby('duration_category', observed=True).agg(
    Total      =('subscribed','count'),
    Subscribed =('subscribed','sum'),
).reset_index()
dur_agg['Conversion_Rate_Pct'] = (dur_agg['Subscribed'] / dur_agg['Total'] * 100).round(2)
dur_agg = dur_agg.dropna(subset=['duration_category'])
dur_agg.to_csv('powerbi_data/dim_call_duration.csv', index=False)
print(f"  [OK] dim_call_duration.csv      ({len(dur_agg)} rows)")

# ── TABLE 7: Previous Campaign Outcome ───────────────────────────
pout_agg = df.groupby('poutcome').agg(
    Total      =('subscribed','count'),
    Subscribed =('subscribed','sum'),
).reset_index()
pout_agg['Conversion_Rate_Pct'] = (pout_agg['Subscribed'] / pout_agg['Total'] * 100).round(2)
pout_agg.to_csv('powerbi_data/dim_prev_outcome.csv', index=False)
print(f"  [OK] dim_prev_outcome.csv       ({len(pout_agg)} rows)")

# ── TABLE 8: KPI Summary Card ─────────────────────────────────────
kpi = pd.DataFrame([{
    'Total_Contacts':     len(df),
    'Total_Subscribed':   df['subscribed'].sum(),
    'Overall_Conv_Rate':  round(df['subscribed'].mean()*100, 2),
    'Avg_Call_Duration':  round(df['duration'].mean(), 0),
    'Pct_Previously_Contacted': round(df['previously_contacted'].mean()*100, 2),
    'Success_Prev_Campaign_Pct': round(
        df[df['poutcome']=='success']['subscribed'].mean()*100, 2),
}])
kpi.to_csv('powerbi_data/kpi_summary.csv', index=False)
print(f"  [OK] kpi_summary.csv            (KPI card values)")

print(f"\n  All files saved to powerbi_data/")
print("\n" + "=" * 60)
print("  POWER BI DASHBOARD SETUP GUIDE")
print("=" * 60)
print("""
HOW TO BUILD THE POWER BI DASHBOARD:

1. IMPORT DATA
   - Open Power BI Desktop
   - Click: Get Data > Text/CSV
   - Import all 8 CSV files from powerbi_data/ folder
   - Load each one

2. RECOMMENDED VISUALS TO CREATE:

   PAGE 1 — CAMPAIGN OVERVIEW
   - KPI Cards (from kpi_summary.csv):
       * Total Contacts
       * Total Subscriptions
       * Overall Conversion Rate %
       * Avg Call Duration
   - Donut Chart: Subscribed vs Not Subscribed (y column)
   - Bar Chart: Conversion Rate by Job (dim_job_performance.csv)

   PAGE 2 — CUSTOMER DEMOGRAPHICS
   - Clustered Bar: Age Group vs Conversion Rate (dim_age_demographics.csv)
   - Bar Chart: Education Level vs Conversion Rate (dim_education.csv)
   - Stacked Bar: Housing Loan + Personal Loan split (fact_campaign.csv)
   - Slicer: Filter by marital status / season

   PAGE 3 — CAMPAIGN PERFORMANCE
   - Line Chart: Monthly Contacts + Conversion % (dim_monthly_performance.csv)
   - Bar Chart: Call Duration Category vs Conversion (dim_call_duration.csv)
   - Bar Chart: Previous Campaign Outcome Impact (dim_prev_outcome.csv)
   - Slicer: Filter by contact type (telephone vs cellular)

   PAGE 4 — PURCHASE BEHAVIOR
   - Scatter Chart: Duration vs Age (from fact_campaign.csv)
   - Treemap: Subscriptions by Job + Education
   - Bar: Campaign Intensity vs Conversion Rate

3. COLOUR THEME
   Use the following hex codes for a professional look:
   - Primary:    #1B2A4A  (navy)
   - Accent:     #2563EB  (blue)
   - Success:    #16A34A  (green)
   - Warning:    #D97706  (amber)
   - Background: #F8FAFC  (off-white)

4. DAX MEASURES TO ADD (in Power BI):
   Conversion Rate =
       DIVIDE(SUM(fact_campaign[subscribed]), COUNT(fact_campaign[subscribed]))

   Subscription Count =
       COUNTROWS(FILTER(fact_campaign, fact_campaign[y] = "yes"))

   Avg Call Duration (mins) =
       AVERAGE(fact_campaign[duration]) / 60
""")
print("[DONE] Power BI export complete!")
