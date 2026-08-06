from PIL import Image, ImageEnhance
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract-OCR\tesseract.exe"
ANCHORS = ["ALDI", "1,25", "0,75", "10,76", "1KG", "10,20"]
grey = Image.open("frames/step1_grey.jpg")

for level in [1.0, 1.5, 2.0, 3.0]:
    out = ImageEnhance.Contrast(grey).enhance(level)
    text = pytesseract.image_to_string(out)
    missing = [a for a in ANCHORS if a not in text]
    print(f"{level}  {len(ANCHORS)-len(missing)}/{len(ANCHORS)}  missing: {missing}")
    out.save(f"frames/step3_c{level}.jpg")