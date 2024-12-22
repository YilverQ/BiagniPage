document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('sidebar');
    const toggleButton = document.getElementById('toggleSidebar');
    const mainContent = document.getElementById('main-content');
    
    toggleButton.addEventListener('click', function () {
        sidebar.classList.toggle('hidden');
        mainContent.classList.toggle('opacity-50'); // Esto crea el efecto de "oscurecer" el contenido cuando el menú está activo
    });
});
