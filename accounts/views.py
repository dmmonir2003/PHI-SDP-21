from django.shortcuts import render
from django.views.generic import FormView
from .forms import UserForm
from django.contrib.auth import login
# Create your views here.


class UserRegistrationView(FormView):
     template_name=''
     form_class=UserForm
     success_url=''

     def form_valid(self, form):
         user=form.save()
         login(user)
         return super().form_valid(form)
     
     
     

