from django.urls import path, include, re_path
from .views import *

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'post', PostAPIViewSet)


urlpatterns = [
    path('', PostListView.as_view(), name='home_page'),
    path('category/<slug:cat_slug>/',   PostCatListView.as_view(), name='category'),
    path('contact/', contact_email, name='contact'),
    path('regist/', RegisterUser.as_view(), name='regist'),
    path('login/', login_user, name='log in'),
    path('logout/', logout_user, name='log out'),

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