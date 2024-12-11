document.addEventListener('DOMContentLoaded', function () {
    const messages = document.querySelectorAll('.messages li');
    messages.forEach((message) => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 500); // Удаление элемента через 0.5 сек после исчезновения
        }, 3000); // Сообщение исчезнет через 3 секунды
    });
});