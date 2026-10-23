"""Clean the raw job-market dataset and create a processed CSV."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = ROOT / "data" / "raw" / "jobs_original.csv"
OUT_FILE = ROOT / "data" / "processed" / "jobs_cleaned.csv"

if not RAW_FILE.exists():
    raise FileNotFoundError(f"Raw dataset not found: {RAW_FILE}")

df = pd.read_csv(RAW_FILE, low_memory=False)
df.columns = [str(c).strip() for c in df.columns]

text_columns = [
    "job_title", "job_category", "company_name", "location_city",
    "location_state", "location_country", "work_mode", "experience_level",
    "experience_required", "employment_type", "contract_type", "skills_extracted",
    "salary_currency", "source_platform", "technical_domain",
]
for col in text_columns:
    if col in df.columns:
        df[col] = df[col].astype("string").str.strip()

for col in ["salary_minimum", "salary_maximum", "stipend_amount", "skill_count", "applicant_count"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

for col in ["posted_date", "application_deadline"]:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)

if {"salary_minimum", "salary_maximum"}.issubset(df.columns):
    df["salary_midpoint"] = (df["salary_minimum"] + df["salary_maximum"]) / 2

# Backwards-compatible aliases for the earlier SQL and Power BI steps.
for new_col, old_col in {
    "title": "job_title", "location": "location_city", "experience": "experience_level",
    "salary_min": "salary_minimum", "salary_max": "salary_maximum",
    "skills": "skills_extracted",
}.items():
    if old_col in df.columns:
        df[new_col] = df[old_col]

if "job_description" in df.columns:
    df["job_description_text"] = (
        df["job_description"].fillna("").astype(str)
        .str.replace(r"<[^>]+>", " ", regex=True)
        .str.replace(r"\s+", " ", regex=True).str.strip()
    )
if "is_active" in df.columns:
    df["is_active"] = (
        df["is_active"].astype("string").str.strip().str.lower()
        .map({"true": True, "false": False, "1": True, "0": False})
        .astype("boolean")
    )

OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUT_FILE, index=False, date_format="%Y-%m-%d")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print(f"Saved: {OUT_FILE}")
if "salary_currency" in df.columns:
    print("Salary currency counts:\n", df["salary_currency"].value_counts(dropna=False).to_string())
if set(["job_title", "location_city", "salary_minimum", "salary_maximum"]).issubset(df.columns):
    print("Missing values in key columns:\n", df[["job_title", "location_city", "salary_minimum", "salary_maximum"]].isna().sum().to_string())
