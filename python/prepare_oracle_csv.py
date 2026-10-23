"""Export only the columns expected by the Oracle JOBS_REAL table."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "processed" / "jobs_cleaned.csv"
OUTPUT = ROOT / "data" / "processed" / "jobs_oracle_import.csv"

if not INPUT.exists():
    raise FileNotFoundError(f"Cleaned dataset not found: {INPUT}. Run clean_jobs_data.py first.")

df = pd.read_csv(INPUT, low_memory=False)
columns = [
    "job_title", "job_category", "company_name", "location_city", "location_state",
    "location_country", "work_mode", "salary_minimum", "salary_maximum",
    "salary_currency", "experience_level", "experience_required", "skills_extracted", "posted_date",
]
missing = [c for c in columns if c not in df.columns]
if missing:
    raise ValueError(f"Missing required columns: {missing}")

out = df[columns].copy()
out["posted_date"] = pd.to_datetime(out["posted_date"], errors="coerce").dt.strftime("%Y-%m-%d")
out.to_csv(OUTPUT, index=False, encoding="utf-8")
print(f"Rows prepared: {len(out):,}")
print(f"Columns prepared: {len(out.columns)}")
print(f"Saved to: {OUTPUT}")
