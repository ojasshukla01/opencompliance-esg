import duckdb

con = duckdb.connect("data/esg_transformed.duckdb")
result = con.execute("SELECT COUNT(*) FROM esg_cleaned").fetchall()

print(f"✅ Table 'esg_cleaned' has {result[0][0]} rows.")
