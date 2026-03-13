"""
Bank Marketing Campaign — Visualizations
Generates 3 chart files saved to outputs/
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import warnings, os
warnings.filterwarnings('ignore')

os.makedirs('outputs', exist_ok=True)

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

def style_ax(ax, grid_axis='y'):
    ax.set_facecolor(PANEL)
    ax.tick_params(colors=MUTED, labelsize=9)
    ax.xaxis.label.set_color(MUTED)
    ax.yaxis.label.set_color(MUTED)
    ax.title.set_color(TEXT)
    for sp in ax.spines.values():
        sp.set_color(BORDER)
    ax.grid(color=BORDER, linewidth=0.5, alpha=0.8, axis=grid_axis)
    ax.set_axisbelow(True)

df = pd.read_csv('data/bank_marketing.csv', sep=';')
df['subscribed'] = (df['y'] == 'yes').astype(int)

job  = pd.read_csv('data/bank_by_job.csv')
mon  = pd.read_csv('data/bank_by_month.csv')
age  = pd.read_csv('data/bank_by_age.csv')
edu  = pd.read_csv('data/bank_by_education.csv')
dur  = pd.read_csv('data/bank_by_duration.csv')

# ════════════════════════════════════════════════════════════════
# CHART A — Bank Campaign Overview Dashboard
# ════════════════════════════════════════════════════════════════
fig = plt.figure(figsize=(24, 15), facecolor=BG)
fig.suptitle('Bank Marketing Campaign  ·  Subscription Analysis  ·  41,188 Clients',
             fontsize=18, fontweight='bold', color=TEXT, y=0.97, fontfamily='monospace')

gs = gridspec.GridSpec(3, 4, figure=fig,
                       hspace=0.55, wspace=0.42,
                       left=0.05, right=0.97, top=0.91, bottom=0.06)

# KPI cards
total       = len(df)
subscribed  = df['subscribed'].sum()
sub_rate    = subscribed / total * 100
avg_duration= df['duration'].mean()
avg_calls   = df['campaign'].mean()

kpis = [
    ('Total Contacts',     f'{total:,}',          ACCENT),
    ('Subscriptions',      f'{subscribed:,}',      GREEN),
    ('Conversion Rate',    f'{sub_rate:.1f}%',     YELLOW),
    ('Avg Call Duration',  f'{avg_duration:.0f}s', PINK),
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

# Job subscription rate (horizontal bar)
ax1 = fig.add_subplot(gs[1, 0:2])
style_ax(ax1, grid_axis='x')
job_s = job.sort_values('Rate%')
bar_colors = [GREEN if v >= job['Rate%'].mean() else ACCENT for v in job_s['Rate%']]
hbars = ax1.barh(job_s['job'], job_s['Rate%'], color=bar_colors, height=0.6, edgecolor='none')
ax1.axvline(job['Rate%'].mean(), color=YELLOW, lw=1.2, ls='--',
            label=f"Avg {job['Rate%'].mean():.1f}%")
for b, v in zip(hbars, job_s['Rate%']):
    ax1.text(v + 0.2, b.get_y() + b.get_height()/2,
             f'{v:.1f}%', va='center', fontsize=8, color=TEXT)
ax1.set_title('Subscription Rate by Job', fontsize=12, fontweight='bold', pad=10)
ax1.set_xlabel('Conversion Rate %')
ax1.legend(facecolor=PANEL, edgecolor=BORDER, labelcolor=TEXT, fontsize=8)

# Monthly contact volume + conversion
ax2 = fig.add_subplot(gs[1, 2:4])
style_ax(ax2)
month_order = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
mon['Month_N'] = mon['month'].map({m: i for i, m in enumerate(month_order)})
mon_s = mon.sort_values('Month_N')
ax2b = ax2.twinx()
ax2.bar(mon_s['month'], mon_s['Total'], color=ACCENT, alpha=0.4, width=0.6, edgecolor='none', label='Contacts')
ax2b.plot(mon_s['month'], mon_s['Rate%'], color=GREEN, lw=2.5,
          marker='o', ms=5, markerfacecolor=BG, markeredgecolor=GREEN, label='Conv. Rate %')
ax2.set_title('Monthly Contacts & Conversion Rate', fontsize=12, fontweight='bold', pad=10)
ax2.set_ylabel('Total Contacts', color=MUTED)
ax2b.set_ylabel('Conversion Rate %', color=GREEN)
ax2b.tick_params(colors=GREEN, labelsize=9)
ax2b.spines['right'].set_color(GREEN)
ax2.tick_params(axis='x', rotation=35, labelsize=8)
lines1, labels1 = ax2.get_legend_handles_labels()
lines2, labels2 = ax2b.get_legend_handles_labels()
ax2.legend(lines1+lines2, labels1+labels2, facecolor=PANEL, edgecolor=BORDER,
           labelcolor=TEXT, fontsize=8, loc='upper right')

# Age group subscription rate
ax3 = fig.add_subplot(gs[2, 0:2])
style_ax(ax3)
age_colors = plt.cm.Blues(np.linspace(0.4, 0.85, len(age)))
bars3 = ax3.bar(age['age_group'], age['Rate%'], color=age_colors, width=0.6, edgecolor='none')
for b, v in zip(bars3, age['Rate%']):
    ax3.text(b.get_x() + b.get_width()/2, v + 0.2,
             f'{v:.1f}%', ha='center', fontsize=9, color=TEXT, fontweight='bold')
ax3.set_title('Subscription Rate by Age Group', fontsize=12, fontweight='bold', pad=10)
ax3.set_ylabel('Conversion Rate %')

# Call duration vs conversion
ax4 = fig.add_subplot(gs[2, 2:4])
style_ax(ax4)
dur_colors = [RED, YELLOW, ACCENT, GREEN, PINK]
bars4 = ax4.bar(dur['duration_bin'], dur['Rate%'], color=dur_colors, width=0.6, edgecolor='none')
for b, v in zip(bars4, dur['Rate%']):
    ax4.text(b.get_x() + b.get_width()/2, v + 0.3,
             f'{v:.1f}%', ha='center', fontsize=9, color=TEXT, fontweight='bold')
ax4.set_title('Conversion Rate by Call Duration', fontsize=12, fontweight='bold', pad=10)
ax4.set_ylabel('Conversion Rate %')
ax4.set_xlabel('Call Duration')

plt.savefig('outputs/bank_dashboard.png', dpi=150, bbox_inches='tight', facecolor=BG)
print("✅  Saved: outputs/bank_dashboard.png")

# ════════════════════════════════════════════════════════════════
# CHART B — Education, Previous Outcome, Economic Indicators
# ════════════════════════════════════════════════════════════════
fig2, axes2 = plt.subplots(1, 3, figsize=(22, 6), facecolor=BG)
fig2.suptitle('Deep Dive — Education, Prior Contact & Economic Factors',
              fontsize=15, fontweight='bold', color=TEXT, y=1.02)

# Education
ax_e = axes2[0]
style_ax(ax_e, grid_axis='x')
edu_s = edu.sort_values('Rate%')
edu_colors = [GREEN if v >= edu['Rate%'].mean() else ACCENT for v in edu_s['Rate%']]
hbars_e = ax_e.barh(edu_s['education'], edu_s['Rate%'], color=edu_colors, height=0.6, edgecolor='none')
for b, v in zip(hbars_e, edu_s['Rate%']):
    ax_e.text(v + 0.1, b.get_y() + b.get_height()/2, f'{v:.1f}%', va='center', fontsize=8, color=TEXT)
ax_e.set_title('Rate by Education Level', fontsize=12, fontweight='bold', color=TEXT)
ax_e.set_xlabel('Conversion Rate %')

# Previous outcome
ax_p = axes2[1]
style_ax(ax_p)
pout = df.groupby('poutcome').agg(
    Total      =('subscribed','count'),
    Subscribed =('subscribed','sum')
).reset_index()
pout['Rate%'] = (pout['Subscribed'] / pout['Total'] * 100).round(1)
p_colors = {'failure': RED, 'nonexistent': MUTED, 'success': GREEN}
bar_pc = [p_colors.get(p, ACCENT) for p in pout['poutcome']]
bars_p = ax_p.bar(pout['poutcome'], pout['Rate%'], color=bar_pc, width=0.5, edgecolor='none')
for b, v in zip(bars_p, pout['Rate%']):
    ax_p.text(b.get_x() + b.get_width()/2, v + 0.3, f'{v:.1f}%',
              ha='center', fontsize=11, color=TEXT, fontweight='bold')
ax_p.set_title('Rate by Previous Campaign Outcome', fontsize=12, fontweight='bold', color=TEXT)
ax_p.set_ylabel('Conversion Rate %')

# Euribor vs subscription scatter
ax_ec = axes2[2]
style_ax(ax_ec)
sub_yes = df[df['subscribed'] == 1]
sub_no  = df[df['subscribed'] == 0].sample(2000, random_state=42)
ax_ec.scatter(sub_no['euribor3m'], sub_no['cons.conf.idx'],
              alpha=0.2, s=8, color=RED,   label='No subscription',  edgecolors='none')
ax_ec.scatter(sub_yes['euribor3m'], sub_yes['cons.conf.idx'],
              alpha=0.4, s=12, color=GREEN, label='Subscribed',        edgecolors='none')
ax_ec.set_title('Euribor Rate vs Consumer Confidence', fontsize=12, fontweight='bold', color=TEXT)
ax_ec.set_xlabel('Euribor 3-Month Rate')
ax_ec.set_ylabel('Consumer Confidence Index')
ax_ec.legend(facecolor=PANEL, edgecolor=BORDER, labelcolor=TEXT, fontsize=9)

plt.tight_layout()
plt.savefig('outputs/bank_deep_dive.png', dpi=150, bbox_inches='tight', facecolor=BG)
print("✅  Saved: outputs/bank_deep_dive.png")
print("\n🎉  Bank visualizations complete!")
