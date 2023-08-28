from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


class MyLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class MyLogoutView(LogoutView):
    template_name = 'accounts/logout.html'


class SignUpView(CreateView):
    template_name = 'accounts/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('log-list')
