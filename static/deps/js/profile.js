function showSection(sectionId) {
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => section.style.display = 'none');
    document.getElementById(sectionId).style.display = 'block';
    // Сохраняем текущий раздел в localStorage
    localStorage.setItem('currentSection', sectionId);
  }

  document.addEventListener('DOMContentLoaded', function() {
    // Получаем сохраненный раздел из localStorage
    const currentSection = localStorage.getItem('currentSection');

    // Если раздел сохранен, показываем его
    if (currentSection) {
        showSection(currentSection);
    } else {
        // По умолчанию показываем первый раздел
        showSection('my-projects');
    }
    
});