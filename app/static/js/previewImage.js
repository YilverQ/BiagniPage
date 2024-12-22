function previewImage(event, previewId, currentImageId) {
    const file = event.target.files[0];
    const reader = new FileReader();
    
    // Primero, ocultar la imagen actual si hay alguna
    const currentImage = document.getElementById(currentImageId);
    if (currentImage) {
        currentImage.classList.add('hidden'); // Ocultar imagen actual
    }

    // Ocultar la vista previa previa si hay alguna
    const preview = document.getElementById(previewId);
    preview.classList.remove('hidden'); // Asegurarse de que la vista previa está visible

    reader.onload = function(e) {
        preview.src = e.target.result; // Asignar la nueva imagen
    }
    
    if (file) {
        reader.readAsDataURL(file); // Leer el archivo de imagen seleccionado
    }
}