document.addEventListener("DOMContentLoaded", async () => {
    const container = document.getElementById("noticiasContainer");

    try {
        const response = await fetch("/api/noticias/");  // ✅ Llamada a la API
        const noticias = await response.json();

        container.innerHTML = ""; // Limpiar mensaje de carga

        if (noticias.length === 0) {
            container.innerHTML = '<p class="text-center text-gray-400 text-xl">No hay noticias disponibles.</p>';
            return;
        }

        noticias.forEach(noticia => {
            const article = document.createElement("article");
            article.className = "bg-white shadow-md rounded-lg p-6 w-full max-w-3xl";

            article.innerHTML = `
                <h4 class="text-2xl font-bold mb-2">${noticia.titulo}</h4>
                <p class="text-gray-700 mb-4">${noticia.contenido}</p>
                <p class="text-sm text-gray-500">Publicado el ${new Date(noticia.fecha).toLocaleDateString()}</p>
            `;

            container.appendChild(article);
        });
    } catch (error) {
        console.error("Error al cargar noticias:", error);
        container.innerHTML = '<p class="text-center text-red-400 text-xl">Error al cargar noticias.</p>';
    }
});
