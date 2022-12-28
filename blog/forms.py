from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User  # Импортируем модель User
from django import forms
from captcha.fields import CaptchaField

from .models import ContactModel, Post, Comments


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['text']
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                }
            )
        }


class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 7,
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
    '''Контактная форма через модель с капчой'''
    captcha = CaptchaField()

    class Meta:
        model = ContactModel
        fields = ['message']
        widgets = {
            'message': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 7,
                }
            ),
        }


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
    captcha = CaptchaField()


class LoginForm(AuthenticationForm, forms.ModelForm):
    '''Форма для авторизации'''
    class Meta:
        model = User
        fields = ['username', 'password']
    # username = forms.CharField(
    #     label='Ваш логин',
    #     widget=forms.TextInput(attrs={'class': 'form-control', }),
    #     min_length=2,
    # )
    # password = forms.CharField(
    #     label='Ваш пароль',
    #     widget=forms.PasswordInput(attrs={'class': 'form-control', }),
    # )
