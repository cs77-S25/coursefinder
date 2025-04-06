// quiz.js
document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const descriptorField = document.getElementById('personality_embedding_input');

    form.addEventListener('submit', function (e) {
        const descriptors = [];

        // Get all input elements
        const inputs = form.querySelectorAll('input[type="checkbox"], input[type="radio"]');
        inputs.forEach(input => {
            if (input.checked && input.dataset.descriptor) {
                descriptors.push(input.dataset.descriptor);
            }
        });

        // Also grab the free-text input
        const interestText = document.getElementById('interest')?.value;
        if (interestText) descriptors.push(interestText);

        // Combine descriptors and set the hidden input's value
        descriptorField.value = descriptors.join(', ');
    });
});

document.addEventListener('DOMContentLoaded', function () {
    // Example of additional functionality: Ensure at least one subject is selected.
    const subjectCheckboxes = document.querySelectorAll('input[name="subject"]');
    const form = document.querySelector('form');

    form.addEventListener('submit', function (e) {
        let checkedSubjects = Array.from(subjectCheckboxes).filter(checkbox => checkbox.checked);

        if (checkedSubjects.length === 0) {
            e.preventDefault(); // Prevent form submission
            alert("Please select at least one subject.");
        }
    });
});
