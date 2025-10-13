document.addEventListener("DOMContentLoaded", () => {
    const filas = document.querySelectorAll("tbody tr");
    filas.forEach(fila => {
    fila.addEventListener("mouseenter", () => fila.style.background = "#e6f0ff");
    fila.addEventListener("mouseleave", () => fila.style.background = "white");
    });
});
