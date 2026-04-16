from googletrans import Translator
import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os
import pyperclip

translator = Translator()

# Page configuration
st.set_page_config(page_title="Speech Translator", layout="wide", initial_sidebar_state="expanded")

# Main title
st.markdown("# 🗣️ Real-Time Speech Translator")
st.markdown("---")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Settings")
    
    language_options = {
        "English": "en",
        "Thai": "th",
        "Spanish": "es",
        "French": "fr",
        "German": "de",
        "Japanese": "ja",
        "Korean": "ko",
        "Chinese": "zh-cn",
        "Hindi": "hi",
        "Portuguese": "pt",
        "Telugu": "te",
        "Malayalam": "ml",
        "Tamil": "ta",
        "Kannada": "kn"
    }
    
    # Reverse language mapping for code to name
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
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'conversation_log' not in st.session_state:
    st.session_state.conversation_log = []
if 'current_lang_index' not in st.session_state:
    st.session_state.current_lang_index = 0

# Function to speak with selected voice (used in both modes)
def speak_translation(text, target_lang):
    try:
        tts = gTTS(text=text, lang=target_lang, slow=False)
        tts.save("translation.mp3")
        playsound("translation.mp3")
        
        if os.path.exists("translation.mp3"):
            os.remove("translation.mp3")
    except Exception as e:
        st.error(f"Error playing audio: {e}")

# Control buttons
col1, col2 = st.columns([2, 1])

with col1:
    if st.session_state.is_running:
        record_btn = st.button("🎙️ RECORDING... (Click to Stop)", key="record", use_container_width=True)
        if not record_btn:
            st.session_state.is_running = False
            st.rerun()
    else:
        record_btn = st.button("🎙️ HOLD TO SPEAK", key="record", use_container_width=True)
        if record_btn:
            st.session_state.is_running = True

with col2:
    clear_btn = st.button("🗑️ Clear", key="clear", use_container_width=True)
    if clear_btn:
        st.session_state.conversation_log = []
        st.session_state.current_lang_index = 0
        st.rerun()

st.markdown("---")

# Main recording area
if st.session_state.is_running:
    # Determine which language to speak
    speaks_original = (st.session_state.current_lang_index == 0)
    current_speak_lang = original_lang if speaks_original else translated_lang
    listen_lang_code = original_lang_code if speaks_original else translated_lang_code
    reply_lang = translated_lang if speaks_original else original_lang
    reply_lang_code = translated_lang_code if speaks_original else original_lang_code
    
    # Display instructions
    st.markdown(f"### 🎤 Speak in: **{current_speak_lang}**")
    st.info(f"📢 You are speaking in {current_speak_lang}. Your message will be translated to {reply_lang}.")
    
    recognizer = sr.Recognizer()
    # Robust noise handling settings
    recognizer.energy_threshold = 1000  
    recognizer.dynamic_energy_threshold = True
    
    try:
        with sr.Microphone() as source:
            # Adjust for background noise
            st.markdown("### Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            st.markdown("### 🎤 Listening... (Waiting up to 15 seconds)")
            st.write("Speak naturally. Works even with background disturbances!")
            
            # Listen for up to 15 seconds with phrase time limit
            audio = recognizer.listen(source, timeout=15, phrase_time_limit=12)
            
            st.markdown("### Processing...")
            spoken_text = recognizer.recognize_google(audio, language=listen_lang_code)
            
            # Translate to target language
            result = translator.translate(spoken_text, dest=reply_lang_code)
            translated = result.text
            
            # Add to conversation log
            st.session_state.conversation_log.append({
                "original": spoken_text,
                "translated": translated,
                "original_lang": current_speak_lang,
                "translated_lang": reply_lang,
                "source": "Microphone"
            })
            
            # Display results
            st.markdown(f"### 🎤 You Said ({current_speak_lang}):")
            st.write(spoken_text)
            
            # Speak translation
            st.markdown(f"### 🔊 Speaking in {reply_lang}...")
            speak_translation(translated, reply_lang_code)
            
            st.markdown(f"### 🌐 Translation ({reply_lang}):")
            st.write(translated)
            
            st.success(f"✅ Translated!")
            
            # Toggle language for next turn
            st.session_state.current_lang_index = 1 - st.session_state.current_lang_index
            st.session_state.is_running = False
            st.rerun()
            
    except sr.UnknownValueError:
        st.warning("⚠️ Could not understand. Please try again.")
        st.session_state.is_running = False
        st.rerun()
    except sr.RequestError as e:
        st.error(f"❌ Microphone error")
        st.session_state.is_running = False
        st.rerun()
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.session_state.is_running = False
        st.rerun()

elif not st.session_state.is_running and len(st.session_state.conversation_log) == 0:
    st.info("👆 Click **HOLD TO SPEAK** to begin!")

# Display conversation
if st.session_state.conversation_log:
    st.markdown("## 💬 Conversation")
    st.markdown("---")
    
    for i, entry in enumerate(st.session_state.conversation_log, 1):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**{entry['original_lang']}**")
            st.markdown(f"```\n{entry['original']}\n```")
            copy_col1, copy_col2 = st.columns([3, 1])
            with copy_col2:
                if st.button("📋 Copy", key=f"copy_orig_{i}", use_container_width=True):
                    pyperclip.copy(entry['original'])
                    st.success("✅ Copied!")
        
        with col2:
            st.markdown(f"**{entry['translated_lang']}**")
            st.markdown(f"```\n{entry['translated']}\n```")
            copy_col1, copy_col2 = st.columns([3, 1])
            with copy_col2:
                if st.button("📋 Copy", key=f"copy_trans_{i}", use_container_width=True):
                    pyperclip.copy(entry['translated'])
                    st.success("✅ Copied!")
        
        st.markdown("---")