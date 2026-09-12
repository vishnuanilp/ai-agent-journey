from speak2 import check_script

cases = [
    ("Breakfast starts at eight.", "en"),
    ("പ്രഭാതഭക്ഷണം എട്ട് മണിക്ക്", "ml"),
    ("नाश्ता आठ बजे शुरू होता है", "hi"),
    ("காலை உணவு எட்டு மணிக்கு", "ta"),
    ("Breakfast starts at eight.", "ml"),
    ("നമസ്കാരം", "hi"),
]

for text, lang in cases:
    check_script(text, lang)