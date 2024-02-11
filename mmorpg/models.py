from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


class Ads(models.Model):
    CATEGORIES = [
        ('tanks', 'Танки'),
        ('heals', 'Хилы'),
        ('dd', 'ДД'),
        ('tradespeople', 'Торговцы'),
        ('guildmasters', 'Гилдмастеры'),
        ('questgivers', 'Квестгиверы'),
        ('blacksmiths', 'Кузнецы'),
        ('tanners', 'Кожевники'),
        ('potionmakers', 'Зельевары'),
        ('spellmasters', 'Мастера заклинаний'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    title = models.CharField("Заголовок", max_length=128)
    text = RichTextUploadingField("Текст")
    category = models.CharField("Категория объявления",
                                max_length=12,
                                choices=CATEGORIES,
                                default='tanks')
    media = models.FileField("Прикрепленные файлы", upload_to='uploads/', blank=True)
    date = models.DateTimeField("Дата объявления", auto_now_add=True)

    def __str__(self):
        return f'{self.date.strftime("%d.%m.%Y %H:%M:%S")} :: ' \
               f'{self.category} :: ' \
               f'{self.title.title()} :: ' \
               f'{self.text[0:50] + "..." if len(str(self.text)) > 50 else self.text}'

    def get_absolute_url(self):
        return reverse('ads_detail', args=[str(self.id)])


class Response(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    text = models.TextField("Текст")
    ad = models.ForeignKey(Ads, on_delete=models.CASCADE, verbose_name="Объявление")
    accepted = models.BooleanField("Принят", default=False)
    date = models.DateTimeField("Дата отклика", auto_now_add=True)

    def __str__(self):
        return f'{self.date.strftime("%d.%m.%Y %H:%M:%S")} :: ' \
               f'{self.text[0:50] + "..." if len(str(self.text)) > 50 else self.text} --> {self.ad.title.title()}'

    def get_absolute_url(self):
        return reverse('response_detail', kwargs={'apk': str(self.ad.pk), 'pk': str(self.pk)})
