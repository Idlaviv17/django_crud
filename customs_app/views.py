from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from .models import AgenteAduanal, AduanaSeccion, ClavePedimento, Pedimento
from .forms import AgenteAduanalForm, AduanaSeccionForm, ClavePedimentoForm, PedimentoForm
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy

# Navigation Context
class NavContextMixin:
    nav_section = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_section'] = self.nav_section
        return context

# Agente Aduanal Views
class AgenteAduanalListView(LoginRequiredMixin, NavContextMixin, ListView):
    nav_section = 'agente'
    model = AgenteAduanal
    context_object_name = 'agentes'
    template_name = 'customs_app/agentes/list.html'

class AgenteAduanalCreateView(LoginRequiredMixin, NavContextMixin, CreateView):
    nav_section = 'agente'
    model = AgenteAduanal
    form_class = AgenteAduanalForm
    template_name = 'customs_app/agentes/form.html'
    success_url = reverse_lazy('agente-list')

class AgenteAduanalUpdateView(LoginRequiredMixin, NavContextMixin, UpdateView):
    nav_section = 'agente'
    model = AgenteAduanal
    form_class = AgenteAduanalForm
    template_name = 'customs_app/agentes/form.html'
    success_url = reverse_lazy('agente-list')

class AgenteAduanalDeleteView(LoginRequiredMixin, NavContextMixin, DeleteView):
    nav_section = 'agente'
    model = AgenteAduanal
    template_name = 'customs_app/agentes/confirm_delete.html'
    success_url = reverse_lazy('agente-list')

# Aduana Seccion Views
class AduanaSeccionListView(LoginRequiredMixin, NavContextMixin, ListView):
    nav_section = 'aduana'
    model = AduanaSeccion
    context_object_name = 'aduanas'
    template_name = 'customs_app/aduanas/list.html'

class AduanaSeccionCreateView(LoginRequiredMixin, NavContextMixin, CreateView):
    nav_section = 'aduana'
    model = AduanaSeccion
    form_class = AduanaSeccionForm
    template_name = 'customs_app/aduanas/form.html'
    success_url = reverse_lazy('aduana-list')

class AduanaSeccionUpdateView(LoginRequiredMixin, NavContextMixin, UpdateView):
    nav_section = 'aduana'
    model = AduanaSeccion
    form_class = AduanaSeccionForm
    template_name = 'customs_app/aduanas/form.html'
    success_url = reverse_lazy('aduana-list')

class AduanaSeccionDeleteView(LoginRequiredMixin, NavContextMixin, DeleteView):
    nav_section = 'aduana'
    model = AduanaSeccion
    template_name = 'customs_app/aduanas/confirm_delete.html'
    success_url = reverse_lazy('aduana-list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Check for related pedimentos
        related_pedimentos = Pedimento.objects.filter(aduana_seccion=self.object)
        
        if related_pedimentos.exists():
            context = self.get_context_data(object=self.object)
            context['related_pedimentos'] = related_pedimentos
            return render(request, 'customs_app/aduanas/cannot_delete.html', context)
            
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            context = self.get_context_data(object=self.get_object())
            context['related_pedimentos'] = Pedimento.objects.filter(aduana_seccion=self.get_object())
            return render(request, 'customs_app/aduanas/cannot_delete.html', context)

# Clave Pedimento Views
class ClavePedimentoListView(LoginRequiredMixin, NavContextMixin, ListView):
    nav_section = 'clave'
    model = ClavePedimento
    context_object_name = 'claves'
    template_name = 'customs_app/claves/list.html'

class ClavePedimentoCreateView(LoginRequiredMixin, NavContextMixin, CreateView):
    nav_section = 'clave'
    model = ClavePedimento
    form_class = ClavePedimentoForm
    template_name = 'customs_app/claves/form.html'
    success_url = reverse_lazy('clave-list')

class ClavePedimentoUpdateView(LoginRequiredMixin, NavContextMixin, UpdateView):
    nav_section = 'clave'
    model = ClavePedimento
    form_class = ClavePedimentoForm
    template_name = 'customs_app/claves/form.html'
    success_url = reverse_lazy('clave-list')

class ClavePedimentoDeleteView(LoginRequiredMixin, NavContextMixin, DeleteView):
    nav_section = 'clave'
    model = ClavePedimento
    template_name = 'customs_app/claves/confirm_delete.html'
    success_url = reverse_lazy('clave-list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Check for related pedimentos
        related_pedimentos = Pedimento.objects.filter(clave_pedimento=self.object)
        
        if related_pedimentos.exists():
            return render(request, 'customs_app/claves/cannot_delete.html', {
                'related_pedimentos': related_pedimentos
            })
            
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            related_pedimentos = Pedimento.objects.filter(clave_pedimento=self.get_object())
            return render(request, 'customs_app/claves/cannot_delete.html', {
                'related_pedimentos': related_pedimentos
            })

# Pedimento Views
class PedimentoListView(LoginRequiredMixin, NavContextMixin, ListView):
    nav_section = 'pedimento'
    model = Pedimento
    context_object_name = 'pedimentos'
    template_name = 'customs_app/pedimentos/list.html'

class PedimentoCreateView(LoginRequiredMixin, NavContextMixin, CreateView):
    nav_section = 'pedimento'
    model = Pedimento
    form_class = PedimentoForm
    template_name = 'customs_app/pedimentos/form.html'
    success_url = reverse_lazy('pedimento-list')

    def get(self, request, *args, **kwargs):
        has_aduanas = AduanaSeccion.objects.exists()
        has_claves = ClavePedimento.objects.exists()

        if not has_aduanas or not has_claves:
            return render(request, 'customs_app/pedimentos/alert.html', {
                'has_aduanas': has_aduanas,
                'has_claves': has_claves
            })
        
        return super().get(request, *args, **kwargs)

class PedimentoUpdateView(LoginRequiredMixin, NavContextMixin, UpdateView):
    nav_section = 'pedimento'
    model = Pedimento
    form_class = PedimentoForm
    template_name = 'customs_app/pedimentos/form.html'
    success_url = reverse_lazy('pedimento-list')

class PedimentoDeleteView(LoginRequiredMixin, NavContextMixin, DeleteView):
    nav_section = 'pedimento'
    model = Pedimento
    template_name = 'customs_app/pedimentos/confirm_delete.html'
    success_url = reverse_lazy('pedimento-list')