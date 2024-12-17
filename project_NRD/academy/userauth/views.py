from django.contrib.auth.views import LoginView  
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
class SignupView(CreateView):  
    form_class = UserCreationForm
    template_name = 'userauth/signup.html'
    success_url = reverse_lazy('login')

class UserLoginView(LoginView):
    template_name = 'userauth/login.html'
    redirect_authenticated_user = True

