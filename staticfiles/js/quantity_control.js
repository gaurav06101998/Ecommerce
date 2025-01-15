document.addEventListener("DOMContentLoaded", function () {
  const decrementBtns = document.querySelectorAll(".decrement-btn");
  const incrementBtns = document.querySelectorAll(".increment-btn");
  const quantityInputs = document.querySelectorAll("input[name='quantity']");

  // Decrease Quantity
  decrementBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      const quantityInput = this.nextElementSibling;
      let currentValue = parseInt(quantityInput.value, 10);
      if (currentValue > 1) {
        quantityInput.value = currentValue - 1;
      }
    });
  });

  // Increase Quantity
  incrementBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      const quantityInput = this.previousElementSibling;
      let currentValue = parseInt(quantityInput.value, 10);
      quantityInput.value = currentValue + 1;
    });
  });

  // Ensure valid input manually
  quantityInputs.forEach((input) => {
    input.addEventListener("input", function () {
      if (this.value < 1) {
        this.value = 1; // Reset to 1 if the user enters a value below 1
      }
    });
  });
});
