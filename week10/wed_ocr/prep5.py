from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract-OCR\tesseract.exe"
ANCHORS = ["ALDI", "1,25", "0,75", "10,76", "1KG", "10,20"]
grey = Image.open("frames/step1_grey.jpg")

for cut in [100, 128, 150, 170, 190]:
    bw = grey.point(lambda p: 255 if p >= cut else 0).convert("1")
    text = pytesseract.image_to_string(bw)
    missing = [a for a in ANCHORS if a not in text]
    print(f"cut {cut}  {6-len(missing)}/6  missing: {missing}")
    bw.save(f"frames/step4_t{cut}.jpg")