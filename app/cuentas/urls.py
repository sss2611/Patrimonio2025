from django.urls import path
from . import views

app_name = 'cuentas'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'), 
    path('profile/', views.profile_view, name='profile'),
    path('register/', views.register, name='register'),    
    # path('users/',views.users_list, name='users_list'),
]