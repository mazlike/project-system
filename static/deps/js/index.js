// Открытие модального окна при нажатии на кнопки "Преподаватель" и "Студент"
// document.getElementById("teacher-button").addEventListener("click", function() {
//     document.getElementById("modal-teacher").style.display = "flex";  // Показываем модальное окно
//     document.getElementById("teacher-button").classList.add("selected");
//     document.getElementById("student-button").classList.remove("selected");
// });

document.getElementById("entry-button").addEventListener("click", function() {
    document.getElementById("modal-entry").style.display = "flex";  // Показываем модальное окно
    document.getElementById("entry-button").classList.add("selected");
});

document.getElementById("reg-button").addEventListener("click", function() {
    document.getElementById("modal-reg").style.display = "flex";  // Показываем модальное окно
    document.getElementById("reg-button").classList.add("selected");
});

// Закрытие модальных окон
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.style.display = 'block'; // Показываем модальное окно
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.style.display = 'none'; // Скрываем модальное окно
}

// неЗакрытие по клику вне модального окна
window.onclick = function (event) {
    const modal = document.getElementById(modalId);
    const modalDialog = modal ? modal.querySelector('.modal-dialog') : null;

    // Проверяем, был ли клик за пределами .modal-dialog
    if (modal && event.target === modal && !modalDialog.contains(event.target)) {
        // Игнорируем клик (не закрываем окно)
        event.stopPropagation(); // Предотвращаем дальнейшее всплытие события
    }
    };