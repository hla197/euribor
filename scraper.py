import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path


SOURCE_URL = "https://mutuionline.24oreborsaonline.ilsole24ore.com/guide-mutui/euribor.asp"
HEADER = [
    "reference_date",
    "index_name",
    "value_eur365",
    "source_url",
    "extraction_timestamp",
]


def read_rows(path):
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open("r", newline="", encoding="utf-8-sig") as fp:
        return list(csv.DictReader(fp))


def write_rows(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as fp:
        writer = csv.DictWriter(fp, fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(rows)


def upsert_row(path, row):
    rows = read_rows(path)
    rows = [item for item in rows if item.get("reference_date") != row["reference_date"]]
    rows.append(row)
    rows.sort(key=lambda item: item["reference_date"])
    write_rows(path, rows)


def main():
    parser = argparse.ArgumentParser(description="GitHub Actions demo Euribor CSV updater.")
    parser.add_argument("--output", default="euribor_rates.csv")
    parser.add_argument("--reference-date", default="2026-06-30")
    parser.add_argument("--value", default="2.36")
    args = parser.parse_args()

    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    row = {
        "reference_date": args.reference_date,
        "index_name": "Euribor 3M",
        "value_eur365": args.value,
        "source_url": SOURCE_URL,
        "extraction_timestamp": now,
    }

    output_path = Path(args.output)
    upsert_row(output_path, row)
    print(f"Updated {output_path} with reference_date={row['reference_date']}")


if __name__ == "__main__":
    main()
