
from django.urls import path
from .views import UserRegistrationView
urlpatterns = [
    
    path('register/',UserRegistrationView.as_view(),name='register' ),
    # path('home/',UserRegistrationView.as_view(),name='home' ),
]
