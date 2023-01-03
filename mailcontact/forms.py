from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    '''Форма для сохранения контакта емаил'''
    class Meta:
        model = Contact
        fields = ['name', 'email']



