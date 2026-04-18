# 🗣️ Real-Time Voice Conversation Translator

A Streamlit-based web application that enables **real-time speech-to-speech translation** between two languages.
The app captures voice input, converts it to text, translates it, and **speaks out the translated result automatically**.

---

## 🚀 Features

* 🎤 **Voice Input** using microphone
* 🌐 **Real-time Translation** using `deep-translator`
* 🔊 **Text-to-Speech Output** using `gTTS`
* 🔁 **Two-way Conversation Mode** (auto-switch between speakers)
* 💬 **Conversation History**
* 🧹 **Clear Chat Option**
* ⚡ **Responsive UI (Streamlit)**

---

## 🧠 How It Works

1. User clicks **"Speak Now"**
2. App records voice using microphone
3. Speech is converted to text
4. Text is translated to target language
5. Translated text is:

   * Displayed on screen
   * 🔊 **Spoken automatically**
6. Conversation alternates between selected languages

---

## 🛠️ Tech Stack

* **Frontend/UI:** Streamlit
* **Speech Recognition:** SpeechRecognition
* **Translation:** deep-translator
* **Text-to-Speech:** gTTS
* **Language Processing:** Google Speech API

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/speech-translator.git
cd speech-translator
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Run the application

```bash
streamlit run app.py
```

---

## 📄 requirements.txt

```txt
streamlit
deep-translator
SpeechRecognition
gTTS
pyaudio
```

---

## ⚙️ Usage

1. Select:

   * **Input Language**
   * **Target Language**
2. Click **🎙️ Speak Now**
3. Speak into your microphone
4. View translation and hear output instantly
5. Click **🔊 Play Last Translation** if audio does not autoplay

---

## ⚠️ Limitations

* 🔒 Browsers may **block repeated automatic audio playback**
* 🎧 Requires microphone access
* 🌐 Requires internet connection (for translation & speech API)

---

## 💡 Future Improvements

* 🎤 Continuous listening mode (no button)
* 💬 Chat-style interface
* 🌍 More language support
* 📱 Mobile optimization
* 🔊 Offline speech support

---

## 👩‍💻 Author

**Vanshika Kayeetha**

---

## 📜 License

This project is for educational purposes.

---

## ⭐ Acknowledgements

* Google Speech Recognition API
* deep-translator
* Streamlit
* gTTS

---

## 🎯 Project Objective

To demonstrate the integration of:

* Speech Recognition
* Natural Language Processing
* Real-time Translation
* Speech Synthesis

into a single interactive application.

---
