from django.core.mail import send_mail, send_mass_mail # send_mass_mail - для массовой рассылки

from django.conf import settings


def send(user_mail):
    '''Отправляем емаил на почту user_mail'''
    send_mail(
        'Подписка на рассылку',
        'Подписка на рассылку оформлена',
        settings.EMAIL_HOST_USER,
        [user_mail],
        fail_silently=False,
    )

