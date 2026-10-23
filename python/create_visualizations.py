"""Create static charts (PNG) from data/processed/jobs_cleaned.csv.

Usage (from the project root):
    python python/create_visualizations.py              # entry-level (fresher) roles
    python python/create_visualizations.py --all-roles  # all 100,000 postings

Charts are saved in the visuals/ folder. All figures describe the supplied
dataset only, not verified market-wide statistics.
"""
import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "processed" / "jobs_cleaned.csv"
OUT = ROOT / "visuals"

TEAL, NAVY, AMBER, RED, BLUE = "#13A89E", "#0B2545", "#F2A541", "#E4572E", "#5C80BC"
FRESHER = "Freshers / Entry Level"

plt.rcParams.update({
    "figure.dpi": 130, "savefig.dpi": 160, "font.family": "DejaVu Sans",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.titlesize": 13, "axes.titleweight": "bold", "axes.titlecolor": NAVY,
    "axes.labelsize": 10, "xtick.labelsize": 9, "ytick.labelsize": 9,
})


def save(fig, name, scope_label):
    fig.text(0.01, 0.005, f"Source: supplied dataset ({scope_label}), Jan to May 2026. "
             "Analysis of the dataset only, not verified market-wide statistics.",
             fontsize=7, color="#52606D", ha="left", va="bottom")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(OUT / name, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", name)


def bar_labels(ax, fmt="{:,.0f}", pad=3):
    for c in ax.containers:
        ax.bar_label(c, fmt=lambda v: fmt.format(v), padding=pad, fontsize=8)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--all-roles", action="store_true", help="use all experience levels")
    args = parser.parse_args()

    if not INPUT.exists():
        raise FileNotFoundError("Run python/clean_jobs_data.py first.")
    OUT.mkdir(exist_ok=True)

    df = pd.read_csv(INPUT, low_memory=False)
    if df["salary_currency"].nunique() != 1 or df["salary_currency"].iloc[0] != "INR":
        raise ValueError("Expected a single INR currency.")
    df["posted_date"] = pd.to_datetime(df["posted_date"])
    scope = df if args.all_roles else df[df["experience_level"] == FRESHER]
    label = f"{'all roles' if args.all_roles else 'freshers / entry level'}, {len(scope):,} postings"

    # 1. Jobs by category
    s = scope["job_category"].value_counts().sort_values()
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.barh(s.index, s.values, color=TEAL)
    bar_labels(ax)
    ax.set(title="Jobs by category", xlabel="Postings")
    ax.set_xlim(0, s.max() * 1.12)
    save(fig, "01_jobs_by_category.png", label)

    # 2. Monthly postings and postings per day
    # Days observed = first to last posting date within each month (the last month may be partial).
    m = scope.groupby(scope["posted_date"].dt.to_period("M")).agg(
        jobs=("posted_date", "size"), first=("posted_date", "min"), last=("posted_date", "max"))
    m["days"] = (m["last"] - m["first"]).dt.days + 1
    m["per_day"] = m["jobs"] / m["days"]
    names = [p.strftime("%b") for p in m.index]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.8))
    a1.bar(names, m["jobs"], color=TEAL)
    bar_labels(a1)
    a1.set(title="Postings per month", ylabel="Postings")
    a2.plot(names, m["per_day"], marker="o", color=NAVY)
    for x, y in zip(names, m["per_day"]):
        a2.annotate(f"{y:,.0f}", (x, y), textcoords="offset points", xytext=(0, 7), ha="center", fontsize=8)
    a2.set(title="Postings per calendar day", ylabel="Postings per day")
    a2.set_ylim(0, m["per_day"].max() * 1.25)
    save(fig, "02_monthly_postings.png", label)

    # 3. Work mode share
    w = scope["work_mode"].value_counts(normalize=True).mul(100).sort_values()
    fig, ax = plt.subplots(figsize=(6, 3.2))
    ax.barh(w.index, w.values, color=[AMBER if i == "On-site" else TEAL for i in w.index])
    bar_labels(ax, "{:.1f}%")
    ax.set(title="Work mode share", xlabel="% of postings")
    ax.set_xlim(0, w.max() * 1.15)
    save(fig, "03_work_mode.png", label)

    # 4. Top 10 skills
    sk = scope["skills_extracted"].str.split(r"\s*,\s*").explode().value_counts().head(10).sort_values()
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.barh(sk.index, sk.values, color=TEAL)
    bar_labels(ax)
    ax.set_title("Top 10 skills in demand", pad=20)
    ax.set(xlabel="Postings mentioning the skill")
    ax.set_xlim(0, sk.max() * 1.12)
    ax.text(0.5, 1.02, "Skills are tied to job categories in this dataset", transform=ax.transAxes,
            fontsize=8, color="#52606D", ha="center")
    save(fig, "04_top_skills.png", label)

    # 5. Salary range by category (LPA)
    g = scope.groupby("job_category").agg(mn=("salary_minimum", "mean"), mx=("salary_maximum", "mean")) / 1e5
    g = g.sort_values("mx", ascending=False)
    fig, ax = plt.subplots(figsize=(8, 4))
    x = range(len(g))
    ax.bar([i - 0.2 for i in x], g["mn"], 0.4, label="Avg minimum", color=BLUE)
    ax.bar([i + 0.2 for i in x], g["mx"], 0.4, label="Avg maximum", color=NAVY)
    bar_labels(ax, "{:.1f}")
    ax.set_xticks(list(x), g.index, rotation=20, ha="right")
    ax.set(title="Salary range by category (LPA)", ylabel="LPA")
    ax.legend(frameon=False)
    save(fig, "05_salary_range.png", label)

    # 6. Interview difficulty by category (100% stacked)
    d = pd.crosstab(scope["job_category"], scope["interview_difficulty"], normalize="index").mul(100)
    d = d[["Easy", "Medium", "Hard"]].sort_index(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 4))
    left = pd.Series(0.0, index=d.index)
    for col, colr in [("Easy", TEAL), ("Medium", AMBER), ("Hard", RED)]:
        ax.barh(d.index, d[col], left=left, color=colr, label=col)
        for i, (v, l) in enumerate(zip(d[col], left)):
            ax.text(l + v / 2, i, f"{v:.0f}%", ha="center", va="center", fontsize=8, color="white")
        left += d[col]
    ax.set(title="Interview difficulty by category", xlabel="% of postings", xlim=(0, 100))
    ax.legend(ncol=3, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.15))
    save(fig, "06_interview_difficulty.png", label)

    # 7. Competition vs salary by role
    r = scope.groupby("job_title").agg(app=("applicant_count", "mean"), sal=("salary_midpoint", "mean"))
    r["sal"] /= 1e5
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.scatter(r["app"], r["sal"], color=TEAL, s=45)
    ax.axvline(scope["applicant_count"].mean(), color=NAVY, linestyle="--", linewidth=1)
    ax.set_title("Competition vs salary by role", pad=20)
    ax.set(xlabel="Average applicants per posting", ylabel="Average salary midpoint (LPA)")
    ax.text(0.5, 1.02, f"Axes zoomed in: roles differ by {r['sal'].max() - r['sal'].min():.2f} LPA "
            f"and {r['app'].max() - r['app'].min():.0f} applicants", transform=ax.transAxes,
            fontsize=8, color="#52606D", ha="center")
    save(fig, "07_competition_vs_salary.png", label)


if __name__ == "__main__":
    main()
