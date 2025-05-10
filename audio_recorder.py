import sounddevice as sd
import soundfile as sf
import threading
import numpy as np

# Globals (for recording state and data)
recording = False
audio_data = []

def audio_callback(indata, frames, time, status):
    global audio_data
    if recording:
        audio_data.append(indata.copy())

def start_recording():
    """
    Starts audio recording in a background thread.
    """
    global recording, audio_data
    recording = True
    audio_data = []

    # Start background thread to record audio
    threading.Thread(target=_record).start()

def stop_recording(file_path="recorded_audio.wav"):
    """
    Stops the audio recording and saves the file.

    Args:
    - file_path (str): Path to save the recorded WAV file.

    Returns:
    - file_path (str): Path where audio is saved.
    """
    global recording
    recording = False

    if audio_data:
        full_data = np.concatenate(audio_data)
        sf.write(file_path, full_data, 44100)
        return file_path
    return None

def _record():
    with sd.InputStream(callback=audio_callback, channels=1, samplerate=44100):
        while recording:
            sd.sleep(100)


