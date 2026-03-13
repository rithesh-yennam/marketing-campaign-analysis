"""
Bank Marketing Campaign — ML Classification
Predicts: Will client subscribe to term deposit? (y = yes/no)
Models: Logistic Regression, Random Forest, Gradient Boosting
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import (classification_report, confusion_matrix,
                              roc_auc_score, roc_curve, precision_recall_curve)
from sklearn.pipeline import Pipeline
import warnings, os
warnings.filterwarnings('ignore')

os.makedirs('outputs', exist_ok=True)
os.makedirs('data', exist_ok=True)

BG     = '#0D1117'
PANEL  = '#161B22'
BORDER = '#30363D'
TEXT   = '#E6EDF3'
MUTED  = '#8B949E'
ACCENT = '#58A6FF'
GREEN  = '#3FB950'
YELLOW = '#D29922'
RED    = '#F85149'
PINK   = '#BC8CFF'

# ── Load & encode ────────────────────────────────────────────────
df = pd.read_csv('data/bank_marketing.csv', sep=';')
df['subscribed'] = (df['y'] == 'yes').astype(int)

cat_cols = ['job','marital','education','default','housing','loan',
            'contact','month','day_of_week','poutcome']
le = LabelEncoder()
for col in cat_cols:
    df[col + '_enc'] = le.fit_transform(df[col].astype(str))

features = [
    'age', 'duration', 'campaign', 'pdays', 'previous',
    'emp.var.rate', 'cons.price.idx', 'cons.conf.idx',
    'euribor3m', 'nr.employed',
    'job_enc', 'marital_enc', 'education_enc', 'default_enc',
    'housing_enc', 'loan_enc', 'contact_enc', 'month_enc',
    'day_of_week_enc', 'poutcome_enc',
]

X = df[features]
y = df['subscribed']

X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

print("=" * 60)
print("  BANK SUBSCRIPTION PREDICTION — MODEL COMPARISON")
print("=" * 60)
print(f"  Train: {len(X_tr):,}  |  Test: {len(X_te):,}")
print(f"  Class balance — Yes: {y.mean()*100:.1f}%  No: {(1-y).mean()*100:.1f}%")

# ── Train models ─────────────────────────────────────────────────
models = {
    'Logistic Regression': Pipeline([
        ('scaler', StandardScaler()),
        ('clf',    LogisticRegression(max_iter=500, random_state=42, class_weight='balanced'))
    ]),
    'Random Forest': RandomForestClassifier(
        n_estimators=200, max_depth=10, random_state=42, class_weight='balanced', n_jobs=-1),
    'Gradient Boosting': GradientBoostingClassifier(
        n_estimators=200, max_depth=5, learning_rate=0.1, random_state=42),
}

results = []
trained = {}
for name, model in models.items():
    model.fit(X_tr, y_tr)
    trained[name] = model
    preds  = model.predict(X_te)
    probas = model.predict_proba(X_te)[:, 1]
    auc    = roc_auc_score(y_te, probas)
    cv     = cross_val_score(model, X, y, cv=StratifiedKFold(5), scoring='roc_auc').mean()
    rep    = classification_report(y_te, preds, output_dict=True)
    prec   = rep['1']['precision']
    rec    = rep['1']['recall']
    f1     = rep['1']['f1-score']
    results.append({'Model': name, 'AUC': round(auc,4), 'CV-AUC': round(cv,4),
                    'Precision': round(prec,4), 'Recall': round(rec,4), 'F1': round(f1,4)})
    print(f"\n  {name}")
    print(f"    AUC={auc:.4f}  CV-AUC={cv:.4f}  Prec={prec:.3f}  Rec={rec:.3f}  F1={f1:.3f}")

pd.DataFrame(results).to_csv('data/bank_model_results.csv', index=False)

# Best model = Random Forest
best   = trained['Random Forest']
probas = best.predict_proba(X_te)[:, 1]
preds  = best.predict(X_te)

# Feature importance
fi = pd.DataFrame({'Feature': features, 'Importance': best.feature_importances_})
fi = fi.sort_values('Importance', ascending=False)
fi.to_csv('data/bank_feature_importance.csv', index=False)

print(f"\n  Top 10 Feature Importances (Random Forest):")
for _, row in fi.head(10).iterrows():
    bar = '' * int(row['Importance'] * 100)
    print(f"    {row['Feature']:<22} {bar} {row['Importance']:.4f}")

# ── Visualize ────────────────────────────────────────────────────
fig, axes = plt.subplots(2, 3, figsize=(22, 12), facecolor=BG)
fig.suptitle('Bank ML Classification — Random Forest  ·  AUC={:.3f}'.format(
    roc_auc_score(y_te, probas)),
    fontsize=16, fontweight='bold', color=TEXT, y=1.01)

def sax(ax, grid_axis='y'):
    ax.set_facecolor(PANEL)
    ax.tick_params(colors=MUTED, labelsize=9)
    ax.xaxis.label.set_color(MUTED)
    ax.yaxis.label.set_color(MUTED)
    ax.title.set_color(TEXT)
    for sp in ax.spines.values(): sp.set_color(BORDER)
    ax.grid(color=BORDER, lw=0.5, alpha=0.8, axis=grid_axis)
    ax.set_axisbelow(True)

# ROC Curve — all 3 models
ax0 = axes[0, 0]; sax(ax0, 'both')
cols_roc = [ACCENT, GREEN, YELLOW]
for (name, model), col in zip(trained.items(), cols_roc):
    p = model.predict_proba(X_te)[:,1]
    fpr, tpr, _ = roc_curve(y_te, p)
    auc = roc_auc_score(y_te, p)
    ax0.plot(fpr, tpr, color=col, lw=2, label=f'{name} (AUC={auc:.3f})')
ax0.plot([0,1],[0,1], color=MUTED, lw=1, ls='--')
ax0.set_title('ROC Curve — All Models', fontsize=12, fontweight='bold')
ax0.set_xlabel('False Positive Rate'); ax0.set_ylabel('True Positive Rate')
ax0.legend(fontsize=8, facecolor=PANEL, edgecolor=BORDER, labelcolor=TEXT)

# Confusion Matrix
ax1 = axes[0, 1]; ax1.set_facecolor(PANEL)
for sp in ax1.spines.values(): sp.set_color(BORDER)
cm = confusion_matrix(y_te, preds)
im = ax1.imshow(cm, cmap='Blues', aspect='auto')
ax1.set_xticks([0,1]); ax1.set_yticks([0,1])
ax1.set_xticklabels(['No','Yes'], color=MUTED)
ax1.set_yticklabels(['No','Yes'], color=MUTED)
for i in range(2):
    for j in range(2):
        ax1.text(j, i, f'{cm[i,j]:,}', ha='center', va='center',
                 color=TEXT, fontsize=14, fontweight='bold')
ax1.set_title('Confusion Matrix (RF)', fontsize=12, fontweight='bold', color=TEXT)
ax1.set_xlabel('Predicted'); ax1.set_ylabel('Actual')

# Precision-Recall Curve
ax2 = axes[0, 2]; sax(ax2, 'both')
prec_c, rec_c, _ = precision_recall_curve(y_te, probas)
ax2.plot(rec_c, prec_c, color=PINK, lw=2)
ax2.fill_between(rec_c, prec_c, alpha=0.12, color=PINK)
ax2.axhline(y.mean(), color=YELLOW, lw=1.2, ls='--', label=f'Baseline ({y.mean():.2f})')
ax2.set_title('Precision–Recall Curve (RF)', fontsize=12, fontweight='bold')
ax2.set_xlabel('Recall'); ax2.set_ylabel('Precision')
ax2.legend(fontsize=8, facecolor=PANEL, edgecolor=BORDER, labelcolor=TEXT)

# Feature Importance
ax3 = axes[1, 0]; sax(ax3, 'x')
fi10 = fi.head(10)
fi_cols = plt.cm.Blues(np.linspace(0.45, 0.9, len(fi10)))
ax3.barh(fi10['Feature'], fi10['Importance'], color=fi_cols[::-1], edgecolor='none')
ax3.set_title('Top 10 Feature Importances', fontsize=12, fontweight='bold')
ax3.set_xlabel('Importance Score')

# Probability Distribution
ax4 = axes[1, 1]; sax(ax4, 'y')
bins = np.linspace(0, 1, 30)
ax4.hist(probas[y_te == 0], bins=bins, color=RED,   alpha=0.6, label='No subscription', edgecolor='none')
ax4.hist(probas[y_te == 1], bins=bins, color=GREEN, alpha=0.7, label='Subscribed',       edgecolor='none')
ax4.axvline(0.5, color=YELLOW, lw=1.5, ls='--', label='Threshold 0.5')
ax4.set_title('Predicted Probability Distribution', fontsize=12, fontweight='bold')
ax4.set_xlabel('Predicted Probability'); ax4.set_ylabel('Count')
ax4.legend(fontsize=8, facecolor=PANEL, edgecolor=BORDER, labelcolor=TEXT)

# Model comparison bar
ax5 = axes[1, 2]; sax(ax5)
res_df  = pd.DataFrame(results)
x_pos   = np.arange(len(res_df))
w       = 0.25
ax5.bar(x_pos - w,   res_df['AUC'],       w, color=ACCENT,  label='AUC',       edgecolor='none')
ax5.bar(x_pos,       res_df['Precision'],  w, color=GREEN,   label='Precision', edgecolor='none')
ax5.bar(x_pos + w,   res_df['Recall'],     w, color=YELLOW,  label='Recall',    edgecolor='none')
ax5.set_xticks(x_pos)
ax5.set_xticklabels([r['Model'].replace(' ', '\n') for r in results], fontsize=8)
ax5.set_title('Model Comparison', fontsize=12, fontweight='bold')
ax5.set_ylabel('Score')
ax5.legend(fontsize=8, facecolor=PANEL, edgecolor=BORDER, labelcolor=TEXT)
ax5.set_ylim(0, 1.05)

plt.tight_layout()
plt.savefig('outputs/bank_ml.png', dpi=150, bbox_inches='tight', facecolor=BG)
print("\n Saved: outputs/bank_ml.png")
print("  ML classification complete!")
