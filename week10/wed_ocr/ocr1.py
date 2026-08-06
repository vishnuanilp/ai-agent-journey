from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract-OCR\tesseract.exe"

img = Image.open("frames/clean_text.jpg")
print("size:", img.size, "mode:", img.mode)

text = pytesseract.image_to_string(img)

print("----- RAW -----")
print(repr(text))
print("----- READABLE -----")
print(text)