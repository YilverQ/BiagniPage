let currentSection = 0;
const sections = document.querySelectorAll('.form-section');
const nextBtn = document.getElementById('nextBtn');
const prevBtn = document.getElementById('prevBtn');
const submitBtn = document.getElementById('submitBtn');

function move(step) {
    sections[currentSection].classList.add('hidden');
    currentSection += step;
    
    if (currentSection >= sections.length - 1) {
        nextBtn.classList.add('hidden');
        submitBtn.classList.remove('hidden');
    } else {
        nextBtn.classList.remove('hidden');
        submitBtn.classList.add('hidden');
    }
    
    if (currentSection <= 0) {
        prevBtn.classList.add('hidden');
    } else {
        prevBtn.classList.remove('hidden');
    }
    
    sections[currentSection].classList.remove('hidden');
    updateStepIcons();
}

function moveToSection(sectionIndex) {
    sections[currentSection].classList.add('hidden');
    currentSection = sectionIndex;
    sections[currentSection].classList.remove('hidden');
    updateStepIcons();
}

function updateStepIcons() {
    const steps = document.querySelectorAll('.step-icon');
    steps.forEach((step, index) => {
        if (index <= currentSection) {
            step.classList.add('text-green-600');
            step.classList.remove('text-gray-400');
        } else {
            step.classList.add('text-gray-400');
            step.classList.remove('text-green-600');
        }
    });
}

document.addEventListener('DOMContentLoaded', function () {
    move(0);  // Iniciar en la primera sección
    updateStepIcons();  // Asegúrate de que el primer paso esté resaltado
});
