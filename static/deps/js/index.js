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
function closeModal(modalId) {
    document.getElementById(modalId).style.display = "none";
}

// Закрытие по клику вне модального окна
window.addEventListener("click", function(event) {
    if (event.target.classList.contains("modal")) {
        event.target.style.display = "none";
    }
});
