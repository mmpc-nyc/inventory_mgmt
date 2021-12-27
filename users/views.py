from django.views.generic import FormView
from django.forms import Form
from django.views import View
from django.contrib.auth import logout, authenticate, login
from rest_framework.reverse import reverse_lazy
from django.contrib import messages
from core import settings
from users.forms import LoginForm
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _


class LoginView(FormView):
    template_name = 'users/login_form.html'
    form_class = LoginForm

    def post(self, request, *args, **kwargs):

        form: Form = self.get_form()
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request=request, user=user)
                    messages.success(request, f'Logged in as {user.username}')
                    return self.form_valid(form)
                messages.error(request, _(f'Login failed, Your account is inactive. Please contact an administrator to reactivate your account'))
            messages.error(request, _(f'Failed to login. Either the user does not exist or you have entered an invalid password'))
        return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('inventory:home')


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('inventory:home'))