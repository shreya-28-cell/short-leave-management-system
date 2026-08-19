from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import UserLoginView, dashboard

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]