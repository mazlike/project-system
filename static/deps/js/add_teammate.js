document.addEventListener('DOMContentLoaded', function () {
    const teamMembersContainer = document.querySelectorAll('.team-members-container');

    teamMembersContainer.forEach(container => {
        const inputField = container.querySelector('.team-member-autocomplete');
        const confirmButton = container.querySelector('.confirm-member');
        const teamMembersList = container.querySelector('#team-members-list');
        const leaderSelect = document.querySelector(`#leader-select-${container.id.split('-').pop()}`);
        const hiddenField = document.createElement('input');
        hiddenField.type = 'hidden';
        hiddenField.name = 'team_members_input';
        container.appendChild(hiddenField);

        confirmButton.addEventListener('click', function () {
            const username = inputField.value.trim();

            // Проверяем, существует ли уже такой участник
            const existingUsernames = Array.from(teamMembersList.children).map(item => 
                item.textContent.replace('×', '').trim()
            );

            if (!username) {
                alert('Введите имя пользователя.');
                return;
            }

            if (existingUsernames.includes(username)) {
                alert('Этот пользователь уже добавлен в команду.');
                return;
            }

            // Добавляем в список участников
            const listItem = document.createElement('li');
            listItem.textContent = username;

            // Кнопка для удаления участника
            const removeButton = document.createElement('button');
            removeButton.textContent = '×';
            removeButton.addEventListener('click', function () {
                listItem.remove();
                updateTeamMembers();
            });

            listItem.appendChild(removeButton);
            teamMembersList.appendChild(listItem);

            // Добавляем участника в select лидера
            const option = document.createElement('option');
            option.value = username;
            option.textContent = username;
            leaderSelect.appendChild(option);

            updateTeamMembers();
            inputField.value = ''; // Очищаем поле ввода
        });

        function updateTeamMembers() {
            // Собираем всех участников из списка
            const usernames = Array.from(teamMembersList.children).map(item =>
                item.textContent.replace('×', '').trim()
            );
            hiddenField.value = usernames.join(',');

            // Удаляем отсутствующих участников из select лидера
            Array.from(leaderSelect.options).forEach(option => {
                if (option.value && !usernames.includes(option.value)) {
                    option.remove();
                }
            });

            // Добавляем новых участников в select лидера
            usernames.forEach(username => {
                if (!Array.from(leaderSelect.options).some(option => option.value === username)) {
                    const newOption = document.createElement('option');
                    newOption.value = username;
                    newOption.textContent = username;
                    leaderSelect.appendChild(newOption);
                }
            });
        }
    });

        // Найти все поля ввода с автозаполнением
    const autoCompleteFields = document.querySelectorAll('.team-member-autocomplete');

    // Шаблон dropdown-а
    const dropdownTemplate = document.getElementById('autocomplete-dropdown-template');

    // Создайте обработчик для каждой формы
    autoCompleteFields.forEach(inputField => {
        let dropdown = dropdownTemplate.content.cloneNode(true).querySelector('.autocomplete-dropdown');
        
        // Обработчик ввода
        inputField.addEventListener('input', function () {
            const query = inputField.value.trim();
            
            if (query.length > 1) { // Выполняем запрос только если введено больше 1 символа
                fetch(`/search-students/?query=${encodeURIComponent(query)}`)
                    .then(response => response.json())
                    .then(data => {
                        // Очистить предыдущие результаты
                        dropdown.querySelector('.autocomplete-items').innerHTML = '';
                        dropdown.style.display = 'block'; // Показать dropdown

                        // Отобразить результаты
                        data.forEach(user => {
                            const option = document.createElement('div');
                            option.className = 'autocomplete-item';
                            option.textContent = user.username;

                            // Добавляем обработчик клика для выбора пользователя
                            option.addEventListener('click', function () {
                                inputField.value = user.username; // Установить выбранное имя
                                dropdown.querySelector('.autocomplete-items').innerHTML = ''; // Очистить dropdown
                                dropdown.style.display = 'none'; // Скрыть dropdown
                            });

                            dropdown.querySelector('.autocomplete-items').appendChild(option);
                        });
                    })
                    .catch(error => {
                        console.error('Ошибка загрузки данных:', error);
                    });
            } else {
                dropdown.querySelector('.autocomplete-items').innerHTML = ''; // Очистить dropdown, если ввод слишком короткий
                dropdown.style.display = 'none';
            }
        });

        // Закрыть dropdown, если пользователь кликнул за его пределами
        document.addEventListener('click', function (event) {
            if (!dropdown.contains(event.target) && event.target !== inputField) {
                dropdown.querySelector('.autocomplete-items').innerHTML = '';
                dropdown.style.display = 'none';
            }
        });

        // Добавление dropdown в DOM после каждого input поля
        inputField.parentNode.appendChild(dropdown);
    });

});
