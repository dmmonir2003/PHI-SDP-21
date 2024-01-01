from django.shortcuts import render,redirect
from django.views.generic import FormView,UpdateView
# from django.views.generic.edit import UpdateView

from .forms import UserForm,UserUpdateForm
from django.contrib.auth import login,logout
from django.contrib.auth.views import LoginView,LogoutView
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
    
class UserLoginView(LoginView):
    template_name='accounts/user_login.html'
    # success_url=reverse_lazy('home') ?---ata hossa na kano
    def get_success_url(self):
        return reverse_lazy('home')
     
class UserLogoutView(LogoutView):
      def get_success_url(self):
         if self.request.user.is_authenticated:
             logout(self.request)
         return  reverse_lazy('home')

class UserProfileUpdate(UpdateView):
    template_name='accounts/profile.html'
    form_class=UserUpdateForm
    success_url=reverse_lazy('home')
    def get_object(self, queryset=None):
        return self.request.user
    
# class UserProfileUpdate(View):
#     template_name='accounts/profile.html'
    

#     def get(self,request):
#         form=UserUpdateForm(instance=request.user)
#         return render(request,self.template_name,{'form':form})
#     def post(self,request):
#         form=UserUpdateForm(request.POST,instance=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#         return render(request,self.template_name,{'form':form})