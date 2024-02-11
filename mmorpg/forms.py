from django import forms
from django.core.exceptions import ValidationError

from .models import Ads


class AdsForm(forms.ModelForm):

    class Meta:
        model = Ads
        fields = ['title', 'text', 'category', 'media']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")

        if len(str(title)) < 5:
            raise ValidationError(
                "Заголовок не должен быть короче 5 символов."
            )

        if len(str(text)) < 20:
            raise ValidationError(
                "Текст не должен быть короче 20 символов."
            )

        if title == text:
            raise ValidationError(
                "Текст не должен быть идентичен заголовку."
            )

        return cleaned_data
