from django.contrib.auth import logout
from django.urls import path
from django.contrib.auth.views import logout_then_login
from .views import InicioView, LoginView, RegistroView
from prestamos.views import NotificacionListView

urlpatterns=[
    path('',InicioView.as_view(), name='inicio'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_then_login, name='logout'),
    path('registro/', RegistroView.as_view(), name='registro'),
    path('notificaciones/', NotificacionListView.as_view(), name='notificaciones'),
]