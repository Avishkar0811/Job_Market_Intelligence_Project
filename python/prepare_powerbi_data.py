"""Prepare Power BI-ready tables from data/processed/jobs_cleaned.csv.

Creates two tables for a star-style model:
  - powerbi_jobs.csv        one row per posting (slim, typed, salary in LPA)
  - powerbi_job_skills.csv  one row per posting and skill (skills split out)
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "processed" / "jobs_cleaned.csv"
OUT = ROOT / "data" / "processed"

if not INPUT.exists():
    raise FileNotFoundError("Run python/clean_jobs_data.py first.")

df = pd.read_csv(INPUT, low_memory=False)
df.insert(0, "job_id", range(1, len(df) + 1))

# Salaries are all INR per year in this dataset; show them in lakhs per annum (LPA).
if df["salary_currency"].nunique() != 1 or df["salary_currency"].iloc[0] != "INR":
    raise ValueError("Expected a single INR currency; convert or filter before using LPA.")
for src, dst in [("salary_minimum", "salary_min_lpa"),
                 ("salary_maximum", "salary_max_lpa"),
                 ("salary_midpoint", "salary_mid_lpa")]:
    df[dst] = (df[src] / 100_000).round(2)

df["career_growth_pct"] = df["career_growth_index"].astype(str).str.rstrip("%").astype(float) / 100
df["probation_period"] = df["probation_period"].fillna("Not specified")
df["is_fresher_role"] = df["experience_level"].eq("Freshers / Entry Level")

keep = [
    "job_id", "job_title", "job_category", "technical_domain", "company_name",
    "company_type", "company_size", "location_city", "location_state", "work_mode",
    "experience_level", "is_fresher_role", "education_required", "contract_type",
    "salary_min_lpa", "salary_max_lpa", "salary_mid_lpa", "stipend_amount",
    "skill_count", "posted_date", "application_deadline", "source_platform",
    "applicant_count", "interview_difficulty", "probation_period", "is_active",
    "career_growth_pct",
]
df[keep].to_csv(OUT / "powerbi_jobs.csv", index=False)

skills = (
    df[["job_id", "skills_extracted"]]
    .assign(skill=df["skills_extracted"].astype(str).str.split(r"[,;|]"))
    .explode("skill")
)
skills["skill"] = skills["skill"].str.strip()
skills = skills[skills["skill"].ne("") & skills["skill"].str.lower().ne("nan")]
skills[["job_id", "skill"]].to_csv(OUT / "powerbi_job_skills.csv", index=False)

print(f"powerbi_jobs.csv: {len(df):,} rows")
print(f"powerbi_job_skills.csv: {len(skills):,} rows")
