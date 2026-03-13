"""
Bank Marketing Campaign — EDA & KPI Analysis
Dataset: UCI Bank Marketing (41,188 records, 21 features)
Target: Predict if client subscribes to term deposit (y = yes/no)
"""
import pandas as pd
import numpy as np
import os

os.makedirs('data', exist_ok=True)

df = pd.read_csv('data/bank_marketing.csv', sep=';')
df['subscribed'] = (df['y'] == 'yes').astype(int)

print("=" * 60)
print("  BANK MARKETING DATASET — SUMMARY")
print("=" * 60)
print(f"  Records:          {len(df):,}")
print(f"  Features:         {df.shape[1]}")
print(f"  Subscribed (yes): {df['subscribed'].sum():,}  ({df['subscribed'].mean()*100:.1f}%)")
print(f"  Not subscribed:   {(1-df['subscribed']).sum():,}  ({(1-df['subscribed']).mean()*100:.1f}%)")

# ── By Job ───────────────────────────────────────────────────────
job = df.groupby('job').agg(
    Total       =('subscribed','count'),
    Subscribed  =('subscribed','sum')
).reset_index()
job['Rate%'] = (job['Subscribed'] / job['Total'] * 100).round(1)
job = job.sort_values('Rate%', ascending=False)
job.to_csv('data/bank_by_job.csv', index=False)
print("\n  Subscription Rate by Job:")
for _, r in job.iterrows():
    print(f"    {r['job']:<20} {r['Rate%']:>5.1f}%  ({r['Subscribed']:,}/{r['Total']:,})")

# ── By Contact Month ─────────────────────────────────────────────
month_order = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
monthly = df.groupby('month').agg(
    Total      =('subscribed','count'),
    Subscribed =('subscribed','sum')
).reset_index()
monthly['Rate%']   = (monthly['Subscribed'] / monthly['Total'] * 100).round(1)
monthly['Month_N'] = monthly['month'].map({m: i for i, m in enumerate(month_order)})
monthly = monthly.sort_values('Month_N')
monthly.to_csv('data/bank_by_month.csv', index=False)

# ── By Age Group ─────────────────────────────────────────────────
df['age_group'] = pd.cut(df['age'], bins=[17,25,35,45,55,65,100],
                         labels=['18-25','26-35','36-45','46-55','56-65','65+'])
age_grp = df.groupby('age_group', observed=True).agg(
    Total      =('subscribed','count'),
    Subscribed =('subscribed','sum')
).reset_index()
age_grp['Rate%'] = (age_grp['Subscribed'] / age_grp['Total'] * 100).round(1)
age_grp.to_csv('data/bank_by_age.csv', index=False)

# ── By Education ─────────────────────────────────────────────────
edu = df.groupby('education').agg(
    Total      =('subscribed','count'),
    Subscribed =('subscribed','sum')
).reset_index()
edu['Rate%'] = (edu['Subscribed'] / edu['Total'] * 100).round(1)
edu = edu.sort_values('Rate%', ascending=False)
edu.to_csv('data/bank_by_education.csv', index=False)

# ── Call Duration Impact ─────────────────────────────────────────
df['duration_bin'] = pd.cut(df['duration'], bins=[0,60,180,300,600,5000],
                             labels=['<1min','1-3min','3-5min','5-10min','>10min'])
dur = df.groupby('duration_bin', observed=True).agg(
    Total      =('subscribed','count'),
    Subscribed =('subscribed','sum')
).reset_index()
dur['Rate%'] = (dur['Subscribed'] / dur['Total'] * 100).round(1)
dur.to_csv('data/bank_by_duration.csv', index=False)
print("\n  Subscription Rate by Call Duration:")
for _, r in dur.iterrows():
    print(f"    {str(r['duration_bin']):<10} {r['Rate%']:>5.1f}%")

print("\n Bank analysis complete — summaries saved to data/")
