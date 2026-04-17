import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile
import os
import io
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder

# Page config
st.set_page_config(page_title="Speech Translator", layout="wide")

st.title("🗣️ Real-Time Voice Conversation Translator")
st.markdown("---")

st.info("🎙️ Click record → speak → stop → translation + audio will appear")

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
    lang1 = st.selectbox("Speaker 1", list(language_options.keys()), index=0)
    lang2 = st.selectbox("Speaker 2", list(language_options.keys()), index=1)

lang1_code = language_options[lang1]
lang2_code = language_options[lang2]

# Session state
if "turn" not in st.session_state:
    st.session_state.turn = 0

if "history" not in st.session_state:
    st.session_state.history = []

# 🔊 Audio playback (reliable)
def speak(text, lang):
    tts = gTTS(text=text, lang=lang, slow=False)

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tmp_path = tmp_file.name
    tmp_file.close()

    tts.save(tmp_path)

    with open(tmp_path, "rb") as f:
        audio_bytes = f.read()

    os.remove(tmp_path)

    st.audio(audio_bytes, format="audio/mp3")

# Layout
col1, col2 = st.columns([3, 1])

with col1:
    if st.session_state.turn == 0:
        st.info(f"🎤 {lang1} - Speak now")
    else:
        st.info(f"🎤 {lang2} - Speak now")

with col2:
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.history = []
        st.session_state.turn = 0

# 🎙️ Mic Recorder (browser-based)
audio_data = mic_recorder(
    start_prompt="🎙️ Start Recording",
    stop_prompt="⏹️ Stop Recording",
    use_container_width=True
)

# 🎤 Process Audio
if audio_data:
    try:
        recognizer = sr.Recognizer()

        audio_bytes = audio_data["bytes"]
        audio_file = io.BytesIO(audio_bytes)

        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)

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

        # Display
        st.success(f"{speaker}: {text}")
        st.info(f"{listener}: {translated}")

        # 🔊 Play translated voice
        speak(translated, output_lang)

        # Save history
        st.session_state.history.append((speaker, text, listener, translated))

        # Switch turn
        st.session_state.turn = 1 - st.session_state.turn

    except sr.UnknownValueError:
        st.error("⚠️ Could not understand audio")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# 💬 Conversation History
if st.session_state.history:
    st.markdown("## 💬 Conversation")

    for s, t, l, tr in st.session_state.history:
        st.markdown(f"**{s}:** {t}")
        st.markdown(f"**{l}:** {tr}")
        st.markdown("---")
