import streamlit as st
import os
from TTS import text_to_speech_with_gtts
from STT import transcribe_audio
from audio_recorder import start_recording, stop_recording
from response import chat_with_bot

# Configuration
UPLOAD_FOLDER = "streamlit_uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# App title
st.title(" Job Interview System")

# File paths
recorded_audio_path = os.path.join(UPLOAD_FOLDER, "recorded_audio.wav")
tts_output_path = os.path.join(UPLOAD_FOLDER, "response_audio.mp3")

# Buttons for recording
if st.button("🎙 Start Speaking"):
    start_recording()
    st.info("Recording started... Speak now.")

if st.button(" Stop Speaking"):
    saved_path = stop_recording(recorded_audio_path)
    if saved_path and os.path.exists(saved_path):
        st.success(f" Recording saved: {saved_path}")
        st.audio(saved_path)

        # Transcribe audio
        try:
            text = transcribe_audio(saved_path)
            st.subheader(" User Input")
            st.write(text)

                        # Get response from bot
            response = chat_with_bot(text)
            st.subheader(" AI Response")
            st.write(response)

            # Convert to speech
            text_to_speech_with_gtts(response, tts_output_path)
            if os.path.exists(tts_output_path):
                st.audio(tts_output_path, format="audio/mp3")
            else:
                st.error(" Text-to-Speech failed to generate audio.")
        except Exception as e:
            st.error(f" Error during transcription or response: {e}")
    else:
        st.error("No recording found.")

