# Euribor GitHub Actions Demo

This is a minimal GitHub Actions demo for a scheduled Python scraper.

The demo script writes one idempotent row to `euribor_rates.csv`:

```csv
reference_date,index_name,value_eur365,source_url,extraction_timestamp
2026-06-30,Euribor 3M,2.36,https://mutuionline.24oreborsaonline.ilsole24ore.com/guide-mutui/euribor.asp,2026-07-27T09:00:00Z
```

## Run Locally

```powershell
python .\scraper.py --output euribor_rates.csv
```

## GitHub Actions

Workflow file:

```text
.github/workflows/euribor-demo.yml
```

It runs:

- Every Monday at 09:00 UTC
- Manually from the GitHub Actions page via `workflow_dispatch`

After running, it commits the updated `euribor_rates.csv` back to the repository.

## Change Schedule

Edit the cron expression in `.github/workflows/euribor-demo.yml`:

```yaml
schedule:
  - cron: "0 9 * * 1"
```

Examples:

- Weekly Monday 09:00 UTC: `0 9 * * 1`
- Monthly on the 1st at 09:00 UTC: `0 9 1 * *`

## Next Step

Replace the demo values in `scraper.py` with the real Euribor extraction logic.
