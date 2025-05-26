from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from .models import CustomUser
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


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
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        nombre = request.POST.get('nombre').strip()
        apellido = request.POST.get('apellido').strip()
        email = request.POST.get('email').strip()
        area = request.POST.get('area')
        password = request.POST.get('password')

        # Verificar si el usuario ya existe
        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error_message': 'El nombre de usuario ya está en uso. Prueba otro.'})

        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error_message': 'El correo electrónico ya está registrado. Usa otro.'})

        # Crear usuario
        CustomUser.objects.create(
            username=username,
            nombre=nombre,
            apellido=apellido,
            email=email,
            area=area,
            password=make_password(password)
        )

        return render(request, 'register.html', {'success_message': 'Usuario registrado exitosamente!'})  # Envia mensaje de éxito

    return render(request, 'register.html')


#@login_required

def users_list(request):
    """Muestra la lista de usuarios en una página HTML."""
    users = CustomUser.objects.all()
    return render(request, "users_list.html", {"users": users})

@csrf_exempt
def admit_user(request, user_id):
    """Admite a un usuario cambiando su estado a 'staff'."""
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        user.is_staff = True
        user.save()
        return redirect("users_list")  # Redirigir después de admitir

    return JsonResponse({"error": "Método no permitido"}, status=405)

def delete_user(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"error": "Usuario no encontrado"}, status=404)
    
    if request.method == "POST":
        user.delete()
        return HttpResponse(status=204)  # Usuario eliminado sin redirección