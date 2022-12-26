from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User  # Импортируем модель User
from django import forms
from captcha.fields import CaptchaField

from .models import ContactModel, Post


class PostCreateModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'publisher', 'author']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                }
            ),
            # 'image': forms.ImageField(),
            'author': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'publisher': forms.CheckboxInput(
                # attrs={
                #     'class': 'form-control',
                # }
            ),
        }


class ContactModelForm(forms.ModelForm):
    '''Контактная форма через модель'''
    class Meta:
        model = ContactModel
        fields = ['name', 'email', 'message']


class ContactForm(forms.Form):
    '''Собственная контактная форма с капчой'''
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
    capcha = CaptchaField()



class LoginForm(AuthenticationForm):
    '''Форма для авторизации'''
    username = forms.CharField(
        label='Ваш логин',
        widget=forms.TextInput(attrs={'class': 'form-control', }),
        min_length=2,
    )
    password = forms.CharField(
        label='Ваш пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', }),
    )
