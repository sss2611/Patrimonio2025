from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/profile/')  # Redirige directamente al perfil
        return render(request, 'login.html', {'error': 'Credenciales inválidas'})  # Devuelve el login con error

    return render(request, 'login.html')

@login_required
def profile_view(request):
    if not request.user.is_superuser and not request.user.is_staff:
        return render(request, 'access_denied.html')  # Redirige a una página de acceso denegado
    
    return render(request, 'profile.html', {'user': request.user})

def register(request):
    return render(request, 'register.html')