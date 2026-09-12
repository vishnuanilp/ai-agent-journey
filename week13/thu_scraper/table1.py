from bs4 import BeautifulSoup

html = """
<table>
<tr><th>Item</th><th>Price</th></tr>
<tr><td>Rice 5kg</td><td>320</td></tr>
<tr><td>Sugar 1kg</td><td>45</td></tr>
</table>
"""

soup = BeautifulSoup(html, "html.parser")

for tr in soup.find_all("tr"):
    cells = tr.find_all(["th", "td"])
    row = [c.get_text(separator=" ", strip=True) for c in cells]
    print(row)