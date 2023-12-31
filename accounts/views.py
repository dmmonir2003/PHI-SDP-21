from django.shortcuts import render
from django.views.generic import FormView
from .forms import UserForm
from django.contrib.auth import login
from django.urls import reverse_lazy
# Create your views here.

class UserRegistrationView(FormView):
    template_name = 'accounts/user_registration.html'
    form_class = UserForm
    success_url = reverse_lazy('register')
    
    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            login(self.request, user)
        return super().form_valid(form)
    
    def form_invalid(self, form):
       print(form.errors)
       return super().form_invalid(form)
     
