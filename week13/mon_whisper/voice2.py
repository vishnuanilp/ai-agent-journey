from listen import listen
from spoken import spoken_to_url
from urlcheck import check_url

text, lang = listen("url.wav")
print("HEARD   :", repr(text))
print("LANG    :", lang)

url = spoken_to_url(text)
print("URL     :", url)

ok, why = check_url(url)
print("URLCHECK:", ok, "|", why)