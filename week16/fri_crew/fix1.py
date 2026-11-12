import sys, runpy
from hotel_crew import find

find.description = ("Guest asks: {question}\n"
    "Search the hotel documents and copy the policy text about this topic, "
    "even if it says no or sets a limit. "
    "Write NOT FOUND only if no returned text is about the topic.")
find._original_description = None
print("FIX: researcher task text swapped")
runpy.run_path("ask3.py", run_name="__main__")
