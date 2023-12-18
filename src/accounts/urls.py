from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts.views import LoginUser, RegisterUser

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
]
