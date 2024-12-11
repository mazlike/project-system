document.addEventListener('DOMContentLoaded', function() {
    const projectItems = document.querySelectorAll('.prj-item');
    const projectDescription = document.getElementById('prj-description');
    const addButton = document.getElementById('add-button');
    const applyForm = document.getElementById('apply-form');

    projectItems.forEach(item => {
        item.addEventListener('click', function() {
            projectItems.forEach(item => item.classList.remove('active'));
            const description = item.getAttribute('data-description');
            const projectId = item.getAttribute('data-id');
            projectDescription.textContent = description;
            this.classList.add('active');
            // Обновляем action в форме
            applyForm.action = `/projects/${projectId}/apply/`;
            addButton.style.display = 'block';
        });
    });
});
