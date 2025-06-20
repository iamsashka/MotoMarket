from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.views import LoginView

class SignUp(CreateView):
    form_class = RegistrationForm  
    success_url = reverse_lazy('users:login')
    template_name = 'registration/signup.html'

class CustomLoginView(LoginView):
    form_class = LoginForm 
    template_name = 'registration/login.html'