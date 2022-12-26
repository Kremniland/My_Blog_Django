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

from .forms import ContactForm, ContactModelForm, PostCreateModelForm
from .models import Category, Post, ContactModel
from .serializers import PostSerializer


class PostListView(ListView):
    '''Домашняя страница со всеми постами всех категорий'''
    model = Post
    template_name = 'blog/home_page.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Домашняя страница'
        return context


class PostCatListView(ListView):
    '''Вывод списка постов по slug категории'''
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


class PostDetailView(DetailView):
    '''Детализация поста'''
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'


class PostCreateView(CreateView):
    model = Post
    form_class = PostCreateModelForm
    template_name = 'blog/post_create.html'
    success_url = reverse_lazy('home_page')


# class ContactCreate(CreateView):
#     '''Обратная связь через форму модели'''
#     form_class = ContactModelForm
#     template_name = 'blog/contact.html'
#     success_url = '/'

def contact_email(request):
    '''Обратная связь через собственную форму'''
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


class RegisterUser(CreateView):
    '''Регистрация через класс:'''
    form_class = UserCreationForm  # Стандартная форма регистрации
    template_name = 'auth/registr.html'
    success_url = reverse_lazy('home_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context


def login_user(request):
    '''Авторизация'''
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)  # Стандартная форма
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
class PostListCreateApiView(ListCreateAPIView):
    '''Просмотр и добавление'''
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostUpdateAPIView(UpdateAPIView):
    '''Изменение'''
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDestroyAPIView(DestroyAPIView):
    '''Удаление'''
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostAPIViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # Добавит вывод кнопку action списка категорий
    @action(methods=['get'], detail=False)  # если False - выведет список, если True - одну
    def category(self, request):
        cats = Category.objects.all()
        return Response({'cats': [c.title for c in cats]})
