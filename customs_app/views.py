from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import AgenteAduanal, Pedimento
from .forms import AgenteAduanalForm, PedimentoForm

class AgenteAduanalListView(LoginRequiredMixin, ListView):
    model = AgenteAduanal
    template_name = 'customs_app/agente_list.html'
    context_object_name = 'agentes'

class AgenteAduanalCreateView(LoginRequiredMixin, CreateView):
    model = AgenteAduanal
    form_class = AgenteAduanalForm
    template_name = 'customs_app/agente_form.html'
    success_url = reverse_lazy('agente-list')

class AgenteAduanalUpdateView(LoginRequiredMixin, UpdateView):
    model = AgenteAduanal
    form_class = AgenteAduanalForm
    template_name = 'customs_app/agente_form.html'
    success_url = reverse_lazy('agente-list')

class AgenteAduanalDeleteView(LoginRequiredMixin, DeleteView):
    model = AgenteAduanal
    template_name = 'customs_app/agente_confirm_delete.html'
    success_url = reverse_lazy('agente-list')
