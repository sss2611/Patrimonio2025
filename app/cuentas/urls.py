from django.urls import path
from . import views

app_name = 'cuentas'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'), 
    path('profile/', views.profile_view, name='profile'),
    path('register/', views.register, name='register'), 
    path('users/',views.users_list, name='users'), 
    path("admit_user/<int:user_id>/", views.admit_user, name="admit_user"),
    path('delete/<int:user_id>/', views.delete_user, name='delete_user')
    ]