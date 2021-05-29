from django.urls import path
from .views import OfertaListView, OfertaFormView, OfertaShowView, OfertaUpdateView, MisOfertasView

urlpatterns=[
    path('',OfertaListView.as_view(), name='ofertas'),
    path('crear/', OfertaFormView.as_view(), name='crear_oferta'),
    path('<oferta_id>/', OfertaShowView.as_view(), name='mostrar_oferta'),
    path('editar/<oferta_id>/', OfertaUpdateView.as_view(), name='editar_oferta'),
    path('misOfertas/', MisOfertasView.as_view(), name='mis_ofertas'),
]