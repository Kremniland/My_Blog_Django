from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication

from .forms import ContactForm, ContactModelForm
from .models import Category, Post, ContactModel
from .serializers import PostSerializer


# def home_page(request):
#     return render(request, 'blog/home_page.html', {'title': 'Домашняя страница'})
class PostListView(ListView):
    model = Post
    template_name = 'blog/home_page.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Домашняя страница'
        return context


# Вывод списка постов по slug категории
class PostCatListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    # allow_empty = False
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['cat_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = Category.objects.get(slug=self.kwargs['cat_slug'])
        return context


# Обратная связь через форму модели
# class ContactCreate(CreateView):
#     form_class = ContactModelForm
#     template_name = 'blog/contact.html'
#     success_url = '/'

# Обратная связь через собственную форму
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
        'title': 'Обратная связь',
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


# Авторизация
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST) # Стандартная форма
        # form = LoginForm(data=request.POST) # Через собственную форму
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


# API
class PostListCreateApiView(ListCreateAPIView): # Просмотр и добавление через модель в сериалайзер
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostUpdateAPIView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDestroyAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostAPIViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(methods=['get'], detail=False) # если False - выведет список, если True - одну
    def category(self, request):
        cats = Category.objects.all()
        return Response({'cats': [c.title for c in cats]})
