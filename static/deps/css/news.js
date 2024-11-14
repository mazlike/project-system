document.addEventListener('DOMContentLoaded', function () {
    const newsItems = document.querySelectorAll('.news-item');
    const newsTitle = document.getElementById('news-title');
    const newsText = document.getElementById('news-text');

    // Данные новостей
    const newsContent = [
        { title: "Новость 1", text: "Текст новости 1. Здесь будет описание первой новости." },
        { title: "Новость 2", text: "Текст новости 2. Здесь будет описание второй новости." },
        { title: "Новость 3", text: "Текст новости 3. Здесь будет описание третьей новости." }
    ];

    // При клике на новость показываем её текст
    newsItems.forEach((item, index) => {
        item.addEventListener('click', () => {
            newsTitle.textContent = newsContent[index].title;
            newsText.textContent = newsContent[index].text;
        });
    });

    // Автоматически открываем первую новость при загрузке страницы
    newsTitle.textContent = newsContent[0].title;
    newsText.textContent = newsContent[0].text;

    // Слайдер с изображениями
    const slider = document.querySelector('.slider');
    const slides = slider.querySelectorAll('.announcement');
    const sliderButtons = document.querySelectorAll('.slider-btn');
    let currentSlide = 0;

    // Функция для смены слайдов
    function changeSlide() {
        slides[currentSlide].style.opacity = 0; // Скрываем текущий слайд
        sliderButtons[currentSlide].classList.remove('active'); // Убираем активный класс с текущей кнопки

        currentSlide = (currentSlide + 1) % slides.length; // Переходим к следующему слайду
        slides[currentSlide].style.opacity = 1; // Показываем новый слайд
        sliderButtons[currentSlide].classList.add('active'); // Делаем кнопку активной для нового слайда
    }

    // Переключение слайдов каждые 30 секунд
    setInterval(changeSlide, 30000);

    // Ручное переключение слайдов через кнопки
    sliderButtons.forEach((btn, index) => {
        btn.addEventListener('click', () => {
            slides[currentSlide].style.opacity = 0; // Скрываем текущий слайд
            sliderButtons[currentSlide].classList.remove('active'); // Убираем активный класс с текущей кнопки

            currentSlide = index; // Переключаем на выбранный слайд
            slides[currentSlide].style.opacity = 1; // Показываем новый слайд
            sliderButtons[currentSlide].classList.add('active'); // Делаем кнопку активной
        });
    });

    // Инициализация первого слайда
    slides[currentSlide].style.opacity = 1;
    sliderButtons[currentSlide].classList.add('active');
});

