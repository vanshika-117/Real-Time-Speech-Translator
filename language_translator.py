import streamlit as st
from deep_translator import GoogleTranslator
import speech_recognition as sr
from gtts import gTTS
import tempfile
import os

# Page config
st.set_page_config(page_title="Speech Translator", layout="wide")

st.title("🗣️ Real-Time Voice Conversation Translator")
st.markdown("---")

# 🌍 Languages
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

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    lang1 = st.selectbox("Speak", list(language_options.keys()), index=0)
    lang2 = st.selectbox("Translate to", list(language_options.keys()), index=1)

lang1_code = language_options[lang1]
lang2_code = language_options[lang2]

# Session state
if "turn" not in st.session_state:
    st.session_state.turn = 0

if "history" not in st.session_state:
    st.session_state.history = []


# 🔊 Reliable audio playback (NO autoplay hack)
def speak(text, lang):
    tts = gTTS(text=text, lang=lang, slow=False)

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tmp_path = tmp_file.name
    tmp_file.close()

    tts.save(tmp_path)

    # Streamlit audio player (reliable every time)
    audio_file = open(tmp_path, "rb")
    audio_bytes = audio_file.read()
    audio_file.close()

    os.remove(tmp_path)

    st.audio(audio_bytes, format="audio/mp3")

# Layout
col1, col2 = st.columns([3, 1])

with col1:
    if st.session_state.turn == 0:
        st.info(f"🎤 {lang1} Speaker : Speak Now")
    else:
        st.info(f"🎤 {lang2} Speaker")

with col2:
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.history = []
        st.session_state.turn = 0

# 🎙️ Record button
record = st.button("🎙️ Speak Now", use_container_width=True)

# 🎤 Main Logic
if record:
    try:
        with sr.Microphone() as source:
            st.warning("Listening... Speak now")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=8)

        # Turn logic
        if st.session_state.turn == 0:
            input_lang = lang1_code
            output_lang = lang2_code
            speaker = lang1
            listener = lang2
        else:
            input_lang = lang2_code
            output_lang = lang1_code
            speaker = lang2
            listener = lang1

        # Speech → Text
        text = recognizer.recognize_google(audio, language=input_lang)

        # Translate
        translated = GoogleTranslator(
            source=input_lang,
            target=output_lang
        ).translate(text)

        # Show text
        st.success(f"{speaker}: {text}")
        st.info(f"{listener}: {translated}")

        # 🔊 Play audio EVERY TIME (fixed)
        speak(translated, output_lang)

        # Save history
        st.session_state.history.append((speaker, text, listener, translated))

        # Switch turn
        st.session_state.turn = 1 - st.session_state.turn

    except sr.UnknownValueError:
        st.error("⚠️ Could not understand audio")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# 💬 History
if st.session_state.history:
    st.markdown("## 💬 Conversation")
    for s, t, l, tr in st.session_state.history:
        st.markdown(f"**{s}:** {t}")
        st.markdown(f"**{l}:** {tr}")
        st.markdown("---")
