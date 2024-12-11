import os

from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form, IntegerField, FileField
from gtts import gTTS

from apps.admin2.tasks import create_vocab_from_excel
from apps.user.models import Book, Unit, Vocabulary, TestSection, Test
from root import settings


class BookModelForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class UnitModelForm(ModelForm):
    class Meta:
        model = Unit
        exclude = 'book',

    #     fields = ['book_id', 'name', 'unit_num']  # Use the actual field names you want.
    #     labels = {'book_id': 'Select a Book'}
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['book_id'].queryset = Book.objects.all()

    def save(self, commit=True):
        unit = super(UnitModelForm, self).save(commit=False)
        unit.name = self.cleaned_data['name'].capitalize()
        book = Book.objects.get(pk=self.data['book_id'])
        unit.book = book
        unit.save()
        return unit


class VocabModelForm(ModelForm):
    class Meta:
        model = Vocabulary
        exclude = 'audio', 'unit',

    def save(self, commit=True):
        vocab = super(VocabModelForm, self).save(commit=False)
        english = vocab.english
        uzbek = vocab.uzbek
        unit_id = self.data['unit_id']
        path = f"/home/jezow/pythonn/e_english/media/vocabulary_audio/{english}_to_{uzbek}.mp3"
        tts = gTTS(text=english, lang='en')
        tts.save(path)
        audio_path = f"vocabulary_audio/{english}_to_{uzbek}.mp3"
        vocab.audio = audio_path
        vocab.unit_id = unit_id
        vocab.save()
        return vocab


class VocabExcelForm(Form):
    unit = IntegerField()
    excel = FileField(required=False)

    def clean_excel(self):
        excel = self.cleaned_data['excel']
        unit = self.data['unit_id']

        if not excel.name.endswith(('.xls', '.xlsx')):
            raise ValidationError('Please upload a valid Excel file.')
        tmp_dir = settings.TMP_DIR
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)

        file_path = os.path.join(tmp_dir, excel.name)
        with open(file_path, 'wb') as temp_file:
            for chunk in excel.chunks():
                temp_file.write(chunk)
                result = create_vocab_from_excel.delay(file_path, unit)
        if result == 'undefined column':
            raise ValidationError('Please add uz and eng columns.')
        return file_path


class TestSectionModelForm(ModelForm):
    class Meta:
        model = TestSection
        fields = '__all__'


class TestModelForm(ModelForm):
    class Meta:
        model = Test
        exclude = 'test_section',

    def save(self, commit=True):
        test_section_id = self.data['test_section_id']
        test = super().save(commit=False)
        test.test_section_id = test_section_id
        test.save()
        return test
