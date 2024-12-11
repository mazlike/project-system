document.addEventListener('DOMContentLoaded', function () {
    const regForm = document.getElementById('registration-form');
    const messagesContainer = document.getElementById('messages-container');

    regForm.addEventListener('submit', async function (event) {
        event.preventDefault(); // Останавливаем стандартное поведение формы

        const formData = new FormData(regForm);

        try {
            const response = await fetch(regForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' // Указываем, что это AJAX-запрос
                }
            });

            const data = await response.json();

            if (response.ok && data.success) {
                // Если регистрация успешна
                messagesContainer.innerHTML = `
                    <div class="success-message">
                        <p>Вы успешно зарегистрированы!</p>
                    </div>`;
                regForm.reset(); // Сбрасываем форму
            } else {
                // Если есть ошибки, обновляем содержимое модального окна
                const modalContent = document.querySelector('#modal-reg .modal-content');
                modalContent.innerHTML = data.html;
            }
        } catch (error) {
            console.error('Ошибка при отправке формы:', error);
        }
    });

    
});
