from flask import Flask, render_template, request, redirect, url_for, flash
from transformers import MarianMTModel, MarianTokenizer
from gtts import gTTS
import os
import random 
from datasets import load_dataset
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate('firebase-key.json')  # Update with your path
firebase_admin.initialize_app(cred)

# Initialize Firestore database
db = firestore.client()

# Loading the English-French Translation dataset
dataset = load_dataset('wmt14', 'fr-en')

# Loading the pre-trained MarianMT model and tokenizer
model_name = 'Helsinki-NLP/opus-mt-en-fr'
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

# Function to translate text using MarianMT Model
def translate_text(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True)
    translated = model.generate(**inputs)
    translation = tokenizer.decode(translated[0], skip_special_tokens=True)
    return translation

# Function to convert text to speech and save to a file 
def speak_text(text, lang='fr', filename='output.mp3'):
    tts = gTTS(text, lang=lang)
    tts.save(filename)

# Function to get flashcards from dataset
def get_flashcard():
    index = random.randint(0, len(dataset['train'])-1)
    english_text = dataset['train'][index]['translation']['en']
    french_text = dataset['train'][index]['translation']['fr']
    return english_text, french_text

# Function to get the Phrase of the Day and generate TTS with translation
def get_phrase_of_the_day():
    index = random.randint(0, len(dataset['train']) - 1)
    english_text = dataset['train'][index]['translation']['en']
    french_text = translate_text(english_text)

    return english_text, french_text

# Function to test the user's learning and calculate BLEU score with smoothing
def test_user_learning(flashcards, user_translations):
    total_score = 0
    smoothing_function = SmoothingFunction().method1  # Use SmoothingFunction to avoid zero BLEU scores

    for i, (english_text, correct_translation) in enumerate(flashcards):
        user_translation = user_translations[i]
        reference = [correct_translation.split()]
        candidate = user_translation.split()

        # Calculate BLEU score
        score = sentence_bleu(reference, candidate, smoothing_function=smoothing_function)
        total_score += score

    # Return average score
    return total_score / len(flashcards) if flashcards else 0

# Function to award badges based on the BLEU score
def award_badge(average_bleu_score):
    if average_bleu_score > 0.8:
        return "🎖️ Congratulations! You earned a GOLD badge!"
    elif average_bleu_score > 0.6:
        return "🥈 Great job! You earned a SILVER badge!"
    elif average_bleu_score > 0.4:
        return "🥉 Good effort! You earned a BRONZE badge!"
    else:
        return "Keep Practicing!"

# Function to store user responses in Firebase
def store_user_response(english_text, user_translation, correct_translation, bleu_score):
    doc_ref = db.collection('user_responses').add({
        'english_text': english_text,
        'user_translation': user_translation,
        'correct_translation': correct_translation,
        'bleu_score': bleu_score
    })

# Routes

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/flashcards', methods=['GET', 'POST'])
def flashcards():
    if request.method == 'POST':
        flashcards = []
        num_flashcards = int(request.form['num_flashcards'])
        for _ in range(num_flashcards):
            english_text, french_text = get_flashcard()
            flashcards.append((english_text, french_text))
        
        # Save the flashcards to session for user testing
        return render_template('flashcards.html', flashcards=flashcards)

    return render_template('flashcards.html')

@app.route('/test_flashcards', methods=['POST'])
def test_flashcards():
    flashcards = request.form.getlist('flashcards')
    user_translations = request.form.getlist('user_translations')
    
    average_bleu_score = test_user_learning(flashcards, user_translations)
    badge = award_badge(average_bleu_score)

    # Store each user's response in Firebase
    for (english_text, correct_translation), user_translation in zip(flashcards, user_translations):
        store_user_response(english_text, user_translation, correct_translation, average_bleu_score)

    return render_template('test_results.html', average_bleu_score=average_bleu_score, badge=badge)

@app.route('/phrase_of_the_day')
def phrase_of_the_day():
    english_text, french_text = get_phrase_of_the_day()
    speak_text(english_text, lang='en', filename='static/phrase_of_the_day_en.mp3')
    speak_text(french_text, lang='fr', filename='static/phrase_of_the_day_fr.mp3')
    
    return render_template('phrase_of_the_day.html', english_text=english_text, french_text=french_text)

@app.route('/translate', methods=['GET', 'POST'])
def translate():
    if request.method == 'POST':
        english_sentence = request.form['english_sentence']
        french_translation = translate_text(english_sentence)
        speak_text(french_translation, lang='fr', filename='static/translation.mp3')
        return render_template('translate.html', english_sentence=english_sentence, french_translation=french_translation)
    
    return render_template('translate.html')

if __name__ == '__main__':
    app.run(debug=True)
