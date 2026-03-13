"""
Marketing Campaign Performance Analysis — MASTER RUNNER
Runs all steps in order. Execute this file to build the full project.

Usage:
    python run_all.py
"""
import subprocess, sys, os, time

os.makedirs('data', exist_ok=True)
os.makedirs('outputs', exist_ok=True)

steps = [
    ("1/5  Generating synthetic marketing data...", "generate_data.py"),
    ("2/5  Running marketing KPI analysis...",      "analysis.py"),
    ("3/5  Creating marketing visualizations...",   "visualize.py"),
    ("4/5  Running bank campaign EDA...",           "bank_analysis.py"),
    ("5a/5 Creating bank visualizations...",        "bank_visualize.py"),
    ("5b/5 Training ML classification models...",   "bank_ml.py"),
]

print("=" * 60)
print("  MARKETING CAMPAIGN PERFORMANCE ANALYSIS")
print("  Full Project Pipeline")
print("=" * 60)

for msg, script in steps:
    print(f"\n  {msg}")
    t = time.time()
    result = subprocess.run([sys.executable, script], capture_output=True, text=True)
    elapsed = time.time() - t
    if result.returncode == 0:
        print(f"  ✅  Done ({elapsed:.1f}s)")
    else:
        print(f"  ❌  Error in {script}:")
        print(result.stderr[-500:])

print("\n" + "=" * 60)
print("  OUTPUTS GENERATED")
print("=" * 60)
for f in sorted(os.listdir('outputs')):
    size = os.path.getsize(f'outputs/{f}') / 1024
    print(f"  outputs/{f:<35} {size:>6.0f} KB")

print("\n  DATA FILES")
for f in sorted(os.listdir('data')):
    size = os.path.getsize(f'data/{f}') / 1024
    print(f"  data/{f:<39} {size:>6.0f} KB")

print("\n🎉  Project complete! All files ready.")
