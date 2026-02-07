import duckdb
from pathlib import Path

con = duckdb.connect()

# Load fact table
con.execute("""
CREATE OR REPLACE TABLE fact_sales AS
SELECT * FROM read_csv_auto('analytics/final.csv');
""")

sql_dir = Path("analytics/sql")

output_dir = Path("analytics/results")
output_dir.mkdir(exist_ok=True)

for sql_file in sorted(sql_dir.glob("*.sql")):
    result = con.execute(sql_file.read_text()).fetchdf()
    output_path = output_dir / f"{sql_file.stem}.csv"
    result.to_csv(output_path, index=False)

