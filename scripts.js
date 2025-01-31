// scripts.js

// Function to handle the flashcard flip animation
function flipFlashcard(flashcard) {
    flashcard.classList.toggle('flipped');
}

// Function to initialize flashcards
function initializeFlashcards() {
    const flashcardContainers = document.querySelectorAll('.flashcard');

    flashcardContainers.forEach(flashcard => {
        flashcard.addEventListener('click', () => flipFlashcard(flashcard));
    });
}

// Function to handle form submission for translation
function handleTranslationForm(event) {
    event.preventDefault(); // Prevent the default form submission

    const textarea = document.querySelector('textarea[name="english_sentence"]');
    const sentence = textarea.value;

    // Simulate translation (replace with an actual API call)
    const simulatedTranslation = simulateTranslation(sentence);

    // Display translation result
    displayTranslationResult(sentence, simulatedTranslation);
}

// Simulate translation (mock function for demo)
function simulateTranslation(sentence) {
    // This is just a placeholder. You can replace it with an actual translation function or API call.
    return sentence.split(' ').reverse().join(' '); // Just reversing words as a mock translation
}

// Display translation result on the page
function displayTranslationResult(english, french) {
    const translationResultDiv = document.querySelector('.translation-result');
    translationResultDiv.innerHTML = `
        <h3>Translation</h3>
        <p><strong>English:</strong> ${english}</p>
        <p><strong>French:</strong> ${french}</p>
        <audio controls>
            <source src="path/to/your/audio/translation.mp3" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
    `;
}

// Attach event listeners for translation forms
function initializeTranslationForms() {
    const translationForms = document.querySelectorAll('form[action="{{ url_for("translate") }}"]');
    
    translationForms.forEach(translationForm => {
        translationForm.addEventListener('submit', handleTranslationForm);
    });
}

// Initialize function to handle all page functionalities
function initializePage() {
    // Initialize flashcards if present
    if (document.querySelector('.flashcard')) {
        initializeFlashcards();
    }

    // Initialize translation forms if present
    if (document.querySelector('form[action="{{ url_for("translate") }}"]')) {
        initializeTranslationForms();
    }
}

// Run the initialize function when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', initializePage);
