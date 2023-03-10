from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse, reverse_lazy

from django.contrib import messages

from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
# Для переопределения что бы добавить форму для комментариев в класс DetailView
from django.views.generic.edit import FormMixin

from django.template import Context, Template

from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView, GenericAPIView
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication

from .forms import ContactForm, ContactModelForm, PostModelForm, LoginForm, CommentForm
from .models import Category, Post, ContactModel, Comments
from .serializers import PostSerializer


class CustomSuccessMessageMixin:
    '''Кастомный класс для работы с messages'''
    @property
    def success_msg(self):
        return False

    def form_valid(self, form):
        '''Метод для вывода messages'''
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)

    def get_success_url(self):
        '''Метод для передачи в адресную строку GET
        запросом id поста для подсвечивания его на странице'''
        return f'{self.success_url}?id={self.object.id}'


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

    def get_queryset(self):
        return Post.objects.all().order_by('-update_date')


class PostCatListView(ListView):
    '''Вывод списка постов по slug категории'''
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    # allow_empty = False
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['cat_slug']).order_by('-update_date')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = Category.objects.get(slug=self.kwargs['cat_slug'])
        return context


class PostDetailView(CustomSuccessMessageMixin, FormMixin, DetailView):
    '''Детализация поста порядок наследования классов важен! при изменении
    порядка наследованиямогут не работать некоторые ф-ии!'''
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'
    # Из класса FormMixin добавляем форму для комментариев на страницу детализации
    form_class = CommentForm
    # Выведет сообщение при успешном создании необходим кастомный класс CustomSuccessMessageMixin
    success_msg = 'Комментарий создан'

    def get_success_url(self, **kwargs):
        '''При успешном создании коментария переводим на страницу детализации поста'''
        return reverse_lazy('post_detail', kwargs={'post_id': self.get_object().id})

    def post(self, reqest, *args, **kwargs):
        '''Переопределяем метод для проверки form поста'''
        form = self.get_form() # Берем форму из get_form()
        if form.is_valid:
            return self.form_valid(form) # Если форма валидна отправляем ее в переопределенный ниже метод form_valid
        else:
            return self.form_invalid(form) # Если не валидна в form_invalid

    def form_valid(self, form):
        ''' Переопределяем метод для добавления недостающих полей в форму комментария'''
        self.object = form.save(commit=False)
        self.object.post = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


def update_comment_status(request, pk, type):
    item = Comments.objects.get(pk=pk)
    request.set_cookie(item.pk, 'test_cookie')
    # Если user не post.author просто выведет надпись, а удаления или публикации не будет
    if request.user != item.post.author:
        return HttpResponse('deny')

    if type == 'public':
        import operator # Для того что бы инверсировать status
        item.status = operator.not_(item.status)
        item.save()
        template = 'inc/comment_item.html'
        context = {'item': item, 'status_comment': 'Комментарий опубликован'}
        return render(request, template, context)

    elif type == 'delete':
        item.delete()
        return HttpResponse('''
        <div class="alert alert-success">
        Комментарий удален
        </div>
        ''')


class PostCreateView(CustomSuccessMessageMixin, LoginRequiredMixin, CreateView):
    '''Создание поста'''
    # login_url = '/login/' # Можно прописать в settings LOGIN_URL = '/login/'
    model = Post
    form_class = PostModelForm
    template_name = 'blog/post_create.html'
    success_url = reverse_lazy('home_page')
    # Используем success_msg из класса CustomSuccessMessageMixin
    success_msg = 'Запись создана'

    def form_valid(self, form):
        '''Добавляем в форму недостающие поля user и publisher'''
        instance = form.save(commit=False) # Создаем объект но не сохраняем его
        instance.author = self.request.user
        instance.publisher = True
        instance.save()
        return super().form_valid(form)
        # return redirect(self.success_url)


class PostDelete(CustomSuccessMessageMixin, LoginRequiredMixin, DeleteView):
    '''Удаление поста'''
    model = Post
    template_name = 'blog/post_detail.html' # Шаблон тот же что и для создания
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('home_page')
    success_msg = 'Запись удалена'


# НЕ РАБОТАЕТ МЕТОД ПЕРЕОПРЕДЕЛЕНИЯ ДЛЯ УДАЛЕНИЯ ТОЛЬКО АВТОРУ
    def delete(self, request, *args, **kwargs):
        print('priveeeeeeeeeeeeeeeeeeetttttttttttt')
        self.object = self.get_object()
        if self.request.user != self.object.author:
            return self.handle_no_permission()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class PostUpdateView(CustomSuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/post_update.html'
    form_class = PostModelForm
    success_url = reverse_lazy('home_page')
    success_msg = 'Запись изменена'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование поста'
        return context

    def get_form_kwargs(self):
        '''Если зарегистрированный пользователь не автор поста выцдаст 403'''
        kwargs = super().get_form_kwargs()
        # instance - объект модели Post
        print(kwargs['instance'].author) # Выведет author редактируемого поля модели пост
        print(self.request.user) # Залогиненый(на сайте) пользователь
        if self.request.user != kwargs['instance'].author:
            return self.handle_no_permission()
        return kwargs


class ContactCreate(CustomSuccessMessageMixin, CreateView):
    '''Обратная связь через класс'''
    form_class = ContactModelForm
    template_name = 'blog/contact.html'
    success_url = '/'
    success_msg = 'Запись отправлена'

    def form_valid(self, form):
        '''Добавляем в форму недостающие поля user и email'''
        instance = form.save(commit=False)
        instance.name = self.request.user
        instance.email = self.request.user.email
        instance.save()
        return redirect(self.success_url)

# ============================= Регистрация ==============================
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


# =========================== API ===============================================
class PostByCategoryAPIView(ListModelMixin, GenericAPIView):
    '''Вывод постов по категориям'''
    serializer_class = PostSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Post.objects.filter(category=pk)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PostListCreateApiView(ListCreateAPIView):
    '''Просмотр и добавление постов'''
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostUpdateAPIView(UpdateAPIView):
    '''Изменение постов'''
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDestroyAPIView(DestroyAPIView):
    '''Удаление постов'''
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostAPIViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().prefetch_related('category')
    serializer_class = PostSerializer

    # Добавит вывод кнопку action списка категорий
    @action(methods=['get'], detail=False)  # если False - выведет список, если True - одну
    def category(self, request):
        cats = Category.objects.all()
        return Response({'cats': [c.title for c in cats]})


# ============================ Методы =================================================
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
