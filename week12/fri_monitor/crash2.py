# crash2.py — the same crash, but it leaves the machine
import os
import sentry_sdk
from dotenv import load_dotenv

load_dotenv()
sentry_sdk.init(dsn=os.getenv("SENTRY_DSN"))

def get_price(menu, item):
    return menu[item]

menu = {"biryani": 180, "porotta": 15}
print("Restaurant order system starting...")
print("Fish curry costs:", get_price(menu, "fish curry"))