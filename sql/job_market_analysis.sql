-- Core SQL analysis for the JOBS_REAL table.
SELECT COUNT(*) AS total_postings FROM JOBS_REAL;

SELECT JOB_TITLE, COUNT(*) AS posting_count
FROM JOBS_REAL
GROUP BY JOB_TITLE
ORDER BY posting_count DESC;

SELECT LOCATION_CITY, COUNT(*) AS posting_count
FROM JOBS_REAL
GROUP BY LOCATION_CITY
ORDER BY posting_count DESC;

SELECT EXPERIENCE_LEVEL, COUNT(*) AS posting_count
FROM JOBS_REAL
GROUP BY EXPERIENCE_LEVEL
ORDER BY posting_count DESC;

-- Salary summaries: always group by currency; do not compare mixed currencies.
SELECT SALARY_CURRENCY, JOB_TITLE, COUNT(*) AS postings,
       ROUND(AVG(SALARY_MINIMUM), 2) AS avg_salary_minimum,
       ROUND(AVG(SALARY_MAXIMUM), 2) AS avg_salary_maximum
FROM JOBS_REAL
WHERE SALARY_MINIMUM IS NOT NULL
  AND SALARY_MAXIMUM IS NOT NULL
  AND SALARY_MAXIMUM >= SALARY_MINIMUM
GROUP BY SALARY_CURRENCY, JOB_TITLE
ORDER BY SALARY_CURRENCY, avg_salary_maximum DESC;

-- Work mode distribution.
SELECT WORK_MODE, COUNT(*) AS posting_count
FROM JOBS_REAL
GROUP BY WORK_MODE
ORDER BY posting_count DESC;

-- Skill frequency. Handles comma-, semicolon-, and pipe-delimited lists.
SELECT TRIM(REGEXP_SUBSTR(SKILLS_EXTRACTED, '[^,;|]+', 1, LEVEL)) AS skill,
       COUNT(*) AS mention_count
FROM JOBS_REAL
WHERE SKILLS_EXTRACTED IS NOT NULL
CONNECT BY REGEXP_SUBSTR(SKILLS_EXTRACTED, '[^,;|]+', 1, LEVEL) IS NOT NULL
       AND PRIOR JOB_ID = JOB_ID
       AND PRIOR SYS_GUID() IS NOT NULL
GROUP BY TRIM(REGEXP_SUBSTR(SKILLS_EXTRACTED, '[^,;|]+', 1, LEVEL))
ORDER BY mention_count DESC;

-- Top skills for each title is available by combining the skill query with JOB_TITLE.
-- Treat all findings as descriptive of this dataset, not verified live market demand.
