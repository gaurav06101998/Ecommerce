document.addEventListener('DOMContentLoaded', function() {
	const slider = document.querySelector('.slider');
	const slides = document.querySelectorAll('.slider-item');
	const totalSlides = slides.length;
	let currentIndex = 0;

	function goToNextSlide() {
			currentIndex = (currentIndex + 1) % totalSlides;
			slider.style.transform = `translateX(-${currentIndex * 100}%)`;
	}

	function goToPrevSlide() {
			currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
			slider.style.transform = `translateX(-${currentIndex * 100}%)`;
	}

	// Automatically go to next slide every 5 seconds
	setInterval(goToNextSlide, 5000);  // Change 5000 for different speeds (in ms)

	// Button actions
	const nextBtn = document.querySelector('.next-btn');
	const prevBtn = document.querySelector('.prev-btn');

	nextBtn.addEventListener('click', goToNextSlide);
	prevBtn.addEventListener('click', goToPrevSlide);
});