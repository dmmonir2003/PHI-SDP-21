from django.template.loader import render_to_string
from django.views.generic import FormView,UpdateView
# from django.views.generic.edit import UpdateView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserForm,UserUpdateForm
from django.contrib.auth import login,logout
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy
from django.core.mail import EmailMultiAlternatives

from django.contrib import messages

# Create your views here.

def transaction_email_to_user(user,subject,template):
     
        message=render_to_string(template,{
            'user':user,
            
        })
        send_email=EmailMultiAlternatives(subject,'',to=[user.email])
        send_email.attach_alternative(message,'text/html')
        send_email.send()

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
    


class ChangepassView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/pass_change.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('profile')
    def form_valid(self, form):
        response = super().form_valid(form)
        
        subject = 'Password Change'
        template = 'accounts/email_change_pass.html'
        message = render_to_string(template, {'user': self.request.user})
        
        send_email = EmailMultiAlternatives(subject, '', to=[self.request.user.email])
        send_email.attach_alternative(message, 'text/html')
        send_email.send()
        messages.success(self.request,'Password change Successfully')
        return response

    
#  class UserProfileUpdate(View):
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