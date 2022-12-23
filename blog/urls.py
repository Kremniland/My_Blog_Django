from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    path('', home_page, name='home_page'),
    path('regist/', RegisterUser.as_view(), name='regist'),
    path('login/', login_user, name='log in'),
    path('logout/', logout_user, name='log out'),

    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]