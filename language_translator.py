import streamlit as st
from deep_translator import GoogleTranslator
import speech_recognition as sr
from gtts import gTTS
import tempfile
import base64
import uuid

# Page setup
st.set_page_config(page_title="Speech Translator", layout="wide")

st.title("🗣️ Real-Time Speech Translator")
st.markdown("---")

# 🌍 Languages
language_options = {
    "English": "en",
    "Thai": "th",
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
    "Kannada": "kn"
}

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    lang1 = st.selectbox("Speak In", list(language_options.keys()), index=0)
    lang2 = st.selectbox("Translate To", list(language_options.keys()), index=1)

lang1_code = language_options[lang1]
lang2_code = language_options[lang2]

# Session state
if "turn" not in st.session_state:
    st.session_state.turn = 0

if "history" not in st.session_state:
    st.session_state.history = []

if "last_audio" not in st.session_state:
    st.session_state.last_audio = None
    
# Speech recognizer
recognizer = sr.Recognizer()

# 🔊 Auto speak function (best working method)
def speak(text, lang):
    try:
        tts = gTTS(text=text, lang=lang)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tts.save(tmp.name)

            with open(tmp.name, "rb") as f:
                audio_bytes = f.read()

        # ✅ store audio persistently
        st.session_state.last_audio = audio_bytes

        # 🔊 try autoplay
        b64 = base64.b64encode(audio_bytes).decode()

        st.markdown(f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Audio error: {e}")
        
# Layout
col1, col2 = st.columns([3, 1])

with col1:
    if st.session_state.turn == 0:
        st.info(f"🎤 {lang1} Speaker - Click to Speak")
    else:
        st.info(f"🎤 {lang2} Speaker - Click to Speak")

with col2:
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.history = []
        st.session_state.turn = 0

# 🎙️ Record button
record = st.button("🎙️ Speak Now", use_container_width=True)

# 🎤 Main logic
if record:
    try:
        with sr.Microphone() as source:
            st.warning("Listening... Speak now")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=8)

        # Speaker logic
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

        # 🌐 Translation (FIXED)
        translated = GoogleTranslator(
            source=input_lang,
            target=output_lang
        ).translate(text)

        # Display
        st.success(f"{speaker}: {text}")
        st.info(f"{listener}: {translated}")

        # 🔊 Speak translation
        speak(translated, output_lang)

        # Save history
        st.session_state.history.append((speaker, text, listener, translated))

        # Switch turn
        st.session_state.turn = 1 - st.session_state.turn

    except sr.UnknownValueError:
        st.error("⚠️ Could not understand audio")
    except Exception as e:
        st.error(f"❌ Error: {e}")
        
# 🔊 Always available fallback player
# 🔊 Play last translation automatically (no player UI)
if st.session_state.last_audio:
    if st.button("🔊 Play Last Translation"):

        b64 = base64.b64encode(st.session_state.last_audio).decode()

        st.markdown(f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
        """, unsafe_allow_html=True)
        
# 💬 Conversation
if st.session_state.history:
    st.markdown("## 💬 Conversation")

    for s, t, l, tr in st.session_state.history:
        st.markdown(f"**{s}:** {t}")
        st.markdown(f"**{l}:** {tr}")
        st.markdown("---")
