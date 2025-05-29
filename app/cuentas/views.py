# 📌 Imports organizados
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse

from .models import CustomUser, Noticia

# 📌 Función de inicio
def home(request):
    return render(request, 'pages/home.html')

# 📌 Autenticación y acceso
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        user = authenticate(request, username=username, password=password)

        if user:
            # Validamos correctamente `admitido`, `staff` y `superuser`
            if user.is_superuser or user.is_staff or user.admitido:
                login(request, user)
                request.session.save()
                return redirect(reverse("cuentas:profile"))
            else:
                return render(request, "auth/login.html", {"error_message": "Acceso denegado. Usuario no admitido."})
        else:
            return render(request, "auth/login.html", {"error_message": "Usuario o contraseña incorrectos."})

    return render(request, "auth/login.html")

@login_required
def profile_view(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.admitido):
        return render(request, 'access_denied.html')  # Redirige si el usuario no tiene acceso

    return render(request, 'users/profile.html', {'user': request.user})

# 📌 Registro de usuarios
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
            return render(request, 'auth/register.html', {'error_message': 'El nombre de usuario ya está en uso. Prueba otro.'})

        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'auth/register.html', {'error_message': 'El correo electrónico ya está registrado. Usa otro.'})

        # Crear usuario con área seleccionada
        user = CustomUser(
            username=username,
            nombre=nombre,
            apellido=apellido,
            email=email,
            area=area
        )
        user.set_password(password)  
        
        # ✅ Si el usuario elige "Staff", se marca como staff
        if area == "Staff":
            user.is_staff = True  

        user.save()

        return redirect('/')  

    return render(request, 'auth/register.html')

# 📌 Gestión de usuarios
@login_required
def users_list(request):
    users = CustomUser.objects.all()
    users_admitidos = users.filter(is_staff=True)
    users_no_admitidos = users.filter(is_staff=False)

    areas_dict = {}
    for user in users_admitidos:
        area = user.area if user.area else "Sin asignar"
        if area not in areas_dict:
            areas_dict[area] = []
        areas_dict[area].append(user)

    return render(request, "users/users_list.html", {
        "users_no_admitidos": users_no_admitidos,
        "areas_dict": areas_dict
    })

@login_required
def admit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    
    if not user.admitido:
        user.is_staff = True  
        user.admitido = True  
        user.save()
    
        if request.user.is_authenticated:
            update_session_auth_hash(request, user)

    return redirect("cuentas:users_list")

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    return redirect("cuentas:users_list")

@login_required
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        user.username = request.POST.get("username")
        user.nombre = request.POST.get("nombre")
        user.apellido = request.POST.get("apellido")
        user.email = request.POST.get("email")
        user.area = request.POST.get("area")
        
        # ✅ Actualiza `is_staff` si el usuario elige "Staff" o marca la opción
        user.is_staff = (request.POST.get("area") == "Staff") or request.POST.get("is_staff") == "on"

        user.save()
        return redirect("cuentas:users_list")

    return render(request, "fichas/edit_user.html", {"user": user})

@login_required
def update_password(request):
    user = request.user

    if request.method == 'POST':
        old_password = request.POST.get('old_password').strip()
        new_password = request.POST.get('new_password').strip()
        confirm_password = request.POST.get('confirm_password').strip()

        if not old_password or not new_password or not confirm_password:
            return render(request, 'auth/update_password.html', {'error_message': 'Todos los campos son obligatorios.'})

        if not user.check_password(old_password):
            return render(request, 'auth/update_password.html', {'error_message': 'Contraseña actual incorrecta.'})

        if len(new_password) < 8 or new_password != confirm_password:
            return render(request, 'auth/update_password.html', {'error_message': 'Contraseña inválida.'})

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user) 

        return redirect('cuentas:profile')

    return render(request, 'auth/update_password.html')

# 📌 Noticias
def noticias_view(request):
    noticias = Noticia.objects.all().order_by('-fecha_publicacion')
    return render(request, 'auth/news.html', {"noticias": noticias})

def obtener_noticias(request):
    noticias_json = [
        {
            "id": noticia.id,
            "titulo": noticia.titulo,
            "contenido": noticia.contenido[:200],
            "fecha": noticia.fecha_publicacion.strftime("%Y-%m-%d"),
            "portada": noticia.portada.url if noticia.portada else ""
        }
        for noticia in Noticia.objects.all().order_by('-fecha_publicacion')
    ]
    return JsonResponse(noticias_json, safe=False)

def cargar_noticias_view(request):
    return render(request, 'fichas/cargar_noticias.html')

# 📌 Secciones
def bellas_artes(request):
    return render(request, 'pages/bellas_artes.html')

def historia(request):
    return render(request, 'pages/historia.html')
