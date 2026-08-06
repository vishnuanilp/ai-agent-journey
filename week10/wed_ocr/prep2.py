from PIL import Image
import pytesseract, time

pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract-OCR\tesseract.exe"
grey = Image.open("frames/step1_grey.jpg")

for factor in [1, 2, 3, 4]:
    w, h = grey.size
    big = grey.resize((w * factor, h * factor), Image.LANCZOS)
    start = time.time()
    text = pytesseract.image_to_string(big)
    secs = time.time() - start
    hits = sum(a in text for a in ["ALDI", "1,25", "250 G", "10,76", "1KG"])
    print(f"{factor}x  {big.size}  {secs:.1f}s  anchors {hits}/5")
    big.save(f"frames/step2_{factor}x.jpg")