from django.urls import path
from .views import register_view, logout_view, login_view, profile_view

app_name = 'authentication'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('profile/', profile_view, name='profile'),
]
