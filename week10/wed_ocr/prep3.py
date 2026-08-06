from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract-OCR\tesseract.exe"
ANCHORS = ["ALDI", "1,25", "250 G", "10,76", "1KG"]

def score(path, label):
    text = pytesseract.image_to_string(Image.open(path))
    found = [a for a in ANCHORS if a in text]
    missing = [a for a in ANCHORS if a not in text]
    print(f"{label:<12} {len(found)}/5   missing: {missing}")

score("frames/clean_text.jpg", "colour")
score("frames/step1_grey.jpg", "grey")