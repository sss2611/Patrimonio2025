function login() {
    // Mostrar alerta con opciones
    Swal.fire({
        title: "Bienvenido a la Dirección de Patrimonio Cultural",
        imageUrl: faviconUrl,
        imageWidth: 100,
        imageHeight: 100,
        showCancelButton: true,
        confirmButtonText: "Ingresar",
        cancelButtonText: "Registrar"
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = "/login/"; 
        } else if (result.dismiss === Swal.DismissReason.cancel) {
            window.location.href = "/register/";
        }
    });
}

document.addEventListener("DOMContentLoaded", function () {
    let loginBtn = document.getElementById("loginBtn");

    if (loginBtn) {
        loginBtn.addEventListener("click", function() {
            console.log("Botón presionado"); // Verifica si el evento se ejecuta

            let email = document.getElementById("emailBox").value;
            let password = document.getElementById("passBox").value;

            if (!email || !password) {
                alert("Por favor, introduce tu usuario y contraseña.");
                return;
            }

            let csrfTokenElement = document.querySelector("[name=csrfmiddlewaretoken]");
            let csrfToken = csrfTokenElement ? csrfTokenElement.value : null;
            
            if (!csrfToken) {
                console.error("No se encontró el token CSRF.");
                return;
            }

            let formData = new URLSearchParams();
            formData.append("username", email);
            formData.append("password", password);

            fetch('/login/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: formData.toString()
            })
            .then(response => response.json())
            .then(data => {
                console.log("Respuesta del servidor:", data); // Para depuración

                if (data.success && data.redirect_url) {
                    setTimeout(() => {
                        window.location.href = data.redirect_url; // Redirige con un pequeño retraso
                    }, 500);
                } else {
                    alert("Credenciales incorrectas. Inténtalo de nuevo.");
                }
            })
            .catch(error => console.error("Error en la autenticación:", error));
        });
    } else {
        console.error("No se encontró el botón de login.");
    }
});

// boton de regitro
async function fetchUsers() {
    try {
        const response = await fetch("/users_list/"); // Llamada a la API
        const data = await response.json();
        const usersList = document.getElementById("usersList");
        usersList.innerHTML = ""; // Limpiar lista antes de agregar elementos

        data.users.forEach(user => {
            const listItem = document.createElement("li");
            listItem.className = "list-group-item d-flex justify-content-between align-items-center";
            listItem.innerHTML = `
                <div>
                    <strong>Usuario:</strong> ${user.username} <br>
                    <strong>Email:</strong> ${user.email} <br>
                    <strong>Área:</strong> ${user.area ? user.area : "Sin asignar"}
                </div>
                <div class="d-flex align-items-center">
                    ${!user.is_staff && !user.is_superuser ? `
                        <i class="bi bi-check-circle text-success cursor-pointer" onclick="admitUser(${user.id})" style="font-size: 1.5em;"></i>
                    ` : '<span class="badge bg-warning text-dark me-2">Admitido</span>'}
                </div>
            `;

            usersList.appendChild(listItem);
        });
    } catch (error) {
        console.error("Error al obtener usuarios:", error);
    }
}

async function admitUser(userId) {
    try {
        const response = await fetch(`/admit_user/${userId}/`, { method: "POST" });
        const result = await response.json();
        alert(result.message);
        fetchUsers(); // Recargar lista
    } catch (error) {
        console.error("Error al admitir usuario:", error);
    }
}

// Recargar cuandoelimine usuarios
document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".delete-user").forEach(button => {
        button.addEventListener("click", async function() {
            let userId = this.getAttribute("data-user-id");

            try {
                let response = await fetch(`/delete/${userId}/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": "{{ csrf_token }}",
                        "Content-Type": "application/json"
                    }
                });

                if (response.status === 204) {
                    this.closest(".col-12").remove();  // Elimina el usuario sin recargar
                    setTimeout(() => {
                        location.reload();  // Recarga la página después de 500 ms
                    }, 100);
                }
            } catch (error) {
                console.error("Error al eliminar usuario:", error);
            }
        });
    });
});

