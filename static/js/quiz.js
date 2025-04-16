document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const descriptorField = document.getElementById('personality_embedding_input');
    const subjectCheckboxes = document.querySelectorAll('input[name="subject"]');

    form.addEventListener('submit', function (e) {
        const descriptors = [];

        // Make sure at least one subject is selected
        let checkedSubjects = Array.from(subjectCheckboxes).filter(checkbox => checkbox.checked);
        if (checkedSubjects.length === 0) {
            e.preventDefault(); // Prevent form submission
            alert("Please select at least one subject.");
            return; // Exit early
        }

        // Get all checked checkboxes and radios with descriptors
        const inputs = form.querySelectorAll('input[type="checkbox"], input[type="radio"]');
        inputs.forEach(input => {
            if (input.checked && input.dataset.descriptor) {
                descriptors.push(input.dataset.descriptor);
            }
        });

        // Also grab the free-text input, using .trim() to get rid of accidental whitespace 
        const interestText = document.getElementById('interest')?.value.trim();

        if (interestText) descriptors.push(interestText);

        // Combine descriptors and set the hidden input's value
        descriptorField.value = descriptors.join(', ');
    });
});
