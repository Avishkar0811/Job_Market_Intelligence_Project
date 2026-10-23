# Job Market Intelligence & Skills Analysis

**Author:** Avishkar Padhen

## Abstract
This project demonstrates a reproducible data-analysis workflow for exploring job-posting records, extracting skill mentions, summarizing roles, locations, salaries and applicant competition, and preparing the data for Oracle SQL, Python charts and a Power BI dashboard. The analysis covers a supplied dataset of 100,000 postings dated 1 January to 30 May 2026, with a focus on entry-level (fresher) IT roles in India.

## Objectives
- Inspect and clean a job-posting dataset using Python and Pandas.
- Explore job titles, locations, experience levels, work modes, and skill mentions.
- Summarize salary ranges while keeping currencies separate.
- Store selected fields in Oracle and analyze them with SQL.
- Build static charts in Python and an interactive Power BI report with KPI cards, charts, and slicers.

## Tools
Python, Pandas, NumPy, Matplotlib, Oracle SQL, Visual Studio Code, Power BI Desktop (Power Query and DAX).

## Methodology
1. Keep the supplied source file in `data/raw/` (not committed to the repository).
2. Run `python/clean_jobs_data.py` to create a cleaned dataset (`jobs_cleaned.csv`).
3. Run `python/analyze_jobs.py` to create summary CSVs.
4. Use `sql/create_jobs_real.sql` to create the Oracle table and `sql/job_market_analysis.sql` for analysis; `python/prepare_oracle_csv.py` prepares the import file.
5. Run `python/prepare_powerbi_data.py` to create a Power BI fact table (`powerbi_jobs.csv`, salaries in LPA) and a skills table (`powerbi_job_skills.csv`, one row per posting and skill), then build the model and dashboard as described in `powerbi/POWER_BI_GUIDE.md`.
6. Run `python/create_visualizations.py` to create seven static charts in `visuals/`.
7. Validate dashboard KPIs against the source data and document data-quality limitations before presenting conclusions.

## Data quality and limitations
The included dataset file is labelled as a 2026 Indian technology career-intelligence dataset. Its provenance, license, collection method, and whether individual rows represent genuine live job postings have not been independently verified as part of this project. Therefore, do not describe its rows as verified live listings or present the resulting counts as authoritative labor-market statistics. Confirm the source page and license before public redistribution. Skill frequencies measure mentions in the supplied data, not necessarily skill demand across the entire market.

### Profiling results
- **Size:** 100,000 rows and 33 raw columns; the cleaned file has 41 columns because it adds a salary midpoint, a plain-text job description and backward-compatible alias columns for the SQL and Power BI steps.
- **Duplicates:** none.
- **Missing values:** only `probation_period` has gaps (33,499 rows, 33.5%); it is shown as "Not specified" in the Power BI table.
- **Dates:** posted dates run from 2026-01-01 to 2026-05-30. Dates in the raw file are day-first (for example 14-02-2026) and are parsed accordingly.
- **Currency:** all salaries are in INR, so salary figures are comparable and are shown in lakhs per annum (LPA).

### Patterns that suggest the data may be generated
- Salaries, applicant counts, cities, work modes and platforms are spread almost perfectly evenly.
- Every fresher role is "Contractual" and every mid-senior role is "Permanent".
- Each job category lists a fixed set of skills, so skill demand mirrors category demand.

For this reason the project demonstrates the analysis method rather than real market trends.

## Results
All figures describe the supplied dataset.

- **Postings:** 100,000, of which 40,129 (40.1%) are entry-level and 59,871 are mid-senior. About 85% are marked active.
- **Categories:** six categories of similar size, from 16,425 (Data Science) to 16,872 (Web Development) postings.
- **Titles:** 24 distinct job titles. The most frequent are Cloud Infrastructure Intern (5,626), Azure Cloud Engineer (5,596) and AWS Solutions Architect (5,560).
- **Locations:** eight cities, each with 12,372 to 12,636 postings (Chennai highest, Bangalore lowest).
- **Companies:** twelve companies with 8,160 to 8,517 postings each (HCLTech highest).
- **Work mode:** Remote 40.0%, Hybrid 39.7%, On-site 20.3%.
- **Salary (INR, annual):** the average salary midpoint is about 8.5 LPA, with individual postings ranging from about 3 to 18 LPA (average minimum 4.5, average maximum 12.5). Averages barely differ by category, company type or experience level.
- **Stipend:** about INR 30,000 per month on average across the dataset, with little difference between roles.
- **Applicants:** about 247 per posting; roles range from about 244 to 252.
- **Skills:** 39 distinct skills across 683,648 posting-skill pairs. Python and Linux lead (about 33,000 postings each) because each appears in two categories.
- **Interview difficulty:** about 60% Medium, 20% Easy and 20% Hard in every category.

## Dashboard insights (Power BI)
The dashboard has three pages: **Market Overview** (KPIs, jobs by category, month, city, work mode and company), **Skills Analysis** (top 10 skills, skill-by-category heatmap, skills per job) and **Salary & Opportunity** (salary range, fresher stipends, competition versus salary, interview difficulty, role table). Screenshots are in the main README.

1. 40.1% of postings are entry-level; the Fresher view shows 40,129 jobs.
2. Posting volume is steady at roughly 660 to 670 postings per day (all roles); the February dip reflects the shorter month.
3. About 80% of postings are remote or hybrid.
4. Salary, competition and interview difficulty barely vary across categories, so the Opportunity Score ranks roles on very small differences and should be read as illustrative.
5. Dashboard KPIs (total jobs, applicants per job, average salary, fresher share, salary range, stipend and hard-interview share) were checked against calculations from the source file and matched.

## Conclusion
The project shows an end-to-end workflow from raw CSV processing to SQL analysis, Python charts and Power BI visualization. Conclusions remain limited to the supplied dataset and its unverified provenance; the near-uniform distributions mean the results illustrate the analysis method more than real labor-market behaviour.
