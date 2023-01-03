from django.db import models


class Contact(models.Model):
    '''Модель для контакта'''
    name = models.CharField(max_length=32)
    email = models.EmailField(max_length=64)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'



