"""
Marketing Campaign Performance Analysis
Step 4: Machine Learning — Predict Conversions & ROAS
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score
import warnings, os
warnings.filterwarnings('ignore')

os.makedirs('outputs', exist_ok=True)

BG    = '#0D1117'
PANEL = '#161B22'
TEXT  = '#E6EDF3'
MUTED = '#8B949E'
ACCENT= '#58A6FF'
GREEN = '#3FB950'
BORDER= '#30363D'

df = pd.read_csv('data/marketing_data.csv')
df['Date'] = pd.to_datetime(df['Date'])

# ── Feature engineering ──────────────────────────────────────────
df['DayOfWeek'] = df['Date'].dt.dayofweek
df['IsWeekend'] = (df['DayOfWeek'] >= 5).astype(int)

le = LabelEncoder()
for col in ['Channel', 'Campaign', 'Region', 'Audience', 'Quarter']:
    df[col + '_enc'] = le.fit_transform(df[col])

features = [
    'Budget', 'Impressions', 'Clicks', 'CTR', 'CPC',
    'Month_Num', 'DayOfWeek', 'IsWeekend',
    'Channel_enc', 'Campaign_enc', 'Region_enc', 'Audience_enc',
]

# ── Model 1: Predict Conversions ──────────────────────────────────
X  = df[features]
y1 = df['Conversions']
y2 = df['ROAS']

X_tr, X_te, y1_tr, y1_te = train_test_split(X, y1, test_size=0.2, random_state=42)
_,    _,    y2_tr, y2_te = train_test_split(X, y2, test_size=0.2, random_state=42)

models = {
    'Linear Regression':    LinearRegression(),
    'Random Forest':        RandomForestRegressor(n_estimators=100, random_state=42),
    'Gradient Boosting':    GradientBoostingRegressor(n_estimators=100, random_state=42),
}

print("=" * 58)
print("  MODEL COMPARISON — Predicting Conversions")
print("=" * 58)
results = []
for name, model in models.items():
    model.fit(X_tr, y1_tr)
    preds = model.predict(X_te)
    mae   = mean_absolute_error(y1_te, preds)
    r2    = r2_score(y1_te, preds)
    cv    = cross_val_score(model, X, y1, cv=5, scoring='r2').mean()
    results.append({'Model': name, 'MAE': round(mae,1), 'R²': round(r2,4), 'CV R²': round(cv,4)})
    print(f"  {name:<25}  MAE={mae:>8.1f}  R²={r2:.4f}  CV-R²={cv:.4f}")

best_model = RandomForestRegressor(n_estimators=100, random_state=42)
best_model.fit(X_tr, y1_tr)
best_preds = best_model.predict(X_te)

# ── Feature Importance ────────────────────────────────────────────
importance_df = pd.DataFrame({
    'Feature':   features,
    'Importance': best_model.feature_importances_
}).sort_values('Importance', ascending=False)

print("\n  Top Feature Importances (Random Forest):")
for _, row in importance_df.head(8).iterrows():
    bar = ' ' * int(row['Importance'] * 50)
    print(f"  {row['Feature']:<18} {bar} {row['Importance']:.4f}")

# ── Visualize: Actual vs Predicted + Feature Importance ──────────
fig, axes = plt.subplots(1, 2, figsize=(16, 6), facecolor=BG)
fig.suptitle('ML Model — Conversion Prediction (Random Forest)',
             fontsize=15, fontweight='bold', color=TEXT)

ax1 = axes[0]
ax1.set_facecolor(PANEL)
ax1.scatter(y1_te, best_preds, alpha=0.35, s=25, color=ACCENT, edgecolors='none')
mn, mx = min(y1_te.min(), best_preds.min()), max(y1_te.max(), best_preds.max())
ax1.plot([mn, mx], [mn, mx], color=GREEN, lw=1.5, ls='--', label='Perfect fit')
ax1.set_xlabel('Actual Conversions', color=MUTED)
ax1.set_ylabel('Predicted Conversions', color=MUTED)
ax1.set_title(f'Actual vs Predicted  (R²={r2_score(y1_te, best_preds):.3f})',
              color=TEXT, fontsize=12)
ax1.tick_params(colors=MUTED)
for sp in ax1.spines.values(): sp.set_color(BORDER)
ax1.legend(fontsize=9, facecolor=PANEL, edgecolor=BORDER, labelcolor=TEXT)

ax2 = axes[1]
ax2.set_facecolor(PANEL)
top8 = importance_df.head(8)
colors_fi = plt.cm.Blues(np.linspace(0.4, 0.9, len(top8)))
ax2.barh(top8['Feature'], top8['Importance'], color=colors_fi[::-1], edgecolor='none')
ax2.set_title('Feature Importance', color=TEXT, fontsize=12)
ax2.set_xlabel('Importance Score', color=MUTED)
ax2.tick_params(colors=MUTED)
ax2.grid(color=BORDER, lw=0.5, alpha=0.8, axis='x')
ax2.set_axisbelow(True)
for sp in ax2.spines.values(): sp.set_color(BORDER)

plt.tight_layout()
plt.savefig('outputs/ml_model.png', dpi=150, bbox_inches='tight', facecolor=BG)
print("\n  Saved: outputs/ml_model.png")

results_df = pd.DataFrame(results)
results_df.to_csv('data/model_results.csv', index=False)
print("  Saved: data/model_results.csv")
print("\n  ML analysis complete!")
