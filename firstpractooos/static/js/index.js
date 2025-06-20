document.addEventListener('DOMContentLoaded', function () {
  // Hero Slider
  const slides = document.querySelectorAll('.hero-slide');
  let currentSlide = 0;
  let slideInterval;

  function showSlide(index) {
    slides.forEach((slide, i) => {
      slide.classList.toggle('active', i === index);
    });
  }

  function nextSlide() {
    currentSlide = (currentSlide + 1) % slides.length;
    showSlide(currentSlide);
  }

  function startSlider() {
    slideInterval = setInterval(nextSlide, 5000);
  }

  function stopSlider() {
    clearInterval(slideInterval);
  }

  // Start the slider
  showSlide(currentSlide);
  startSlider();

  // Pause on hover (optional)
  const slider = document.querySelector('.hero-slider');
  slider.addEventListener('mouseenter', stopSlider);
  slider.addEventListener('mouseleave', startSlider);

  // Add touch events for mobile
  let touchStartX = 0;
  let touchEndX = 0;

  slider.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
    stopSlider();
  });

  slider.addEventListener('touchend', (e) => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
    startSlider();
  });

  function handleSwipe() {
    if (touchEndX < touchStartX - 50) {
      // Swipe left - next slide
      nextSlide();
    } else if (touchEndX > touchStartX + 50) {
      // Swipe right - previous slide
      currentSlide = (currentSlide - 1 + slides.length) % slides.length;
      showSlide(currentSlide);
    }
  }
});