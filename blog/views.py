from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import ContactForm
from .models import Category, Post, ContactModel


def home_page(request):
    return render(request, 'blog/home_page.html')


# Обратная связь
# class ContactCreate(CreateView):
#     form_class = ContactForm
#     template_name = 'blog/contact.html'
#     success_url = '/'
# def contact_email(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             contact_add = ContactModel.objects.create(
#                 name=form.cleaned_data['name'],
#                 email=form.cleaned_data['email'],
#                 message=form.cleaned_data['message'],
#             )
#             return redirect('home_page')
#     else:
#         form = ContactForm()
#     context = {'form': form}
#     return render(request, 'blog/contact.html', context)
def contact_email(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_add = ContactModel.objects.create(
                name=request.user,
                email=request.user.email,
                message=form.cleaned_data['message'],
                )
            return redirect('home_page')
    else:
        form = ContactForm()
    context = {
        'form': form,
    }
    return render(request, 'blog/contact.html', context)


# Регистрация через класс:
class RegisterUser(CreateView):
    form_class = UserCreationForm  # Стандартная форма регистрации
    template_name = 'auth/registr.html'
    success_url = reverse_lazy('home_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST) # Стандартная форма
        # form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home_page')
    else:
        form = AuthenticationForm()
        # form = LoginForm()
    title = 'Авторизация'
    return render(request, 'auth/login.html', {'form': form, 'title': title})


def logout_user(request):
    logout(request)
    return redirect('log in')

# class CategoryList(ListView):
#     model = Category
#     template_name = 'blog/home_page.html'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Список категорий'
#         return context
#
