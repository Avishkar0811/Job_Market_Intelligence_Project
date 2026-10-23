"""Create simple summary CSVs for Power BI and project analysis."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "processed" / "jobs_cleaned.csv"
OUT = ROOT / "data" / "processed"
if not INPUT.exists():
    raise FileNotFoundError("Run python/clean_jobs_data.py first.")
df = pd.read_csv(INPUT, low_memory=False)

# Role and location summaries
if "job_title" in df:
    df["job_title"].value_counts(dropna=False).rename_axis("job_title").reset_index(name="posting_count").to_csv(OUT / "role_counts.csv", index=False)
if "location_city" in df:
    df["location_city"].value_counts(dropna=False).rename_axis("location_city").reset_index(name="posting_count").to_csv(OUT / "location_counts.csv", index=False)

# Salary summary is grouped by currency so unlike currencies are never combined.
needed = {"job_title", "salary_minimum", "salary_maximum", "salary_currency"}
if needed.issubset(df.columns):
    salary = df.dropna(subset=["salary_minimum", "salary_maximum", "salary_currency"]).copy()
    salary = salary[(salary["salary_minimum"] >= 0) & (salary["salary_maximum"] >= salary["salary_minimum"])]
    salary["salary_midpoint_calc"] = (salary["salary_minimum"] + salary["salary_maximum"]) / 2
    salary.groupby(["salary_currency", "job_title"], dropna=False).agg(
        posting_count=("job_title", "size"),
        average_salary_minimum=("salary_minimum", "mean"),
        average_salary_maximum=("salary_maximum", "mean"),
        average_salary_midpoint=("salary_midpoint_calc", "mean"),
    ).reset_index().to_csv(OUT / "salary_by_role_currency.csv", index=False)

# Split comma/semicolon/pipe-delimited extracted skills into a frequency table.
if "skills_extracted" in df:
    skills = df["skills_extracted"].dropna().astype(str).str.split(r"[,;|]").explode().str.strip()
    skills = skills[skills.ne("") & skills.str.lower().ne("nan")]
    skills.value_counts().rename_axis("skill").reset_index(name="mention_count").to_csv(OUT / "skill_counts.csv", index=False)
print("Analysis outputs saved in data/processed/")
