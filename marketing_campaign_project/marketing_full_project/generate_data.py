"""
Marketing Campaign Performance Analysis
Step 1: Generate Synthetic Dataset
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(42)
random.seed(42)

N = 1000
CHANNELS   = ['Email', 'Social Media', 'Google Ads', 'Influencer', 'SEO']
CAMPAIGNS  = ['Summer Sale', 'Black Friday', 'New Year', 'Spring Launch', 'Brand Awareness']
REGIONS    = ['North', 'South', 'East', 'West', 'Central']
AUDIENCES  = ['18-24', '25-34', '35-44', '45-54', '55+']

start = datetime(2024, 1, 1)
dates = [start + timedelta(days=random.randint(0, 364)) for _ in range(N)]

ch_probs   = [0.22, 0.28, 0.25, 0.13, 0.12]
channels   = np.random.choice(CHANNELS,   N, p=ch_probs)
campaigns  = np.random.choice(CAMPAIGNS,  N)
regions    = np.random.choice(REGIONS,    N)
audiences  = np.random.choice(AUDIENCES,  N)

budget_map = {
    'Email':        (500,   3_000),
    'Social Media': (1_000, 8_000),
    'Google Ads':   (2_000,15_000),
    'Influencer':   (3_000,20_000),
    'SEO':          (800,   5_000),
}
budgets = [random.randint(*budget_map[c]) for c in channels]

impressions = [int(b * random.uniform(50, 300)) for b in budgets]

ctr_map = {'Email': 0.15, 'Social Media': 0.06, 'Google Ads': 0.04, 'Influencer': 0.08, 'SEO': 0.05}
clicks = [max(1, int(imp * (ctr_map[c] + np.random.normal(0, 0.01)))) for imp, c in zip(impressions, channels)]

cvr_map = {'Email': 0.08, 'Social Media': 0.04, 'Google Ads': 0.06, 'Influencer': 0.05, 'SEO': 0.07}
conversions = [max(0, int(cl * (cvr_map[c] + np.random.normal(0, 0.005)))) for cl, c in zip(clicks, channels)]

revenue = [round(conv * random.uniform(40, 250), 2) for conv in conversions]

df = pd.DataFrame({
    'Date':        dates,
    'Channel':     channels,
    'Campaign':    campaigns,
    'Region':      regions,
    'Audience':    audiences,
    'Budget':      budgets,
    'Impressions': impressions,
    'Clicks':      clicks,
    'Conversions': conversions,
    'Revenue':     revenue,
})

df['CTR']      = (df['Clicks']      / df['Impressions'] * 100).round(2)
df['CVR']      = (df['Conversions'] / df['Clicks']      * 100).round(2)
df['CPC']      = (df['Budget']      / df['Clicks']).round(2)
df['ROAS']     = (df['Revenue']     / df['Budget']).round(2)
df['ROI']      = ((df['Revenue'] - df['Budget']) / df['Budget'] * 100).round(1)
df['Month']    = pd.to_datetime(df['Date']).dt.strftime('%b')
df['Month_Num']= pd.to_datetime(df['Date']).dt.month
df['Quarter']  = pd.to_datetime(df['Date']).dt.quarter.map({1:'Q1',2:'Q2',3:'Q3',4:'Q4'})
df = df.sort_values('Date').reset_index(drop=True)

os.makedirs('data', exist_ok=True)
df.to_csv('data/marketing_data.csv', index=False)
print(f"✅  Dataset created: {df.shape[0]} rows × {df.shape[1]} columns")
print(df.head(3).to_string())
