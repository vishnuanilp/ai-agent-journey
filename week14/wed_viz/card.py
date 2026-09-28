tools = [{"type": "function", "function": {
    "name": "sales_by_day",
    "description": "Shop sales per weekday from shop.csv. how='sum' gives money, how='count' gives number of sales.",
    "parameters": {"type": "object", "properties": {"how": {"type": "string", "enum": ["sum", "count"]}}, "required": ["how"]}}}]