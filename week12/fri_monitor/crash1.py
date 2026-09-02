# crash1.py — a crash with nobody watching
def get_price(menu, item):
    return menu[item]

menu = {"biryani": 180, "porotta": 15}

print("Restaurant order system starting...")
print("Biryani costs:", get_price(menu, "biryani"))
print("Fish curry costs:", get_price(menu, "fish curry"))
print("Order system still running...")