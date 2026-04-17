import streamlit as st
from deep_translator import GoogleTranslator
import speech_recognition as sr
from gtts import gTTS
import tempfile
import os
import pyperclip

# Page config
st.set_page_config(page_title="Speech Translator", layout="wide")

st.title("🗣️ Real-Time Speech Translator")
st.markdown("---")

# Sidebar
language_options = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh-cn",
    "Tamil": "ta",
    "Telugu": "te",
    "Malayalam": "ml",
    "Kannada": "kn",
    "Thai": "th"
}

with st.sidebar:
    st.header("⚙️ Settings")

    original_lang = st.selectbox("📍 Speak In:", list(language_options.keys()))
    translated_lang = st.selectbox("🎯 Translate To:", list(language_options.keys()), index=1)

original_lang_code = language_options[original_lang]
translated_lang_code = language_options[translated_lang]

if original_lang_code == translated_lang_code:
    st.error("❌ Select different languages!")

# Session state
if "history" not in st.session_state:
    st.session_state.history = []

# Recognizer
recognizer = sr.Recognizer()

# 🎤 AUDIO INPUT (Streamlit Cloud compatible)
audio_file = st.audio_input("🎙️ Click and record your speech")

if audio_file:
    try:
        st.info("Processing audio...")

        # Save temp audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_file.read())
            audio_path = tmp.name

        # Convert speech → text
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            spoken_text = recognizer.recognize_google(
                audio_data,
                language=original_lang_code
            )

        os.remove(audio_path)

        # Translate
        translated_text = GoogleTranslator(
            source='auto',
            target=translated_lang_code
        ).translate(spoken_text)

        # Save history
        st.session_state.history.append((spoken_text, translated_text))

        # Display
        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"🎤 {original_lang}")
            st.code(spoken_text)

        with col2:
            st.subheader(f"🌐 {translated_lang}")
            st.code(translated_text)

        # 🔊 Text-to-Speech (Cloud-safe)
        tts = gTTS(translated_text, lang=translated_lang_code)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
            tts.save(tmp_audio.name)
            st.audio(tmp_audio.read(), format="audio/mp3")

        os.remove(tmp_audio.name)

        st.success("✅ Translation Complete!")

    except sr.UnknownValueError:
        st.warning("⚠️ Could not understand audio")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# Conversation History
if st.session_state.history:
    st.markdown("## 💬 Conversation History")

    for i, (orig, trans) in enumerate(st.session_state.history):
        col1, col2 = st.columns(2)

        with col1:
            st.code(orig)
            if st.button("📋 Copy", key=f"o{i}"):
                pyperclip.copy(orig)

        with col2:
            st.code(trans)
            if st.button("📋 Copy", key=f"t{i}"):
                pyperclip.copy(trans)
