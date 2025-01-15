from django.urls import path
from .views import (
    AgenteAduanalListView, AgenteAduanalCreateView,
    AgenteAduanalUpdateView, AgenteAduanalDeleteView
)

urlpatterns = [
    # List view - shows all agents
    path('agentes/', AgenteAduanalListView.as_view(), name='agente-list'),
    # Create view - form for new agent
    path('agentes/new/', AgenteAduanalCreateView.as_view(), name='agente-create'),
    # Update view - form for editing existing agent
    path('agentes/<str:pk>/edit/', AgenteAduanalUpdateView.as_view(), name='agente-update'),
    # Delete view - confirmation page for deletion
    path('agentes/<str:pk>/delete/', AgenteAduanalDeleteView.as_view(), name='agente-delete'),
]