# -Language-Learning-Web-App---English-to-French-Translator-Flashcards-
This Flask web app helps users learn French through flashcards, translations, and speech synthesis. It uses **MarianMT** for translation, **gTTS** for pronunciation, and **BLEU scores** for learning assessment, with user progress stored in **Firebase Firestore**.
# ✨ Features:

  📖 Flashcards: Randomly generated English-French word pairs to practice translation.

  📝 Translation Tool: Translate English sentences to French using Helsinki-NLP's MarianMT model.

  🔊 Text-to-Speech (TTS): Converts translated text into speech for better pronunciation.

  🏆 Learning Assessment: Tests user knowledge using BLEU score evaluation.

  🎖️ Badge System: Awards Gold, Silver, or Bronze badges based on translation accuracy.

  🔥 Firebase Integration: Stores user responses and learning progress in Firestore.

  📅 Phrase of the Day: Daily random English phrase with French translation & pronunciation.

# 🚀 How to Run:

1. Clone the repository:
   
   git clone https://github.com/your-username/your-repo-name.git

   cd your-repo-name
   
2. Set Up Firebase
   
   Add your firebase-key.json to the project folder.

   Update cred = credentials.Certificate('firebase-key.json') with your correct path.

3. Run the App:
   
   python app.py

💡 Contributions Welcome! Feel free to fork, improve, and submit pull requests. 🚀
