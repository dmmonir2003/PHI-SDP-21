
from django.urls import path
from .views import UserRegistrationView,UserLoginView,UserLogoutView,UserProfileUpdate,ChangepassView
urlpatterns = [
    
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('login/',UserLoginView.as_view(),name='login' ),
    path('logout/',UserLogoutView.as_view(),name='logout' ),
    path('profile/',UserProfileUpdate.as_view(),name='profile' ),
    path('pass_change/',ChangepassView.as_view(),name='pass_change' ),

   
]
