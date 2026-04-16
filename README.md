Real-Time Speech Translator
The Real-Time Speech Translator is an intelligent web application built with Streamlit that 
enables seamless two-way conversation translation between multiple languages using voice input
and output. This project bridges language barriers by combining advanced speech recognition, translation,
and text-to-speech technologies.

Key Features:
The application supports 14 languages including English, Thai, Spanish, French, German, 
Japanese, Korean, Chinese, Hindi, Portuguese, and several Indian languages (Telugu, Malayalam, Tamil, Kannada).
Users can select their native language and target language through an intuitive sidebar interface.

Core Functionality:
The app captures speech through the device microphone with intelligent noise handling—it automatically
adjusts for ambient noise with a listening timeout of 10 seconds, making it reliable even in noisy environments.
The speech is converted to text using Google Speech-to-Text API, then translated using the googletrans library. 
The translated text is automatically spoken aloud using Google Text-to-Speech (gTTS) and playsound libraries,
creating a natural conversational experience.

User Experience:

The interface features a clean two-column layout displaying the conversation history with user's original text
and AI translations side-by-side. Each text segment includes copy-to-clipboard functionality for easy sharing. 
The app maintains conversation logs throughout the session and includes a clear chat button to reset conversations.

Technical Stack:

Built with Python 3.13, utilizing Streamlit for the web interface, googletrans for translation, speech_recognition for audio input, and gTTS for voice output. The application is fully functional and optimized for responsive, real-time translation experiences.
