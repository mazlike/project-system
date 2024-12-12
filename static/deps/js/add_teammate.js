document.addEventListener('DOMContentLoaded', function () {
    const maxTeamMembers = 4; // Максимальное количество участников
    const container = document.getElementById('team-members-container');
    const addButton = document.getElementById('add-team-member');
    let counter = 1;

    // Функция для добавления нового поля ввода
    function addTeamMemberInput() {
        if (counter >= maxTeamMembers) {
            addButton.disabled = true;
            return;
        }
        const newInput = document.createElement('div');
        newInput.className = 'team-member-input';
        newInput.innerHTML = `
            <input type="text" class="team-member-autocomplete" name="team_members_input_${counter}" placeholder="Введите username">
            <span class="remove-member" onclick="removeMember(this)">✖</span>
        `;
        container.appendChild(newInput);
        counter++;

        // Добавляем обработчик для нового поля
        const newField = newInput.querySelector('.team-member-autocomplete');
        setupAutocomplete(newField);
    }

    // Обработчик нажатия на кнопку "Добавить участника"
    addButton.addEventListener('click', addTeamMemberInput);

    // Функция для настройки автодополнения для поля
    function setupAutocomplete(field) {
        field.addEventListener('input', function () {
            const query = this.value;
            fetchUsers(query, function (results) {
                // Отобразить результаты в выпадающем списке
                const dropdown = document.createElement('ul');
                dropdown.className = 'autocomplete-dropdown';
                dropdown.style.position = 'absolute';
                dropdown.style.backgroundColor = '#38304e';
                dropdown.style.border = '1px solid #ccc';
                dropdown.style.listStyle = 'none';
                dropdown.style.padding = '0';
                dropdown.style.margin = '0';
                dropdown.style.width = field.offsetWidth + 'px';
                dropdown.style.zIndex = '1000';

                // Очищаем предыдущий выпадающий список, если он есть
                const oldDropdown = field.parentElement.querySelector('.autocomplete-dropdown');
                if (oldDropdown) oldDropdown.remove();

                // Добавляем результаты в выпадающий список
                results.forEach(result => {
                    const item = document.createElement('li');
                    item.textContent = result.username;
                    item.style.padding = '5px';
                    item.style.cursor = 'pointer';
                    item.addEventListener('click', function () {
                        field.value = result.username; // Выбираем значение
                        dropdown.remove(); // Убираем выпадающий список
                    });
                    dropdown.appendChild(item);
                });

                // Добавляем выпадающий список к полю ввода
                field.parentElement.appendChild(dropdown);
            });
        });
    }

    // Функция для отправки AJAX-запроса на сервер
    function fetchUsers(query, callback) {
        if (query.length < 3) {
            callback([]); // Если введено меньше 3 символов, не отправляем запрос
            return;
        }
        fetch(`/search-users/?query=${query}`)
            .then(response => response.json())
            .then(data => callback(data))
            .catch(error => {
                console.error('Ошибка при выполнении AJAX-запроса:', error);
                callback([]);
            });
    }

    // Настройка автодополнения для существующих полей
    const existingFields = document.querySelectorAll('.team-member-autocomplete');
    existingFields.forEach(field => setupAutocomplete(field));
    // Функция для удаления участника
    window.removeMember = function (element) {
        const inputContainer = element.parentElement; // Родительский элемент (div с классом .team-member-input)
        inputContainer.remove(); // Удаляем весь контейнер с полем и иконкой удаления
        counter--; // Уменьшаем счетчик
        addButton.disabled = false; // Включаем кнопку "Добавить участника", если было достигнуто максимальное количество участников
    };
});
document.querySelector('form').addEventListener('submit', function (event) {
    const teamMemberInputs = document.querySelectorAll('.team-member-autocomplete');
    teamMemberInputs.forEach(input => {
        if (!input.value.trim()) {
            // Если поле пустое, удаляем его из формы
            input.remove();
        }
    });
});