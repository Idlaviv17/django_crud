from django.urls import path
from . import views

urlpatterns = [
    # Agente Aduanal URLs
    path('agentes/', views.AgenteAduanalListView.as_view(), name='agente-list'),
    path('agentes/nuevo/', views.AgenteAduanalCreateView.as_view(), name='agente-create'),
    path('agentes/<str:pk>/editar/', views.AgenteAduanalUpdateView.as_view(), name='agente-update'),
    path('agentes/<str:pk>/eliminar/', views.AgenteAduanalDeleteView.as_view(), name='agente-delete'),

    # Aduana Seccion URLs
    path('aduanas/', views.AduanaSeccionListView.as_view(), name='aduana-list'),
    path('aduanas/nuevo/', views.AduanaSeccionCreateView.as_view(), name='aduana-create'),
    path('aduanas/<int:pk>/editar/', views.AduanaSeccionUpdateView.as_view(), name='aduana-update'),
    path('aduanas/<int:pk>/eliminar/', views.AduanaSeccionDeleteView.as_view(), name='aduana-delete'),

    # Clave Pedimento URLs
    path('claves/', views.ClavePedimentoListView.as_view(), name='clave-list'),
    path('claves/nuevo/', views.ClavePedimentoCreateView.as_view(), name='clave-create'),
    path('claves/<str:pk>/editar/', views.ClavePedimentoUpdateView.as_view(), name='clave-update'),
    path('claves/<str:pk>/eliminar/', views.ClavePedimentoDeleteView.as_view(), name='clave-delete'),

    # Pedimento URLs
    path('pedimentos/', views.PedimentoListView.as_view(), name='pedimento-list'),
    path('pedimentos/nuevo/', views.PedimentoCreateView.as_view(), name='pedimento-create'),
    path('pedimentos/<str:pk>/editar/', views.PedimentoUpdateView.as_view(), name='pedimento-update'),
    path('pedimentos/<str:pk>/eliminar/', views.PedimentoDeleteView.as_view(), name='pedimento-delete'),
]