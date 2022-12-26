from django.urls import path, include, re_path
from .views import *

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'post', PostAPIViewSet)


urlpatterns = [
    path('', PostListView.as_view(), name='home_page'),
    path('post/<int:post_id>/', PostDetailView.as_view(), name='post_detail'),
    path('post/delete/<int:post_id>/', PostDelete.as_view(), name='post_delete'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),

    path('category/<slug:cat_slug>/',   PostCatListView.as_view(), name='category'),

    path('contact/', ContactCreate.as_view(), name='contact'),

    path('regist/', RegisterUser.as_view(), name='regist'),
    # path('login/', login_user, name='log in'),
    path('login/', MyLoginView.as_view(), name='log in'),
    # path('logout/', logout_user, name='log out'),
    path('logout/', MyLogoutView.as_view(), name='log out'),

    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),

# Вывод всех записей и добавление записи ListCreateApiView
    path('api/v1/postlist/', PostListCreateApiView.as_view()),
    path('api/v1/postlist/<int:pk>/', PostListCreateApiView.as_view()),
# Изменение записи UpdateAPIView
    path('api/v1/postdetail/<int:pk>/', PostUpdateAPIView.as_view()),
# Удаление записи через DestroyAPIView
    path('api/v1/postdestroy/<int:pk>/', PostDestroyAPIView.as_view()),

    path('viewset/', include(router.urls)),

]