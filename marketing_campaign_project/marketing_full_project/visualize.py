"""
Marketing Campaign Performance Analysis
Step 3: Dashboard Visualizations (saves all charts to outputs/)
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import warnings, os
warnings.filterwarnings('ignore')

os.makedirs('outputs', exist_ok=True)

# ── Load data ────────────────────────────────────────────────────
df      = pd.read_csv('data/marketing_data.csv')
ch      = pd.read_csv('data/channel_summary.csv')
monthly = pd.read_csv('data/monthly_trend.csv').sort_values('Month_Num')
camp    = pd.read_csv('data/campaign_summary.csv')
reg     = pd.read_csv('data/region_summary.csv')
top10   = pd.read_csv('data/top10_campaigns.csv')

# ── Design tokens ────────────────────────────────────────────────
BG      = '#0D1117'
PANEL   = '#161B22'
BORDER  = '#30363D'
TEXT    = '#E6EDF3'
MUTED   = '#8B949E'
ACCENT  = '#58A6FF'
GREEN   = '#3FB950'
YELLOW  = '#D29922'
RED     = '#F85149'
PINK    = '#BC8CFF'

CH_COLORS = {
    'Email':        '#58A6FF',
    'Social Media': '#BC8CFF',
    'Google Ads':   '#3FB950',
    'Influencer':   '#F85149',
    'SEO':          '#D29922',
}

def style_ax(ax, grid=True):
    ax.set_facecolor(PANEL)
    ax.tick_params(colors=MUTED, labelsize=9)
    ax.xaxis.label.set_color(MUTED)
    ax.yaxis.label.set_color(MUTED)
    ax.title.set_color(TEXT)
    for sp in ax.spines.values():
        sp.set_color(BORDER)
    if grid:
        ax.grid(color=BORDER, linewidth=0.5, alpha=0.8, axis='y')
    ax.set_axisbelow(True)

# ════════════════════════════════════════════════════════════════
# CHART 1 — Main Executive Dashboard (6-panel)
# ════════════════════════════════════════════════════════════════
fig = plt.figure(figsize=(24, 15), facecolor=BG)
fig.suptitle('Marketing Campaign Performance Dashboard  ·  FY 2024',
             fontsize=20, fontweight='bold', color=TEXT, y=0.97,
             fontfamily='monospace')

gs = gridspec.GridSpec(3, 4, figure=fig,
                       hspace=0.55, wspace=0.40,
                       left=0.05, right=0.97,
                       top=0.91, bottom=0.06)

total_spend   = df['Budget'].sum()
total_revenue = df['Revenue'].sum()
overall_roas  = total_revenue / total_spend
overall_roi   = (total_revenue - total_spend) / total_spend * 100
avg_ctr       = df['Clicks'].sum() / df['Impressions'].sum() * 100
total_conv    = df['Conversions'].sum()

kpis = [
    ('Total Spend',       f"${total_spend/1e6:.2f}M",  ACCENT),
    ('Total Revenue',     f"${total_revenue/1e6:.1f}M",GREEN),
    ('Overall ROAS',      f"{overall_roas:.1f}×",       YELLOW),
    ('Overall ROI',       f"{overall_roi:,.0f}%",        PINK),
]
for i, (label, val, color) in enumerate(kpis):
    ax = fig.add_subplot(gs[0, i])
    ax.set_facecolor(PANEL)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color(color); sp.set_linewidth(2)
    ax.text(0.5, 0.60, val, transform=ax.transAxes, ha='center', va='center',
            fontsize=26, fontweight='bold', color=color, fontfamily='monospace')
    ax.text(0.5, 0.20, label, transform=ax.transAxes, ha='center', va='center',
            fontsize=10, color=MUTED)

# Panel 2-row: ROAS by Channel (bar)
ax1 = fig.add_subplot(gs[1, 0:2])
style_ax(ax1)
colors_bar = [CH_COLORS[c] for c in ch['Channel']]
bars = ax1.bar(ch['Channel'], ch['ROAS'], color=colors_bar, width=0.55, edgecolor='none')
for b, v in zip(bars, ch['ROAS']):
    ax1.text(b.get_x() + b.get_width()/2, b.get_height() + 2,
             f'{v:.0f}×', ha='center', fontsize=9, color=TEXT, fontweight='bold')
ax1.set_title('ROAS by Channel', fontsize=12, fontweight='bold', pad=10)
ax1.set_ylabel('ROAS', color=MUTED); ax1.tick_params(axis='x', rotation=10)

# Monthly Revenue Line
ax2 = fig.add_subplot(gs[1, 2:4])
style_ax(ax2)
x = range(len(monthly))
ax2.plot(x, monthly['Revenue']/1e3, color=GREEN, lw=2.5,
         marker='o', ms=5, markerfacecolor=BG, markeredgecolor=GREEN, markeredgewidth=1.5)
ax2.fill_between(x, monthly['Revenue']/1e3, alpha=0.12, color=GREEN)
ax2.set_xticks(x)
ax2.set_xticklabels(monthly['Month'], rotation=45, fontsize=8)
ax2.set_title('Monthly Revenue ($K)', fontsize=12, fontweight='bold', pad=10)
ax2.set_ylabel('Revenue ($K)', color=MUTED)

# Campaign Revenue (horizontal bar)
ax3 = fig.add_subplot(gs[2, 0:2])
style_ax(ax3, grid=False)
camp_s = camp.sort_values('Revenue')
camp_colors = plt.cm.Blues(np.linspace(0.4, 0.85, len(camp_s)))
hbars = ax3.barh(camp_s['Campaign'], camp_s['Revenue']/1e3, color=camp_colors, edgecolor='none', height=0.55)
for b, v in zip(hbars, camp_s['Revenue']/1e3):
    ax3.text(v + 500, b.get_y() + b.get_height()/2, f'${v:,.0f}K',
             va='center', fontsize=8, color=TEXT)
ax3.set_title('Revenue by Campaign ($K)', fontsize=12, fontweight='bold', pad=10)
ax3.set_xlabel('Revenue ($K)', color=MUTED)
ax3.grid(color=BORDER, linewidth=0.5, alpha=0.8, axis='x')

# ROI by Region
ax4 = fig.add_subplot(gs[2, 2:4])
style_ax(ax4)
reg_s = reg.sort_values('ROI%')
reg_colors = [GREEN if v > reg['ROI%'].mean() else ACCENT for v in reg_s['ROI%']]
ax4.bar(reg_s['Region'], reg_s['ROI%'], color=reg_colors, width=0.55, edgecolor='none')
ax4.axhline(reg['ROI%'].mean(), color=YELLOW, lw=1.2, ls='--', label=f"Avg {reg['ROI%'].mean():,.0f}%")
ax4.legend(fontsize=8, facecolor=PANEL, edgecolor=BORDER, labelcolor=TEXT)
ax4.set_title('ROI % by Region', fontsize=12, fontweight='bold', pad=10)
ax4.set_ylabel('ROI %', color=MUTED)

plt.savefig('outputs/dashboard_main.png', dpi=150, bbox_inches='tight', facecolor=BG)
print("✅  Saved: outputs/dashboard_main.png")

# ════════════════════════════════════════════════════════════════
# CHART 2 — Conversion Funnel + CTR/CVR Comparison
# ════════════════════════════════════════════════════════════════
fig2, axes2 = plt.subplots(1, 2, figsize=(16, 6), facecolor=BG)
fig2.suptitle('Channel Efficiency Analysis', fontsize=16, fontweight='bold',
              color=TEXT, y=1.02)

# Funnel
ax_f = axes2[0]
ax_f.set_facecolor(PANEL)
funnel_stages = ['Impressions', 'Clicks', 'Conversions']
funnel_vals   = [df['Impressions'].sum()/1e6, df['Clicks'].sum()/1e3, df['Conversions'].sum()/1e3]
funnel_units  = ['M', 'K', 'K']
funnel_cols   = [ACCENT, PINK, GREEN]
widths = [1.0, 0.65, 0.35]
for i, (stage, val, unit, col, w) in enumerate(zip(funnel_stages, funnel_vals, funnel_units, funnel_cols, widths)):
    left = (1.0 - w) / 2
    ax_f.barh(2 - i, w, left=left, height=0.45, color=col, edgecolor='none')
    ax_f.text(0.5, 2 - i, f'{stage}  {val:.1f}{unit}',
              ha='center', va='center', color='white', fontsize=11, fontweight='bold')
ax_f.set_xlim(0, 1); ax_f.set_yticks([]); ax_f.set_xticks([])
ax_f.set_title('Conversion Funnel', fontsize=13, fontweight='bold', color=TEXT, pad=10)
for sp in ax_f.spines.values(): sp.set_color(BORDER)

# CTR vs CVR by channel (grouped bar)
ax_g = axes2[1]
style_ax(ax_g)
x_pos   = np.arange(len(ch))
bar_w   = 0.35
ax_g.bar(x_pos - bar_w/2, ch.sort_values('Channel')['CTR%'], bar_w,
         color=ACCENT, label='CTR %', edgecolor='none')
ax_g.bar(x_pos + bar_w/2, ch.sort_values('Channel')['CVR%'], bar_w,
         color=GREEN, label='CVR %', edgecolor='none')
ax_g.set_xticks(x_pos)
ax_g.set_xticklabels(ch.sort_values('Channel')['Channel'], rotation=10, fontsize=9)
ax_g.set_title('CTR % vs CVR % by Channel', fontsize=13, fontweight='bold', color=TEXT, pad=10)
ax_g.set_ylabel('%', color=MUTED)
ax_g.legend(facecolor=PANEL, edgecolor=BORDER, labelcolor=TEXT, fontsize=9)

plt.tight_layout()
plt.savefig('outputs/channel_efficiency.png', dpi=150, bbox_inches='tight', facecolor=BG)
print("✅  Saved: outputs/channel_efficiency.png")

# ════════════════════════════════════════════════════════════════
# CHART 3 — Spend vs Revenue Scatter + Quarterly Trend
# ════════════════════════════════════════════════════════════════
fig3, axes3 = plt.subplots(1, 2, figsize=(16, 6), facecolor=BG)
fig3.suptitle('Budget Efficiency & Quarterly Performance', fontsize=16,
              fontweight='bold', color=TEXT, y=1.02)

ax_s = axes3[0]
style_ax(ax_s, grid=True)
for _, row in ch.iterrows():
    ax_s.scatter(row['Spend']/1e3, row['Revenue']/1e3,
                 color=CH_COLORS[row['Channel']], s=220, zorder=5,
                 edgecolors='white', linewidth=0.8)
    ax_s.annotate(row['Channel'],
                  (row['Spend']/1e3, row['Revenue']/1e3),
                  xytext=(6, 4), textcoords='offset points',
                  color=TEXT, fontsize=9)
ax_s.set_title('Spend vs Revenue by Channel ($K)', fontsize=13, fontweight='bold', color=TEXT)
ax_s.set_xlabel('Spend ($K)'); ax_s.set_ylabel('Revenue ($K)')

quarterly = pd.read_csv('data/quarterly_summary.csv')
ax_q = axes3[1]
style_ax(ax_q)
q_colors = [ACCENT, GREEN, YELLOW, PINK]
bars_q = ax_q.bar(quarterly['Quarter'], quarterly['Revenue']/1e3, color=q_colors, width=0.55, edgecolor='none')
for b, v, r in zip(bars_q, quarterly['Revenue']/1e3, quarterly['ROAS']):
    ax_q.text(b.get_x() + b.get_width()/2, v + 500, f'ROAS {r:.0f}×',
              ha='center', fontsize=9, color=TEXT)
ax_q.set_title('Quarterly Revenue ($K) with ROAS', fontsize=13, fontweight='bold', color=TEXT)
ax_q.set_ylabel('Revenue ($K)')

plt.tight_layout()
plt.savefig('outputs/budget_quarterly.png', dpi=150, bbox_inches='tight', facecolor=BG)
print("✅  Saved: outputs/budget_quarterly.png")

print("\n🎉  All charts saved to outputs/")
