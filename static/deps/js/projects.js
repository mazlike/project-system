function showBlock(blockId) {
    const blocks = document.querySelectorAll('.block');
    blocks.forEach(block => {
        block.style.display = (block.id === blockId) ? 'block' : 'none';
    });

    const projectTitle = document.querySelector('.project-title');
    projectTitle.textContent = document.querySelector(`.navigation-item[onclick="showBlock('${blockId}')"]`).textContent;
    // Сохраняем текущий блок в localStorage
    localStorage.setItem('currentBlock', blockId);
}

function toggleDropdown() {
    const dropdown = document.getElementById('avatar-dropdown');
    dropdown.classList.toggle('show');
}

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.style.display = 'block'; // Показываем модальное окно
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.style.display = 'none'; // Скрываем модальное окно
}

function disableModalCloseOnOutsideClick(modalId) {
    window.onclick = function (event) {
    const modal = document.getElementById(modalId);
    const modalDialog = modal ? modal.querySelector('.modal-dialog') : null;

    // Проверяем, был ли клик за пределами .modal-dialog
    if (modal && event.target === modal && !modalDialog.contains(event.target)) {
        // Игнорируем клик (не закрываем окно)
        event.stopPropagation(); // Предотвращаем дальнейшее всплытие события
    }
    };
}
disableModalCloseOnOutsideClick('taskModal');
disableModalCloseOnOutsideClick('noteModal');

document.addEventListener('DOMContentLoaded', () => {
    // Удаляем window.onload, чтобы избежать конфликта
    // window.onload = function() { showBlock('team'); }

    // Получаем последний активный блок из localStorage
    const lastBlockId = localStorage.getItem('currentBlock');

    // Если блок был сохранён, показываем его
    if (lastBlockId) {
        showBlock(lastBlockId);
    } else {
        // По умолчанию показываем первый блок
        const firstBlockId = document.querySelectorAll('.block')[0].id;
        showBlock(firstBlockId);
    }
    const hasEvaluation = document.getElementById('has-evaluation').value === "true";

    if (hasEvaluation) {
        // Блокируем все интерактивные элементы
        const interactiveElements = document.querySelectorAll('button, input, textarea, select');
        interactiveElements.forEach(element => {
            element.classList.add('disabled');
        });
    }

}); 