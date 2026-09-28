import pandas as pd

orders = pd.DataFrame({"order": [1, 2, 3], "dish_id": ["D1", "D2", "D1"], "qty": [2, 1, 1]})
menu = pd.DataFrame({"dish_id": ["D1", "D2", "D1"], "price": [80, 220, 90]})

m = pd.merge(orders, menu, on="dish_id")
print("orders:", len(orders), " merged:", len(m))
print(m)
print("revenue:", (m["qty"] * m["price"]).sum())

print("\nduplicate keys in menu:\n", menu[menu["dish_id"].duplicated(keep=False)])

try:
    pd.merge(orders, menu, on="dish_id", validate="many_to_one")
except pd.errors.MergeError as e:
    print("\nvalidate stopped:", str(e).splitlines()[0])