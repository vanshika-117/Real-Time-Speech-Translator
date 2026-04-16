import streamlit as st
from deep_translator import GoogleTranslator
import speech_recognition as sr
from gtts import gTTS
import pyperclip
import tempfile
import os

# Page configuration
st.set_page_config(
    page_title="Speech Translator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.markdown("# 🗣️ Real-Time Speech Translator")
st.markdown("---")

# Initialize recognizer
recognizer = sr.Recognizer()

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Settings")

    language_options = {
        "English": "en",
        "Hindi": "hi",
        "Spanish": "es",
        "French": "fr",
        "German": "de",
        "Japanese": "ja",
        "Korean": "ko",
        "Chinese": "zh-cn",
        "Portuguese": "pt",
        "Tamil": "ta",
        "Telugu": "te",
        "Malayalam": "ml",
        "Kannada": "kn",
        "Thai": "th"
    }

    lang_code_to_name = {v: k for k, v in language_options.items()}

    original_lang = st.selectbox(
        "📍 Speak In:",
        list(language_options.keys()),
        index=0
    )
    original_lang_code = language_options[original_lang]

    translated_lang = st.selectbox(
        "🎯 Translate To:",
        list(language_options.keys()),
        index=1
    )
    translated_lang_code = language_options[translated_lang]

    if original_lang_code == translated_lang_code:
        st.error("❌ Select different languages!")

# Initialize session state
if "conversation_log" not in st.session_state:
    st.session_state.conversation_log = []

# Function: Speak Translation
def speak_translation(text, target_lang):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tts = gTTS(text=text, lang=target_lang)
            tts.save(tmp_file.name)
            audio_path = tmp_file.name

        # Play audio in Streamlit
        with open(audio_path, "rb") as audio_file:
            st.audio(audio_file.read(), format="audio/mp3")

        os.remove(audio_path)

    except Exception as e:
        st.error(f"Error playing audio: {e}")

# Function: Translate Text
def translate_text(text, source_lang, target_lang):
    try:
        translator = GoogleTranslator(
            source=source_lang,
            target=target_lang
        )
        return translator.translate(text)
    except Exception as e:
        st.error(f"Translation Error: {e}")
        return None

# Control buttons
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🎙️ Record Your Voice")
with col2:
    if st.button("🗑️ Clear"):
        st.session_state.conversation_log = []
        st.rerun()

st.markdown("---")

# Audio Input using Streamlit
audio_file = st.audio_input("Click to record your speech")

if audio_file is not None:
    try:
        st.info("🔄 Processing audio...")

        # Save audio temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_file.read())
            audio_path = tmp.name

        # Convert speech to text
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            spoken_text = recognizer.recognize_google(
                audio_data,
                language=original_lang_code
            )

        os.remove(audio_path)

        # Translate text
        translated_text = translate_text(
            spoken_text,
            original_lang_code,
            translated_lang_code
        )

        if translated_text:
            # Store in conversation log
            st.session_state.conversation_log.append({
                "original": spoken_text,
                "translated": translated_text,
                "original_lang": original_lang,
                "translated_lang": translated_lang
            })

            # Display results
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"### 🎤 You Said ({original_lang})")
                st.code(spoken_text)

            with col2:
                st.markdown(f"### 🌐 Translation ({translated_lang})")
                st.code(translated_text)

            # Play translated speech
            st.markdown(f"### 🔊 Pronunciation ({translated_lang})")
            speak_translation(translated_text, translated_lang_code)

            st.success("✅ Translation Complete!")

    except sr.UnknownValueError:
        st.warning("⚠️ Could not understand the audio.")
    except sr.RequestError:
        st.error("❌ Speech recognition service is unavailable.")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# Display conversation history
if st.session_state.conversation_log:
    st.markdown("## 💬 Conversation History")
    st.markdown("---")

    for i, entry in enumerate(st.session_state.conversation_log, 1):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**{entry['original_lang']}**")
            st.code(entry["original"])
            if st.button("📋 Copy", key=f"copy_orig_{i}"):
                pyperclip.copy(entry["original"])
                st.success("Copied!")

        with col2:
            st.markdown(f"**{entry['translated_lang']}**")
            st.code(entry["translated"])
            if st.button("📋 Copy", key=f"copy_trans_{i}"):
                pyperclip.copy(entry["translated"])
                st.success("Copied!")