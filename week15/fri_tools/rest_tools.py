from langchain_core.tools import tool

TABLES = {"20:00": "free", "21:00": "full"}
MENU = {"biryani": "chicken, rice, onion", "dal": "lentils, ghee"}

@tool
def check_table(people: int, time: str) -> str:
    """Check if a table is free. time is 24-hour HH:MM, e.g. 20:00."""
    return TABLES.get(time, "closed")
@tool
def menu_search(dish: str) -> str:
    """Return the ingredients of one dish on the menu."""
    return MENU[dish.lower()]

TOOLS = [check_table, menu_search]