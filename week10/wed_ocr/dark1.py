from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract-OCR\tesseract.exe"

img = Image.open("frames/dark_person.jpg")
grey = img.convert("L")
print("size:", grey.size)

text = pytesseract.image_to_string(grey)
print("----- RAW -----")
print(repr(text))

data = pytesseract.image_to_data(grey, output_type=pytesseract.Output.DICT)
words = [(w, c) for w, c in zip(data["text"], data["conf"]) if w.strip()]
print("words found:", len(words))
for w, c in words:
    print(f"{c:>6}  {w}")