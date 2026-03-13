"""
Marketing Campaign Performance Analysis
Step 2: EDA, KPI Computation & Insight Extraction
"""
import pandas as pd
import numpy as np
import os

df = pd.read_csv('data/marketing_data.csv')
df['Date'] = pd.to_datetime(df['Date'])

os.makedirs('data', exist_ok=True)
os.makedirs('outputs', exist_ok=True)

# ── Overall KPIs ─────────────────────────────────────────────────
total_spend       = df['Budget'].sum()
total_revenue     = df['Revenue'].sum()
total_impressions = df['Impressions'].sum()
total_clicks      = df['Clicks'].sum()
total_conversions = df['Conversions'].sum()
overall_roas      = total_revenue / total_spend
overall_roi       = (total_revenue - total_spend) / total_spend * 100
avg_ctr           = total_clicks / total_impressions * 100
avg_cvr           = total_conversions / total_clicks * 100
avg_cpc           = total_spend / total_clicks

print("=" * 60)
print("  OVERALL KPI SUMMARY")
print("=" * 60)
print(f"  Total Spend:          ${total_spend:>12,.0f}")
print(f"  Total Revenue:        ${total_revenue:>12,.0f}")
print(f"  Total Impressions:     {total_impressions:>12,.0f}")
print(f"  Total Clicks:          {total_clicks:>12,.0f}")
print(f"  Total Conversions:     {total_conversions:>12,.0f}")
print(f"  Overall ROAS:          {overall_roas:>12.2f}x")
print(f"  Overall ROI:           {overall_roi:>11.1f}%")
print(f"  Avg CTR:               {avg_ctr:>11.2f}%")
print(f"  Avg CVR:               {avg_cvr:>11.2f}%")
print(f"  Avg CPC:               ${avg_cpc:>11.2f}")

# ── Channel Summary ───────────────────────────────────────────────
ch = df.groupby('Channel').agg(
    Campaigns   =('Campaign','count'),
    Spend       =('Budget','sum'),
    Revenue     =('Revenue','sum'),
    Impressions =('Impressions','sum'),
    Clicks      =('Clicks','sum'),
    Conversions =('Conversions','sum'),
).reset_index()
ch['ROAS'] = (ch['Revenue'] / ch['Spend']).round(2)
ch['ROI%'] = ((ch['Revenue'] - ch['Spend']) / ch['Spend'] * 100).round(1)
ch['CTR%'] = (ch['Clicks'] / ch['Impressions'] * 100).round(2)
ch['CVR%'] = (ch['Conversions'] / ch['Clicks'] * 100).round(2)
ch['CPC']  = (ch['Spend'] / ch['Clicks']).round(2)
ch = ch.sort_values('ROAS', ascending=False)
ch.to_csv('data/channel_summary.csv', index=False)

print("\n" + "=" * 60)
print("  CHANNEL PERFORMANCE (sorted by ROAS)")
print("=" * 60)
print(ch[['Channel','Spend','Revenue','ROAS','ROI%','CTR%','CVR%']].to_string(index=False))

# ── Campaign Summary ──────────────────────────────────────────────
camp = df.groupby('Campaign').agg(
    Spend       =('Budget','sum'),
    Revenue     =('Revenue','sum'),
    Conversions =('Conversions','sum'),
).reset_index()
camp['ROAS'] = (camp['Revenue'] / camp['Spend']).round(2)
camp['ROI%'] = ((camp['Revenue'] - camp['Spend']) / camp['Spend'] * 100).round(1)
camp = camp.sort_values('Revenue', ascending=False)
camp.to_csv('data/campaign_summary.csv', index=False)

print("\n" + "=" * 60)
print("  CAMPAIGN PERFORMANCE (sorted by Revenue)")
print("=" * 60)
print(camp.to_string(index=False))

# ── Region Summary ────────────────────────────────────────────────
reg = df.groupby('Region').agg(
    Spend       =('Budget','sum'),
    Revenue     =('Revenue','sum'),
    Conversions =('Conversions','sum'),
).reset_index()
reg['ROI%'] = ((reg['Revenue'] - reg['Spend']) / reg['Spend'] * 100).round(1)
reg['ROAS'] = (reg['Revenue'] / reg['Spend']).round(2)
reg.to_csv('data/region_summary.csv', index=False)

# ── Monthly Trend ─────────────────────────────────────────────────
monthly = df.groupby(['Month_Num','Month']).agg(
    Spend       =('Budget','sum'),
    Revenue     =('Revenue','sum'),
    Conversions =('Conversions','sum'),
    Clicks      =('Clicks','sum'),
    Impressions =('Impressions','sum'),
).reset_index().sort_values('Month_Num')
monthly['ROAS'] = (monthly['Revenue'] / monthly['Spend']).round(2)
monthly['CTR%'] = (monthly['Clicks'] / monthly['Impressions'] * 100).round(2)
monthly.to_csv('data/monthly_trend.csv', index=False)

# ── Quarterly Summary ─────────────────────────────────────────────
quarterly = df.groupby('Quarter').agg(
    Spend   =('Budget','sum'),
    Revenue =('Revenue','sum'),
).reset_index()
quarterly['ROAS'] = (quarterly['Revenue'] / quarterly['Spend']).round(2)
quarterly.to_csv('data/quarterly_summary.csv', index=False)

# ── Top Performing Rows ───────────────────────────────────────────
top10 = df.nlargest(10, 'ROAS')[['Date','Channel','Campaign','Region','Budget','Revenue','ROAS','ROI']]
top10.to_csv('data/top10_campaigns.csv', index=False)

print("\n  All summaries saved to data/")
print("    → channel_summary.csv")
print("    → campaign_summary.csv")
print("    → region_summary.csv")
print("    → monthly_trend.csv")
print("    → quarterly_summary.csv")
print("    → top10_campaigns.csv")
