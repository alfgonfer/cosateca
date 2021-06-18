from django.urls import path
from .views import PrestarFormView, SolicitarFormView, PrestarNotificacionFormView, PrestamosListView

urlpatterns=[
    path('', PrestamosListView.as_view(), name='prestamos'),
    path('prestar/', PrestarFormView.as_view(), name='prestar_peticion'),
    path('prestar_notificacion/', PrestarNotificacionFormView.as_view(), name='prestar_notificacion'),
    path('solicitar/', SolicitarFormView.as_view(), name='solicitar_oferta'),
    
]