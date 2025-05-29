from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from .models import Noticia

def home(request):
    return render(request, 'pages/home.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Validamos correctamente `admitido`, `staff` y `superuser`
            if user.is_superuser or user.is_staff or getattr(user, "admitido", False):
                login(request, user)
                request.session.save()
                return redirect(reverse("cuentas:profile"))  # Redirige correctamente
            else:
                return render(request, "auth/login.html", {"error_message": "Acceso denegado. Usuario no admitido."})
        else:
            return render(request, "auth/login.html", {"error_message": "Usuario o contraseña incorrectos."})

    return render(request, "auth/login.html")

@login_required
def profile_view(request):
    if not (request.user.is_superuser or request.user.is_staff or getattr(request.user, "admitido", False)):
        return render(request, 'access_denied.html')  # Redirige si el usuario no tiene acceso
    
    return render(request, 'users/profile.html', {'user': request.user})



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

        # Crear usuario
        user = CustomUser(
            username=username,
            nombre=nombre,
            apellido=apellido,
            email=email,
            area=area
        )
        user.set_password(password)  # 🔹 Guarda la contraseña correctamente
        user.save()

        return redirect('/')  # Redirige al home después del registro exitoso

    return render(request, 'auth/register.html')


#@login_required
def users_list(request):
    # Obtener todos los usuarios
    users = CustomUser.objects.all().values("id", "username", "email", "area", "is_staff", "is_superuser")

    # Filtrar usuarios admitidos
    users_admitidos = [user for user in users if user["is_staff"]]
    
    # Filtrar usuarios no admitidos (recién registrados)
    users_no_admitidos = [user for user in users if not user["is_staff"]]

    # Organizar usuarios admitidos por área
    areas_dict = {}
    for user in users_admitidos:
        area = user["area"] if user["area"] else "Sin asignar"
        if area not in areas_dict:
            areas_dict[area] = []
        areas_dict[area].append(user)

    return render(request, "users/users_list.html", {
        "users_no_admitidos": users_no_admitidos,
        "areas_dict": areas_dict
    })

def admit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    # No cambiar el área al admitir el usuario
    user.is_staff = True  
    user.admitido = True  # Usamos el campo admitido en lugar de is_staff
    user.save()

    if request.user.is_authenticated:
        update_session_auth_hash(request, user)
   
    return redirect("cuentas:users_list")

def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()  # Eliminar usuario
    return redirect("cuentas:users_list")  # Redirige para recargar la lista sin el usuario eliminado

def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        user.username = request.POST.get("username")
        user.nombre = request.POST.get("nombre")
        user.apellido = request.POST.get("apellido")
        user.email = request.POST.get("email")
        user.area = request.POST.get("area")
        user.save()
        return redirect("cuentas:users_list")

    return render(request, "fichas/edit_user.html", {"user": user})

@login_required
def update_password(request):
    user = request.user  # 🔹 Obtiene el usuario autenticado

    if request.method == 'POST':
        old_password = request.POST.get('old_password').strip()
        new_password = request.POST.get('new_password').strip()
        confirm_password = request.POST.get('confirm_password').strip()

        #Verificar que los campos no estén vacíos
        if not old_password or not new_password or not confirm_password:
            return render(request, 'auth/update_password.html', {'error_message': 'Todos los campos son obligatorios.'})

        #Verificar si la contraseña actual es correcta
        if not user.check_password(old_password):
            return render(request, 'auth/update_password.html', {'error_message': 'Contraseña actual incorrecta.'})

        #Verificar que la nueva contraseña tenga al menos 8 caracteres
        if len(new_password) < 8:
            return render(request, 'auth/update_password.html', {'error_message': 'La nueva contraseña debe tener al menos 8 caracteres.'})

        #Verificar que la nueva contraseña coincida con la confirmación
        if new_password != confirm_password:
            return render(request, 'auth/update_password.html', {'error_message': 'Las contraseñas no coinciden.'})

        #Cambiar la contraseña y actualizar la sesión
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)  # Mantiene al usuario autenticado después del cambio

        return redirect('cuentas:profile')  # Redirige al perfil después de actualizar

    return render(request, 'auth/update_password.html')

    # news
def noticias_view(request):
    noticias = Noticia.objects.all().order_by('-fecha_publicacion')  # ✅ Obtener noticias de la BD
    return render(request, 'auth/news.html', {"noticias": noticias})  # ✅ Pasar noticias al template

def obtener_noticias(request):
    noticias = Noticia.objects.all().order_by('-fecha_publicacion')
    noticias_json = [
        {
            "id": noticia.id,
            "titulo": noticia.titulo,
            "contenido": noticia.contenido[:200],  # Limitar caracteres
            "fecha": noticia.fecha_publicacion.strftime("%Y-%m-%d"),
            "portada": noticia.portada.url if noticia.portada else ""
        }
        for noticia in noticias
    ]
    return JsonResponse(noticias_json, safe=False)

def cargar_noticias_view(request):
    return render(request, 'fichas/cargar_noticias.html')

def bellas_artes(request):
    return render(request, 'pages/bellas_artes.html')

def historia(request):
   return render(request, 'pages/historia.html')