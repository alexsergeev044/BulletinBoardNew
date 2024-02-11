from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives

from .models import Ads, Response


def send_msg(subject, ad, emails, response_txt='', response_html=''):

    text_content = (
        f'Название объявления: {ad.title}\n'
        f'Ссылка на объявление: http://127.0.0.1:8000{ad.get_absolute_url()}{response_txt}'
    )
    html_content = (
        f'Название объявления: {ad.title}<br>'
        f'<a href="http://127.0.0.1:8000{ad.get_absolute_url()}">'
        f'Ссылка на объявление</a>{response_html}'
    )
    i = 0
    for email in emails:
        if isinstance(subject, str):
            msg = EmailMultiAlternatives(subject, f'{subject}!\n\n'+text_content, None, [email])
            msg.attach_alternative(f'{subject}!<br><br>'+html_content, "text/html")
        else:
            msg = EmailMultiAlternatives(subject[i], f'{subject[i]}!\n\n'+text_content, None, [email])
            msg.attach_alternative(f'{subject[i]}!<br><br>'+html_content, "text/html")
            i += 1

        msg.send()


@receiver(post_save, sender=Ads)
def ad_created(instance, created, **kwargs):
    if not created:
        return

    emails = list(User.objects.all().values_list('email', flat=True).distinct())
    subject = f'Опубликовано новое объявление "{instance.title}"'

    if len(emails) > 0:
        send_msg(subject, instance, emails)


@receiver(post_save, sender=Response)
def response_created(instance, created, **kwargs):
    if created:
        emails = [instance.author.email, instance.ad.author.email, ]
        subject = (f'Вы опубликовали отклик на объявление "{instance.ad.title}"',
                   f'На ваше объявление "{instance.ad.title}" опубликовал отклик {instance.author}',
                   )
    elif instance.accepted:
        emails = [instance.author.email, ]
        subject = (f'Ваш отклик на объявление "{instance.ad.title}" был принят {instance.ad.author}',
                   )
    else:
        return

    response_txt = (
        f'\n\nОтклик:\n'
        f'Текст: {instance.text}\n'
        f'Ссылка на отклик: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    response_html = (
        f'<br><br>Отклик:<br>'
        f'Текст: {instance.text}<br>'
        f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
        f'Ссылка на отклик</a>'
    )
    if len(emails) > 0:
        send_msg(subject, instance.ad, emails, response_txt, response_html)
