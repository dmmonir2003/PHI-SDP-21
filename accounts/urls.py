
from django.urls import path
from .views import UserRegistrationView
urlpatterns = [
    
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('login/',UserRegistrationView.as_view(),name='login' ),
    path('logout/',UserRegistrationView.as_view(),name='logout' ),
    path('profile/',UserRegistrationView.as_view(),name='profile' ),
   
]
