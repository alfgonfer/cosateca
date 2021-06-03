from django.urls import path
from .views import PeticionListView, PeticionCreateView, PeticionUpdateView, MisPeticionesView, PeticionDeleteView

urlpatterns=[
    path('',PeticionListView.as_view(), name='peticiones'),
    path('crear/', PeticionCreateView.as_view(), name='crear_peticion'),
    path('misPeticiones/', MisPeticionesView.as_view(), name='mis_peticiones'),
    path('borrar/', PeticionDeleteView.as_view(), name='borrar_peticion'),
    path('editar/<peticion_id>/', PeticionUpdateView.as_view(), name='editar_peticion'),
]