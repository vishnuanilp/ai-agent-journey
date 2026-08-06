from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract-OCR\tesseract.exe"

img = Image.open("frames/clean_text.jpg")
data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

print("keys:", list(data.keys()))
print("rows:", len(data["text"]))

for word, conf in zip(data["text"], data["conf"]):
    if word.strip():
        print(f"{conf:>6}  {word}")