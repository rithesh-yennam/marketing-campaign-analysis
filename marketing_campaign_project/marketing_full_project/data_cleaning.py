"""
Marketing Campaign Performance Analysis
Step: Data Cleaning & Preprocessing
Dataset: UCI Bank Marketing (41,188 records)
Author: Rithesh Yennam
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os, warnings
warnings.filterwarnings('ignore')

os.makedirs('data', exist_ok=True)
os.makedirs('outputs', exist_ok=True)

print("=" * 60)
print("  DATA CLEANING & PREPROCESSING PIPELINE")
print("=" * 60)

# ── STEP 1: Load Raw Data ─────────────────────────────────────────
print("\n[STEP 1] Loading raw data...")
df_raw = pd.read_csv('data/bank_marketing.csv', sep=';')
print(f"  Raw shape: {df_raw.shape[0]:,} rows x {df_raw.shape[1]} columns")
print(f"  Columns: {list(df_raw.columns)}")

# ── STEP 2: Inspect Missing Values ───────────────────────────────
print("\n[STEP 2] Checking for missing values...")
missing = df_raw.isnull().sum()
pct_missing = (missing / len(df_raw) * 100).round(2)
missing_df = pd.DataFrame({'Missing Count': missing, 'Missing %': pct_missing})
missing_df = missing_df[missing_df['Missing Count'] > 0]
if missing_df.empty:
    print("  No null values found in dataset.")
else:
    print(missing_df)

# Check for 'unknown' values which act as implicit missing values
print("\n  Checking for 'unknown' category (implicit missing values):")
cat_cols = df_raw.select_dtypes(include='object').columns
for col in cat_cols:
    unknown_count = (df_raw[col] == 'unknown').sum()
    if unknown_count > 0:
        pct = unknown_count / len(df_raw) * 100
        print(f"    {col:<20} {unknown_count:>5} unknowns ({pct:.1f}%)")

# ── STEP 3: Handle 'unknown' Values ──────────────────────────────
print("\n[STEP 3] Handling unknown values...")
df = df_raw.copy()

# Replace 'unknown' with NaN for numeric-like categoricals, mode for others
unknown_cols = ['job', 'marital', 'education', 'default', 'housing', 'loan']
for col in unknown_cols:
    unknown_count = (df[col] == 'unknown').sum()
    if unknown_count > 0:
        mode_val = df[df[col] != 'unknown'][col].mode()[0]
        df[col] = df[col].replace('unknown', mode_val)
        print(f"  '{col}': replaced {unknown_count} unknowns with mode ('{mode_val}')")

# ── STEP 4: Remove Duplicates ─────────────────────────────────────
print("\n[STEP 4] Checking and removing duplicates...")
dup_count = df.duplicated().sum()
print(f"  Duplicate rows found: {dup_count}")
if dup_count > 0:
    df = df.drop_duplicates().reset_index(drop=True)
    print(f"  After removing: {len(df):,} rows")
else:
    print("  No duplicate rows found.")

# ── STEP 5: Data Type Validation ─────────────────────────────────
print("\n[STEP 5] Validating data types...")
print(f"  {'Column':<22} {'Dtype':<12} {'Sample'}")
for col in df.columns:
    sample = str(df[col].iloc[0])[:20]
    print(f"  {col:<22} {str(df[col].dtype):<12} {sample}")

# ── STEP 6: Outlier Detection ─────────────────────────────────────
print("\n[STEP 6] Detecting outliers in numeric columns...")
num_cols = ['age', 'duration', 'campaign', 'pdays', 'previous',
            'emp.var.rate', 'cons.price.idx', 'cons.conf.idx',
            'euribor3m', 'nr.employed']

outlier_summary = []
for col in num_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = df[(df[col] < lower) | (df[col] > upper)][col].count()
    outlier_summary.append({
        'Column': col, 'Q1': round(Q1,2), 'Q3': round(Q3,2),
        'IQR': round(IQR,2), 'Lower Bound': round(lower,2),
        'Upper Bound': round(upper,2), 'Outlier Count': outliers,
        'Outlier %': round(outliers/len(df)*100, 2)
    })
    print(f"  {col:<22} outliers: {outliers:>4} ({outliers/len(df)*100:.1f}%)")

outlier_df = pd.DataFrame(outlier_summary)
outlier_df.to_csv('data/outlier_report.csv', index=False)

# Cap duration outliers (calls > 99th percentile are likely data errors)
duration_cap = df['duration'].quantile(0.99)
df['duration_capped'] = df['duration'].clip(upper=duration_cap)
print(f"\n  Capped 'duration' outliers at {duration_cap:.0f}s (99th percentile)")

# ── STEP 7: Feature Engineering ──────────────────────────────────
print("\n[STEP 7] Feature transformation & engineering...")

# Age groups
df['age_group'] = pd.cut(
    df['age'], bins=[17, 25, 35, 45, 55, 65, 100],
    labels=['18-25', '26-35', '36-45', '46-55', '56-65', '65+']
)
print("  [OK] Created 'age_group' feature")

# Call duration buckets
df['duration_category'] = pd.cut(
    df['duration_capped'],
    bins=[0, 60, 180, 300, 600, 99999],
    labels=['Very Short (<1min)', 'Short (1-3min)',
            'Medium (3-5min)', 'Long (5-10min)', 'Very Long (>10min)']
)
print("  [OK] Created 'duration_category' feature")

# Contact season
month_to_season = {
    'dec': 'Winter', 'jan': 'Winter', 'feb': 'Winter',
    'mar': 'Spring', 'apr': 'Spring', 'may': 'Spring',
    'jun': 'Summer', 'jul': 'Summer', 'aug': 'Summer',
    'sep': 'Autumn', 'oct': 'Autumn', 'nov': 'Autumn'
}
df['season'] = df['month'].map(month_to_season)
print("  [OK] Created 'season' feature from month")

# Was previously contacted?
df['previously_contacted'] = (df['pdays'] != 999).astype(int)
print("  [OK] Created 'previously_contacted' binary feature (pdays != 999)")

# Campaign intensity bucket
df['campaign_intensity'] = pd.cut(
    df['campaign'], bins=[0, 1, 3, 6, 100],
    labels=['Single', 'Low (2-3)', 'Medium (4-6)', 'High (7+)']
)
print("  [OK] Created 'campaign_intensity' feature")

# Binary target
df['subscribed'] = (df['y'] == 'yes').astype(int)
print("  [OK] Created binary 'subscribed' target column")

# ── STEP 8: Final Clean Dataset ───────────────────────────────────
print("\n[STEP 8] Saving cleaned dataset...")
df.to_csv('data/bank_marketing_clean.csv', index=False)
print(f"  Cleaned dataset: {df.shape[0]:,} rows x {df.shape[1]} columns")
print(f"  Saved to: data/bank_marketing_clean.csv")

# Cleaning summary
summary = pd.DataFrame({
    'Step': [
        'Raw dataset',
        'After handling unknowns',
        'After removing duplicates',
        'After feature engineering',
    ],
    'Rows': [
        df_raw.shape[0],
        df_raw.shape[0],
        len(df),
        len(df),
    ],
    'Columns': [
        df_raw.shape[1],
        df_raw.shape[1],
        df_raw.shape[1],
        df.shape[1],
    ],
    'Note': [
        'Raw input',
        'Replaced unknowns with mode',
        f'{dup_count} duplicates removed',
        '6 new features added',
    ]
})
summary.to_csv('data/cleaning_summary.csv', index=False)

# ── VISUALISE: Before/After Cleaning ─────────────────────────────
BG    = '#0D1117'
PANEL = '#161B22'
BORDER= '#30363D'
TEXT  = '#E6EDF3'
MUTED = '#8B949E'
ACCENT= '#58A6FF'
GREEN = '#3FB950'

fig = plt.figure(figsize=(22, 12), facecolor=BG)
fig.suptitle('Data Cleaning & Feature Engineering Report',
             fontsize=17, fontweight='bold', color=TEXT, y=0.98,
             fontfamily='monospace')
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.38,
                       left=0.06, right=0.97, top=0.91, bottom=0.07)

def sax(ax, grid_axis='y'):
    ax.set_facecolor(PANEL)
    ax.tick_params(colors=MUTED, labelsize=9)
    ax.xaxis.label.set_color(MUTED)
    ax.yaxis.label.set_color(MUTED)
    ax.title.set_color(TEXT)
    for sp in ax.spines.values(): sp.set_color(BORDER)
    ax.grid(color=BORDER, lw=0.5, alpha=0.8, axis=grid_axis)
    ax.set_axisbelow(True)

# Unknown values per column
ax1 = fig.add_subplot(gs[0, 0])
sax(ax1, 'x')
unknowns = {col: (df_raw[col]=='unknown').sum()
            for col in cat_cols if (df_raw[col]=='unknown').sum()>0}
ax1.barh(list(unknowns.keys()), list(unknowns.values()),
         color=ACCENT, edgecolor='none', height=0.6)
ax1.set_title("'unknown' Values per Column", fontweight='bold', fontsize=11)
ax1.set_xlabel('Count')

# Age distribution before/after grouping
ax2 = fig.add_subplot(gs[0, 1])
sax(ax2)
ax2.hist(df_raw['age'], bins=30, color=ACCENT, alpha=0.7, edgecolor='none', label='Raw age')
ax2.set_title('Age Distribution (Raw)', fontweight='bold', fontsize=11)
ax2.set_xlabel('Age'); ax2.set_ylabel('Count')

ax3 = fig.add_subplot(gs[0, 2])
sax(ax3)
age_grp_counts = df['age_group'].value_counts().sort_index()
ax3.bar(age_grp_counts.index, age_grp_counts.values,
        color=GREEN, edgecolor='none', width=0.6)
ax3.set_title('After: Age Groups (Feature Engineering)', fontweight='bold', fontsize=11)
ax3.set_xlabel('Age Group'); ax3.set_ylabel('Count')
ax3.tick_params(axis='x', rotation=20)

# Duration before/after capping
ax4 = fig.add_subplot(gs[1, 0])
sax(ax4)
ax4.hist(df_raw['duration'], bins=50, color='#F85149', alpha=0.6,
         edgecolor='none', label='Before')
ax4.axvline(duration_cap, color=GREEN, lw=1.5, ls='--', label=f'Cap={duration_cap:.0f}s')
ax4.set_title('Duration: Before Outlier Capping', fontweight='bold', fontsize=11)
ax4.set_xlabel('Duration (seconds)'); ax4.set_ylabel('Count')
ax4.legend(fontsize=8, facecolor=PANEL, edgecolor=BORDER, labelcolor=TEXT)

# Duration categories
ax5 = fig.add_subplot(gs[1, 1])
sax(ax5)
dur_cat = df['duration_category'].value_counts()
colors_d = ['#F85149','#D29922','#58A6FF','#3FB950','#BC8CFF']
ax5.bar(range(len(dur_cat)), dur_cat.values, color=colors_d, edgecolor='none', width=0.6)
ax5.set_xticks(range(len(dur_cat)))
ax5.set_xticklabels([str(l) for l in dur_cat.index], rotation=20, fontsize=8)
ax5.set_title('After: Duration Categories', fontweight='bold', fontsize=11)
ax5.set_ylabel('Count')

# New features summary
ax6 = fig.add_subplot(gs[1, 2])
ax6.set_facecolor(PANEL)
for sp in ax6.spines.values(): sp.set_color(BORDER)
ax6.set_xticks([]); ax6.set_yticks([])
ax6.set_title('New Features Added', fontweight='bold', fontsize=11, color=TEXT)
new_feats = [
    ('age_group',             'Age bucketed into 6 groups'),
    ('duration_category',     'Call length 5-tier bucket'),
    ('season',                'Month -> Spring/Summer/etc'),
    ('previously_contacted',  'Binary: pdays != 999'),
    ('campaign_intensity',    'Contact frequency tier'),
    ('subscribed',            'Binary target (y=yes)'),
    ('duration_capped',       'Duration capped at 99th pct'),
]
for i, (feat, desc) in enumerate(new_feats):
    y_pos = 0.88 - i * 0.12
    ax6.add_patch(plt.Rectangle((0.01, y_pos-0.045), 0.98, 0.09,
                  facecolor=BORDER, edgecolor='none', transform=ax6.transAxes))
    ax6.text(0.05, y_pos, feat, transform=ax6.transAxes,
             color=ACCENT, fontsize=9, fontweight='bold', va='center')
    ax6.text(0.55, y_pos, desc, transform=ax6.transAxes,
             color=MUTED, fontsize=8, va='center')

plt.savefig('outputs/data_cleaning.png', dpi=150,
            bbox_inches='tight', facecolor=BG)
print("[OK] Saved: outputs/data_cleaning.png")
print("\n[DONE] Data cleaning complete!")
