// quiz.js
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
