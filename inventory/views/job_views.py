from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView
from inventory.models import Job


class JobDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Job
    template_name_suffix = '_detail'
    extra_context = {'title': 'Job Detail'}
    permission_required = {'any': ('inventory_view_job',)}


class JobListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Job
    template_name_suffix = '_list'
    extra_context = {'title': 'Job List'}
    permission_required = {'any': ('inventory_view_job',)}


class JobCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Job
    template_name_suffix = '_create'
    permission_required = {'any': ('inventory_create_job',)}


class JobDeleteView(PermissionRequiredMixin, CreateView, DeleteView):
    model = Job
    template_name_suffix = '_delete'
    permission_required = {'any': ('inventory_delete_job',)}


class JobUpdateView(PermissionRequiredMixin, CreateView, UpdateView):
    model = Job
    template_name_suffix = '_update'
    permission_required = {'any': ('inventory_update_job',)}
