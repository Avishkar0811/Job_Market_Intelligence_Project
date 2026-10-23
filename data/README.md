# Data folder

The full dataset is **not stored in this repository**. Its provenance and licence have not been verified, and the cleaned files are large (the raw file is about 57 MB and the cleaned file about 83 MB).

| Path | Contents | In Git? |
|---|---|---|
| `data/raw/jobs_original.csv` | Supplied source file (100,000 rows, 33 columns) | No (ignored) |
| `data/sample/jobs_sample.csv` | Random 1,000-row excerpt (seed 42) with the same columns, for trying the pipeline | Yes |
| `data/processed/jobs_cleaned.csv` | Output of `python/clean_jobs_data.py` | No (ignored, regenerate) |
| `data/processed/powerbi_*.csv` | Output of `python/prepare_powerbi_data.py` | No (ignored, regenerate) |
| `data/processed/jobs_oracle_import.csv` | Output of `python/prepare_oracle_csv.py` | No (ignored, regenerate) |
| `data/processed/*_counts.csv`, `salary_by_role_currency.csv` | Small summaries from `python/analyze_jobs.py` | Yes |

## Run the pipeline with the sample

```bash
cp data/sample/jobs_sample.csv data/raw/jobs_original.csv
python python/clean_jobs_data.py
```

On Windows PowerShell use `Copy-Item data\sample\jobs_sample.csv data\raw\jobs_original.csv`. Results on the 1,000-row sample will differ from the figures in the README and report, which come from the full 100,000-row file.

## Use the full dataset

Place your own copy of the full file at `data/raw/jobs_original.csv`, then run the scripts in the order given in the main README. Confirm the source and licence before sharing the data publicly.
