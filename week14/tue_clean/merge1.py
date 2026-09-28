import pandas as pd

orders = pd.DataFrame({"order": [1, 2, 3], "dish_id": ["D1", "D2", "D9"], "qty": [2, 1, 1]})
menu = pd.DataFrame({"dish_id": ["D1", "D2", "D3"],
                     "name": ["dosa", "biryani", "payasam"], "price": [80, 220, 60]})

inner = pd.merge(orders, menu, on="dish_id")
left = pd.merge(orders, menu, on="dish_id", how="left", indicator=True)

print("orders:", len(orders), " inner:", len(inner), " left:", len(left))
print("\n--- inner ---")
print(inner)
print("\n--- left, with where each row came from ---")
print(left)