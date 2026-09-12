from listen import listen
from urlcheck import check_url

text, lang = listen("clinic.wav")
print("HEARD   :", text)
print("LANG    :", lang)
ok, why = check_url(text)
print("URLCHECK:", ok, "|", why)