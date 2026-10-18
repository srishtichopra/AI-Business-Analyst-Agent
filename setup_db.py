
import duckdb
from pathlib import Path

DATA_DIR = Path("data")
DB_PATH = "olist.duckdb"
SKIP = {"geolocation"}


def table_name(path):
    return path.stem.replace("olist_", "").replace("_dataset", "")


def main():
    con = duckdb.connect(DB_PATH)
    for csv in sorted(DATA_DIR.glob("*.csv")):
        name = table_name(csv)
        if name in SKIP:
            continue
        con.execute(
            f"CREATE OR REPLACE TABLE {name} AS "
            f"SELECT * FROM read_csv_auto('{csv.as_posix()}')"
        )
        count = con.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
        print(name, count)
    con.close()


if __name__ == "__main__":
    main()