from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication

from .forms import ContactForm, ContactModelForm, PostCreateModelForm, LoginForm
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
    '''Создание поста'''
    model = Post
    form_class = PostCreateModelForm
    template_name = 'blog/post_create.html'
    success_url = reverse_lazy('home_page')

    def form_valid(self, form):
        '''Добавляем в форму недостающие поля user и publisher'''
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.publisher = True
        instance.save()
        return redirect(self.success_url)


class PostDelete(DeleteView):
    '''Удаление поста'''
    model = Post
    template_name = 'blog/post_detail.html' # Шаблон тот же что и для создания
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('home_page')


class ContactCreate(CreateView):
    '''Обратная связь через класс'''
    form_class = ContactModelForm
    template_name = 'blog/contact.html'
    success_url = '/'

    def form_valid(self, form):
        '''Добавляем в форму недостающие поля user и email'''
        instance = form.save(commit=False)
        instance.name = self.request.user
        instance.email = self.request.user.email
        instance.save()
        return redirect(self.success_url)


class RegisterUser(CreateView):
    '''Регистрация через класс:'''
    form_class = UserCreationForm  # Стандартная форма регистрации
    template_name = 'auth/registr.html'
    success_url = reverse_lazy('home_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

    def form_valid(self, form):
        '''Переопределяем что бы после регистрации не надо было авторизоваться'''
        form_valid = super().form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        auth_user = authenticate(username=username, password=password)
        login(self.request, auth_user)
        return form_valid


class MyLoginView(LoginView):
    '''Авторизация через класс'''
    form_class = LoginForm
    template_name = 'auth/login.html'

    def get_success_url(self):
        return reverse_lazy('home_page')


class MyLogoutView(LogoutView):
    '''Логоут через класс'''
    next_page = reverse_lazy('home_page')


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


# =============================================================================
def contact_email(request):
    '''Обратная связь через метод'''
    if request.method == 'POST':
        form = ContactModelForm(request.POST)
        if form.is_valid():
            contact_add = ContactModel.objects.create(
                name=request.user,
                email=request.user.email,
                message=form.cleaned_data['message'],
            )
            return redirect('home_page')
    else:
        form = ContactModelForm()
    context = {
        'form': form,
        'title': 'Обратная связь',
    }
    return render(request, 'blog/contact.html', context)


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
