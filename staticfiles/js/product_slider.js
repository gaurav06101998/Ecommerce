document.addEventListener("DOMContentLoaded", function() {
  const slider = document.querySelector('.product-slider');
  const slides = document.querySelectorAll('.product-slider-item');
  const dots = document.querySelectorAll('.dot');
  let currentSlide = 0;
  const totalSlides = slides.length;

  // Function to update the displayed slide and active dot
  function showSlide(index) {
    if (index >= totalSlides) {
      currentSlide = 0;
    } else if (index < 0) {
      currentSlide = totalSlides - 1;
    } else {
      currentSlide = index;
    }

    // Update slider position
    slider.style.transform = `translateX(-${currentSlide * 100}%)`;

    // Update the active dot
    dots.forEach(dot => dot.classList.remove('active'));
    dots[currentSlide].classList.add('active');
  }

  // Show the first slide by default
  showSlide(currentSlide);

  // Navigation buttons (Prev and Next)
  const prevBtn = document.querySelector('.prev-btn');
  const nextBtn = document.querySelector('.next-btn');

  if (prevBtn) {
    prevBtn.addEventListener('click', function() {
      showSlide(currentSlide - 1);
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', function() {
      showSlide(currentSlide + 1);
    });
  }

  // Auto slide every 5 seconds
  setInterval(() => {
    showSlide(currentSlide + 1);
  }, 5000);

  // Add event listeners to each dot to change the slide
  dots.forEach((dot, index) => {
    dot.addEventListener('click', function() {
      showSlide(index); // Show the slide corresponding to the clicked dot
    });
  });
});
