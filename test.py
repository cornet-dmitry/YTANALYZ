from googletrans import Translator


translator = Translator()

videoTitle = "Stromae - Multitude, le film (Full concert)"

translator = Translator()
translation = translator.translate("Der Himmel ist blau und ich mag Bananen", dest='ru')
print(translation.text)

# Перевод названия видео на русский язык
try:
    translated_title = translator.translate(videoTitle, src='auto', dest='ru').text

except Exception as e:
    translated_title = videoTitle  # Если перевод не удался, оставляем оригинал
    print(f"Ошибка при переводе: {e}")

print(translated_title)