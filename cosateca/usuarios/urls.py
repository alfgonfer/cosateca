from django.contrib.auth import logout
from django.urls import path
from .views import InicioView, LoginView
from django.contrib.auth.views import logout_then_login

urlpatterns=[
    path('',InicioView.as_view(), name='inicio'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_then_login, name='logout')
]