from django.urls import path, include
from .views import home, results, login, sign,logout,add_back, msg


urlpatterns = [
    path('', home, name="home"),
    path('sign-up', sign, name='sign'),
    path('found/<str:pk>', results, name="results"),
    path('login', login, name="login"),
    path('logout', logout, name="logout"),
    path('add_back/<str:pk>/', add_back, name="add_back"),
    path('msg/<str:pk>', msg, name="msg"),
]