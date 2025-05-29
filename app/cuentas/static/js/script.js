// BOTON DE ACCESO EN HOME
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

// BOTON DE LOGIN
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
