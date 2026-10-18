import duckdb

con = duckdb.connect("olist.duckdb", read_only=True)

for table in ["orders", "order_items", "order_payments", "products", "customers", "order_reviews"]:
    print("\n" + table)
    print(con.execute(f"DESCRIBE {table}").fetchdf()[["column_name", "column_type"]])