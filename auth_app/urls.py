# auth_app/urls.py
from django.urls import path
from .views import SignupView, LoginView, UserView

urlpatterns = [
    path('signup', SignupView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('user', UserView.as_view(), name='user'),
]