document.addEventListener('DOMContentLoaded', () => {
    const slidesContainer = document.querySelector('.slides-container');
    const slides = document.querySelectorAll('.slide');
    const prevButton = document.querySelector('.prev');
    const nextButton = document.querySelector('.next');
    const radioButtons = document.querySelectorAll('input[name="carousel"]');
    let currentIndex = 0;
    let autoSwitchInterval;
    let userInteractionTimeout;

    const switchSlide = (newIndex) => {
        slidesContainer.style.transform = `translateX(-${newIndex * 100}%)`;
        radioButtons[newIndex].checked = true;
        currentIndex = newIndex;
    };

    const nextSlide = () => {
        const newIndex = (currentIndex + 1) % slides.length;
        switchSlide(newIndex);
    };

    const prevSlide = () => {
        const newIndex = (currentIndex - 1 + slides.length) % slides.length;
        switchSlide(newIndex);
    };

    const resetAutoSwitch = () => {
        clearTimeout(userInteractionTimeout);
        clearInterval(autoSwitchInterval);
        userInteractionTimeout = setTimeout(() => {
            autoSwitchInterval = setInterval(nextSlide, 10000);
        }, 30000);
    };

    // Event listeners for buttons and radio buttons
    nextButton.addEventListener('click', () => {
        nextSlide();
        resetAutoSwitch();
    });

    prevButton.addEventListener('click', () => {
        prevSlide();
        resetAutoSwitch();
    });

    radioButtons.forEach((radio, index) => {
        radio.addEventListener('change', () => {
            switchSlide(index);
            resetAutoSwitch();
        });
    });

    // Initialize the first slide and start automatic switching
    switchSlide(currentIndex);
    autoSwitchInterval = setInterval(nextSlide, 10000);
});