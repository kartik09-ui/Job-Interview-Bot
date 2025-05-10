import streamlit as st
import os
from TTS import text_to_speech_with_gtts
from STT import record_audio, transcribe_audio
from audio_recorder import start_recording, stop_recording
# from model_processing import ChatManager
from response import chat_with_bot

# Configuration
UPLOAD_FOLDER = "streamlit_uploads"
ALLOWED_EXTENSIONS = {"mp3", "wav"}


os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# def speech_to_text_record():
#     file=os.path.join(UPLOAD_FOLDER,'record.mp3')
#     record_audio(file)


# chat_mgr = ChatManager(storage_path="chat_history.json")

# def generate_response(text):
#     response=chat_mgr.get_llm_response(text)
#     return response


# Title of the app
st.title("JOB INTERVIEW SYSTEM")


# if st.button("Start Interview"):

audio_path = os.path.join(UPLOAD_FOLDER, 'record.mp3')
if st.button("Start Recording"):
    start_recording()
    st.info("Recording started...")

if st.button("Stop Recording"):
    audio_path = stop_recording("my_audio.wav")
    if audio_path:
        st.success(f"Recording saved at: {audio_path}")
        st.audio(audio_path)
    else:
        st.error("No audio data recorded.")


text=transcribe_audio(audio_path)
st.write(text)

response=chat_with_bot(text)
st.write(response)
file=os.path.join(UPLOAD_FOLDER,'audio.mp3')
st.write(text_to_speech_with_gtts(response,file))
with open(file, "rb") as f:
    st.audio(f.read(), format="audio/mp3")


