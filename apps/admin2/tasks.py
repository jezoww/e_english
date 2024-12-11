import os

from celery import shared_task
import pandas as pd
from django.core.cache import cache
from django.utils.text import slugify
from gtts import gTTS

from apps.user.models import Vocabulary


@shared_task
def create_vocab_from_excel(file_path, unit_id):
    # Faylni o‘qish
    try:
        data = pd.read_excel(file_path)
    except FileNotFoundError:
        return 'File not found'

    # Ustunlarni tekshirish
    if 'eng' not in data.columns or 'uz' not in data.columns:
        return 'undefined column'

    # Ma’lumotlarni qayta ishlash
    for _, row in data.iterrows():
        english_word = row['eng']
        uzbek_word = row['uz']
        if pd.isna(english_word) or pd.isna(uzbek_word):
            continue
        # Audio fayl yaratish
        audio_path = f"/home/jezow/pythonn/e_english/media/vocabulary_audio/{slugify(english_word)}_to_{slugify(uzbek_word)}.mp3"
        tts = gTTS(text=english_word, lang='en')
        tts.save(audio_path)
        audio_path = f"vocabulary_audio/{slugify(english_word)}_to_{slugify(uzbek_word)}.mp3"

        Vocabulary.objects.create(
            uzbek=uzbek_word,
            english=english_word,
            unit_id=unit_id,
            audio=audio_path
        )
    os.remove(file_path)
    cache.clear()
    return 'success'
