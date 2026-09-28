tools = [{"type": "function", "function": {
    "name": "job_mail",
    "description": "Counts job-hunt emails from jobs.csv, weekdays on Paris time. by='day' gives emails per weekday, by='sender' gives emails per sender.",
    "parameters": {"type": "object", "properties": {"by": {"type": "string", "enum": ["day", "sender"]}}, "required": ["by"]}}}]