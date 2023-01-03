from django.views.generic import CreateView

from .models import Contact
from .forms import ContactForm
from .service import send


class ContactView(CreateView):
    '''Сохраняем контакт в БД'''
    model = Contact
    form_class = ContactForm
    template_name = 'blog/contact.html'
    success_url = '/'

    def form_valid(self, form):
        '''Переопределяем для отправки письма на почту указанную пользователем'''
        form.save()
        send(form.instance.email)
        return super().form_valid(form)


