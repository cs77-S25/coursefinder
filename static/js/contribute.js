const difficultySlider = document.getElementById("difficulty");
const difficultyValue = document.getElementById("difficulty-value");

difficultySlider.addEventListener("input", function () {
    difficultyValue.textContent = this.value;
});

function prepareEmbeddingText() {
    const courseName = document.getElementById("course-name").value;
    const professor = document.getElementById("professor").value;
    const department = document.getElementById("department").value;
    const attributes = document.getElementById("attributes").value;
    const structure = document.getElementById("structure").value;
    const enjoyability = document.getElementById("enjoyability").value;
    const recommendation = document.getElementById("recommendation").value;
    const difficulty = difficultySlider.value;

    const embeddingText = `Course: ${courseName} (Department: ${department}) taught by Professor ${professor}. 
Difficulty: ${difficulty}/5. 
Enjoyability: ${enjoyability}/5. 
Recommended: ${recommendation}. 
Attributes: ${attributes}. 
Structure: ${structure}.`;

    document.getElementById("embedding-text").value = embeddingText.trim();
}
