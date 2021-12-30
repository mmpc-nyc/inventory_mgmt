from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.db.models import Model
from django.views.generic import UpdateView, DeleteView, CreateView
from django.views.generic.base import ContextMixin

from inventory.views.axios_views import AxiosListView, AxiosDetailView


class CustomMixin(PermissionRequiredMixin, ContextMixin):
    model: Model
    permission_scope: str
    title: str
    view_type: str
    partial_list_template: str
    partial_detail_template: str

    def get_permission_required(self) -> dict[str:list]:
        self.permission_required = self.permission_required or self.get_default_permission_required()
        return super().get_permission_required()

    def get_default_permission_required(self) -> dict[str:list]:
        return {'any': [f'{self.model._meta.app_label}_{self.permission_scope}_{self.model._meta.model_name}', ]}

    def get_title(self):
        if hasattr(self, 'title'): return self.title
        model_name = f'{self.model._meta.verbose_name or self.model._meta.model_name.capitalize()}'
        if hasattr(self, 'object'):
            return f'{model_name} {self.object.__str__() or self.object.__repr__()}'
        if hasattr(self, 'view_type'):
            return f'{model_name} {self.view_type.capitalize()}'
        return model_name

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        title = self.get_title()
        context['title'] = title
        context['model_name'] = self.model._meta.model_name
        context['app_name'] = self.model._meta.app_label
        context['partial_list_template'] = self.get_partial_list_template()
        context['partial_detail_template'] = self.get_partial_detail_template()
        if hasattr(self, 'view_type'):
            context['view_type'] = self.view_type
        return context

    def generate_partial_template(self):
        return f'{self.model._meta.app_label}/partials/{self.model._meta.model_name}'

    def get_partial_list_template(self):
        if hasattr(self, 'partial_list_template'):
            return self.partial_list_template
        self.partial_list_template = f'{self.generate_partial_template()}_list.html'
        return self.partial_list_template

    def get_partial_detail_template(self):
        if hasattr(self, 'partial_detail_template'):
            return self.partial_detail_template
        self.partial_detail_template = f'{self.generate_partial_template()}_detail.html'
        return self.partial_detail_template


class CustomDetailView(CustomMixin, AxiosDetailView):
    permission_scope = 'view'
    view_type = 'detail'


class CustomListView(CustomMixin, AxiosListView):
    permission_scope = 'view'
    view_type = 'list'
    template_name = 'inventory/list.html'


class CustomUpdateView(CustomMixin, UpdateView):
    permission_scope = 'update'
    view_type = 'update'


class CustomDeleteView(CustomMixin, DeleteView):
    permission_scope = 'delete'
    view_type = 'delete'


class CustomCreateView(CustomMixin, CreateView):
    permission_scope = 'create'
    view_type = 'create'
