from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User  # Импортируем модель User
from django import forms

from .models import ContactModel


class ContactModelForm(forms.ModelForm): # Через модель
    class Meta:
        model = ContactModel
        fields = ['name', 'email', 'message']


class ContactForm(forms.Form):
    # name = forms.CharField(
    #     label='Имя',
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'form-control',
    #         }
    #     )
    # )
    # email = forms.CharField(
    #     label='Почта',
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'form-control',
    #         }
    #     )
    # )
    message = forms.CharField(
        label='Текст письма',

        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 7,

            }
        )
    )


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Ваш логин',
        widget=forms.TextInput(attrs={'class': 'form-control', }),
        min_length=2,
    )
    password = forms.CharField(
        label='Ваш пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', }),
    )
