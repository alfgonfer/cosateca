from django.urls import path
from .views import PrestarFormView, SolicitarFormView

urlpatterns=[
    path('prestar/', PrestarFormView.as_view(), name='prestar_peticion'),
    path('solicitar/', SolicitarFormView.as_view(), name='solicitar_oferta'),
]