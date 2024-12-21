// flash_messages.js
document.addEventListener('DOMContentLoaded', function() {
    // Cerrar automáticamente los mensajes después de 5 segundos
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300); // Eliminar después de 300ms
        });
    }, 4000);

    // Agregar evento de clic para cerrar mensajes manualmente
    const closeButtons = document.querySelectorAll('.alert button');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.parentElement.style.display = 'none'; // Cerrar el mensaje al hacer clic en "X"
        });
    });
});
