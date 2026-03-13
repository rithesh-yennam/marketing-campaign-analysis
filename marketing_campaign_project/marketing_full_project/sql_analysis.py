"""
Marketing Campaign Performance Analysis
SQL Analysis -- MySQL
Author: Rithesh Yennam
"""
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os, warnings
warnings.filterwarnings('ignore')

os.makedirs('data', exist_ok=True)
os.makedirs('outputs', exist_ok=True)

# ── MySQL CONNECTION SETTINGS ─────────────────────────────────────
MYSQL_HOST     = 'localhost'
MYSQL_PORT     = 3306
MYSQL_USER     = 'root'
MYSQL_PASSWORD = 'Ritesh123#'
MYSQL_DATABASE = 'marketing_campaign_db'

# ── Connect to MySQL ──────────────────────────────────────────────
USE_MYSQL = False
conn = None

try:
    import mysql.connector
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE}")
    cursor.execute(f"USE {MYSQL_DATABASE}")
    conn.database = MYSQL_DATABASE
    USE_MYSQL = True
    print("[OK] Connected to MySQL successfully")
    print(f"     Host: {MYSQL_HOST} | Database: {MYSQL_DATABASE}")
except Exception as e:
    print(f"[INFO] MySQL not available: {e}")
    print("[INFO] Falling back to SQLite (queries are identical)")
    import sqlite3
    conn = sqlite3.connect(':memory:')

print("=" * 60)
print("  SQL ANALYSIS -- BANK MARKETING CAMPAIGN")
print("=" * 60)

# ── Load Data ─────────────────────────────────────────────────────
df = pd.read_csv('data/bank_marketing_clean.csv')
df.columns = [c.replace('.', '_') for c in df.columns]

if USE_MYSQL:
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS marketing_campaign")
    cursor.execute("""
    CREATE TABLE marketing_campaign (
        id                INT AUTO_INCREMENT PRIMARY KEY,
        age               INT,
        age_group         VARCHAR(20),
        job               VARCHAR(50),
        marital           VARCHAR(20),
        education         VARCHAR(50),
        housing           VARCHAR(10),
        loan              VARCHAR(10),
        contact           VARCHAR(20),
        month             VARCHAR(10),
        day_of_week       VARCHAR(10),
        duration          INT,
        duration_capped   FLOAT,
        duration_category VARCHAR(30),
        campaign          INT,
        campaign_intensity VARCHAR(20),
        pdays             INT,
        previous          INT,
        poutcome          VARCHAR(20),
        season            VARCHAR(10),
        previously_contacted INT,
        emp_var_rate      FLOAT,
        cons_price_idx    FLOAT,
        cons_conf_idx     FLOAT,
        euribor3m         FLOAT,
        nr_employed       FLOAT,
        subscribed        INT,
        y                 VARCHAR(5)
    )""")
    conn.commit()

    cols = ['age','age_group','job','marital','education',
            'housing','loan','contact','month','day_of_week',
            'duration','duration_capped','duration_category',
            'campaign','campaign_intensity','pdays','previous',
            'poutcome','season','previously_contacted',
            'emp_var_rate','cons_price_idx','cons_conf_idx',
            'euribor3m','nr_employed','subscribed','y']

    df_ins = df[cols].copy()
    for c in ['duration_category', 'campaign_intensity', 'age_group']:
        df_ins[c] = df_ins[c].astype(str)

    placeholders = ', '.join(['%s'] * len(cols))
    ins_sql = f"INSERT INTO marketing_campaign ({', '.join(cols)}) VALUES ({placeholders})"

    for i in range(0, len(df_ins), 1000):
        batch = df_ins.iloc[i:i+1000]
        rows = [tuple(None if pd.isna(v) else v for v in row) for row in batch.values]
        cursor.executemany(ins_sql, rows)
    conn.commit()
    print(f"[OK] Inserted {len(df):,} rows into MySQL table")

    def run_query(title, sql):
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")
        result = pd.read_sql(sql, conn)
        print(result.to_string(index=False))
        return result

else:
    df.to_sql('marketing_campaign', conn, index=False, if_exists='replace')
    print(f"[OK] Loaded {len(df):,} records into SQLite")

    def run_query(title, sql):
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")
        result = pd.read_sql_query(sql, conn)
        print(result.to_string(index=False))
        return result

# ────────────────────────────────────────────────────────────────
# QUERY 1: Overall Campaign Success Rate
# ────────────────────────────────────────────────────────────────
q1 = run_query("Q1: Overall Campaign Success Rate", """
SELECT
    COUNT(*)                                        AS total_contacts,
    SUM(subscribed)                                 AS total_subscribed,
    ROUND(SUM(subscribed) * 100.0 / COUNT(*), 2)   AS success_rate_pct,
    ROUND(AVG(duration), 0)                         AS avg_call_duration_sec
FROM marketing_campaign
""")

# ────────────────────────────────────────────────────────────────
# QUERY 2: Customer Segmentation by Education
# ────────────────────────────────────────────────────────────────
q2 = run_query("Q2: Customer Segmentation by Education", """
SELECT
    education,
    COUNT(*)                                        AS total_customers,
    SUM(subscribed)                                 AS subscribed,
    ROUND(SUM(subscribed) * 100.0 / COUNT(*), 2)   AS conversion_rate_pct
FROM marketing_campaign
GROUP BY education
ORDER BY conversion_rate_pct DESC
""")

# ────────────────────────────────────────────────────────────────
# QUERY 3: Campaign Response by Job Category
# ────────────────────────────────────────────────────────────────
q3 = run_query("Q3: Campaign Response by Job Category", """
SELECT
    job,
    COUNT(*)                                        AS total_contacts,
    SUM(subscribed)                                 AS subscribed,
    ROUND(SUM(subscribed) * 100.0 / COUNT(*), 2)   AS conversion_rate_pct,
    ROUND(AVG(duration), 0)                         AS avg_call_sec
FROM marketing_campaign
GROUP BY job
ORDER BY conversion_rate_pct DESC
""")

# ────────────────────────────────────────────────────────────────
# QUERY 4: Monthly Campaign Performance
# ────────────────────────────────────────────────────────────────
q4 = run_query("Q4: Monthly Campaign Performance", """
SELECT
    month,
    COUNT(*)                                        AS total_contacts,
    SUM(subscribed)                                 AS subscriptions,
    ROUND(SUM(subscribed) * 100.0 / COUNT(*), 2)   AS conversion_pct,
    ROUND(AVG(duration), 0)                         AS avg_duration_sec
FROM marketing_campaign
GROUP BY month
ORDER BY subscriptions DESC
""")

# ────────────────────────────────────────────────────────────────
# QUERY 5: Age Group Analysis
# ────────────────────────────────────────────────────────────────
q5 = run_query("Q5: Age Group Subscription Analysis", """
SELECT
    age_group,
    COUNT(*)                                        AS total,
    SUM(subscribed)                                 AS subscribed,
    ROUND(SUM(subscribed) * 100.0 / COUNT(*), 2)   AS conversion_pct,
    ROUND(AVG(age), 1)                              AS avg_age,
    ROUND(AVG(duration), 0)                         AS avg_call_sec
FROM marketing_campaign
GROUP BY age_group
ORDER BY age_group
""")

# ────────────────────────────────────────────────────────────────
# QUERY 6: Previous Campaign Outcome Impact
# ────────────────────────────────────────────────────────────────
q6 = run_query("Q6: Impact of Previous Campaign Outcome", """
SELECT
    poutcome                                        AS previous_outcome,
    COUNT(*)                                        AS total_contacts,
    SUM(subscribed)                                 AS subscribed,
    ROUND(SUM(subscribed) * 100.0 / COUNT(*), 2)   AS conversion_pct
FROM marketing_campaign
GROUP BY poutcome
ORDER BY conversion_pct DESC
""")

# ────────────────────────────────────────────────────────────────
# QUERY 7: Top Customer Segments
# ────────────────────────────────────────────────────────────────
q7 = run_query("Q7: Top Customer Segments - Job + Education + Contact", """
SELECT
    job,
    education,
    contact,
    COUNT(*)                                        AS total,
    SUM(subscribed)                                 AS subscribed,
    ROUND(SUM(subscribed) * 100.0 / COUNT(*), 2)   AS conversion_pct
FROM marketing_campaign
GROUP BY job, education, contact
HAVING COUNT(*) >= 50
ORDER BY conversion_pct DESC
LIMIT 10
""")

# ────────────────────────────────────────────────────────────────
# QUERY 8: Call Duration Impact on Conversion
# ────────────────────────────────────────────────────────────────
q8 = run_query("Q8: Call Duration vs Conversion Rate", """
SELECT
    duration_category,
    COUNT(*)                                        AS total,
    SUM(subscribed)                                 AS subscribed,
    ROUND(SUM(subscribed) * 100.0 / COUNT(*), 2)   AS conversion_pct
FROM marketing_campaign
GROUP BY duration_category
ORDER BY conversion_pct ASC
""")

# ────────────────────────────────────────────────────────────────
# QUERY 9: Season vs Conversion Rate
# ────────────────────────────────────────────────────────────────
q9 = run_query("Q9: Season vs Conversion Rate", """
SELECT
    season,
    COUNT(*)                                        AS total_contacts,
    SUM(subscribed)                                 AS subscribed,
    ROUND(SUM(subscribed) * 100.0 / COUNT(*), 2)   AS conversion_pct
FROM marketing_campaign
GROUP BY season
ORDER BY conversion_pct DESC
""")

# ────────────────────────────────────────────────────────────────
# QUERY 10: Housing Loan & Personal Loan Impact
# ────────────────────────────────────────────────────────────────
q10 = run_query("Q10: Housing Loan & Personal Loan Impact", """
SELECT
    housing,
    loan,
    COUNT(*)                                        AS total,
    SUM(subscribed)                                 AS subscribed,
    ROUND(SUM(subscribed) * 100.0 / COUNT(*), 2)   AS conversion_pct
FROM marketing_campaign
GROUP BY housing, loan
ORDER BY conversion_pct DESC
""")

conn.close()

# ── Save all query results ────────────────────────────────────────
queries = [
    ('q1_overall',        q1),
    ('q2_education',      q2),
    ('q3_job',            q3),
    ('q4_monthly',        q4),
    ('q5_age',            q5),
    ('q6_prev_outcome',   q6),
    ('q7_segments',       q7),
    ('q8_duration',       q8),
    ('q9_season',         q9),
    ('q10_loan',          q10),
]
for name, result in queries:
    result.to_csv(f'data/sql_{name}.csv', index=False)
print("\n[OK] All query results saved to data/sql_*.csv")

# ── Visualise 4 key SQL results ───────────────────────────────────
BG    = '#0D1117'
PANEL = '#161B22'
BORDER= '#30363D'
TEXT  = '#E6EDF3'
MUTED = '#8B949E'
ACCENT= '#58A6FF'
GREEN = '#3FB950'
YELLOW= '#D29922'
RED   = '#F85149'
PINK  = '#BC8CFF'

fig = plt.figure(figsize=(22, 12), facecolor=BG)
fig.suptitle('SQL Analysis Results -- Bank Marketing Campaign',
             fontsize=17, fontweight='bold', color=TEXT, y=0.98,
             fontfamily='monospace')
gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.35,
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

# Job conversion rates
ax1 = fig.add_subplot(gs[0, 0])
sax(ax1, 'x')
job_s = q3.sort_values('conversion_rate_pct')
bar_c = [GREEN if v >= q3['conversion_rate_pct'].mean() else ACCENT
         for v in job_s['conversion_rate_pct']]
ax1.barh(job_s['job'], job_s['conversion_rate_pct'],
         color=bar_c, edgecolor='none', height=0.6)
ax1.axvline(q3['conversion_rate_pct'].mean(), color=YELLOW, lw=1.2,
            ls='--', label=f"Avg {q3['conversion_rate_pct'].mean():.1f}%")
ax1.set_title('Q3: Conversion Rate by Job (%)', fontweight='bold', fontsize=11)
ax1.set_xlabel('Conversion Rate %')
ax1.legend(fontsize=8, facecolor=PANEL, edgecolor=BORDER, labelcolor=TEXT)

# Monthly performance
ax2 = fig.add_subplot(gs[0, 1])
sax(ax2)
month_order = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
q4_s = q4.copy()
q4_s['month_n'] = q4_s['month'].map({m:i for i,m in enumerate(month_order)})
q4_s = q4_s.sort_values('month_n')
ax2b = ax2.twinx()
ax2.bar(q4_s['month'], q4_s['total_contacts']/1000, color=ACCENT, alpha=0.4,
        width=0.6, edgecolor='none')
ax2b.plot(q4_s['month'], q4_s['conversion_pct'], color=GREEN, lw=2.5,
          marker='o', ms=5, markerfacecolor=BG, markeredgecolor=GREEN)
ax2.set_title('Q4: Monthly Contacts & Conversion %', fontweight='bold', fontsize=11)
ax2.set_ylabel('Contacts (K)', color=MUTED)
ax2b.set_ylabel('Conversion %', color=GREEN)
ax2b.tick_params(colors=GREEN, labelsize=9)
ax2b.spines['right'].set_color(GREEN)
ax2.tick_params(axis='x', rotation=35, labelsize=8)

# Duration impact
ax3 = fig.add_subplot(gs[1, 0])
sax(ax3)
dur_colors = [RED, YELLOW, ACCENT, GREEN, PINK]
q8_clean = q8.dropna(subset=['duration_category'])
bars3 = ax3.bar(range(len(q8_clean)), q8_clean['conversion_pct'],
                color=dur_colors[:len(q8_clean)], edgecolor='none', width=0.6)
for b, v in zip(bars3, q8_clean['conversion_pct']):
    ax3.text(b.get_x()+b.get_width()/2, v+0.3, f'{v:.1f}%',
             ha='center', fontsize=9, color=TEXT, fontweight='bold')
ax3.set_xticks(range(len(q8_clean)))
ax3.set_xticklabels([str(x) for x in q8_clean['duration_category']],
                    rotation=15, fontsize=8)
ax3.set_title('Q8: Conversion Rate by Call Duration', fontweight='bold', fontsize=11)
ax3.set_ylabel('Conversion Rate %')

# Previous outcome impact
ax4 = fig.add_subplot(gs[1, 1])
sax(ax4)
p_colors = {'failure': RED, 'nonexistent': MUTED, 'success': GREEN}
pout_c = [p_colors.get(p, ACCENT) for p in q6['previous_outcome']]
bars4 = ax4.bar(q6['previous_outcome'], q6['conversion_pct'],
                color=pout_c, edgecolor='none', width=0.5)
for b, v in zip(bars4, q6['conversion_pct']):
    ax4.text(b.get_x()+b.get_width()/2, v+0.3, f'{v:.1f}%',
             ha='center', fontsize=11, color=TEXT, fontweight='bold')
ax4.set_title('Q6: Conversion by Previous Campaign Outcome', fontweight='bold', fontsize=11)
ax4.set_ylabel('Conversion Rate %')

plt.savefig('outputs/sql_analysis.png', dpi=150, bbox_inches='tight', facecolor=BG)
print("[OK] Saved: outputs/sql_analysis.png")
print("\n[DONE] SQL analysis complete!")
print(f"  Engine used: {'MySQL' if USE_MYSQL else 'SQLite (MySQL not connected)'}")
