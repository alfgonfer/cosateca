"""cosateca URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from usuarios import urls as usuarios_urls
from ofertas import urls as ofertas_urls
from peticiones import urls as peticiones_urls
from prestamos import urls as prestamos_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(usuarios_urls)),
    path('ofertas/', include(ofertas_urls)),
    path('peticiones/', include(peticiones_urls)),
    path('prestamos/',include(prestamos_urls))
]
