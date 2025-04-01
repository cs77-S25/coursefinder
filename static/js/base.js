// base.js

// Update difficulty value display dynamically as the slider moves
const difficultySlider = document.getElementById('difficulty');
const difficultyValue = document.getElementById('difficulty-value');

difficultySlider.addEventListener('input', function() {
    difficultyValue.textContent = difficultySlider.value;
});




