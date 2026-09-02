from limiter import sb

r = sb.table("audit_log").select("*").order("id", desc=True).limit(8).execute()
for row in r.data:
    print(row["id"], row["user_id"], row["action"], "|", row["outcome"], "| ms:", row["ms"])