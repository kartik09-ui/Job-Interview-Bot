from dotenv import load_dotenv
load_dotenv()

import subprocess
import platform
import os
from gtts import gTTS


# def text_to_speech_with_gtts(input_text, output_filepath):
#     language="en"

#     audioobj= gTTS(
#         text=input_text,
#         lang=language,
#         slow=False
#     )
#     audioobj.save(output_filepath)
#     os_name = platform.system()
#     try:
#         if os_name == "Darwin":  # macOS
#             subprocess.run(['afplay', output_filepath])
#         elif os_name == "Windows":  # Windows
#             subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
#         elif os_name == "Linux":  # Linux
#             subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
#         else:
#             raise OSError("Unsupported operating system")
#     except Exception as e:
#         print(f"An error occurred while trying to play the audio: {e}")


# input_text="Hi this is Ai with Hg, autoplay testing!"
# text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing_autoplay.mp3")

from dotenv import load_dotenv
load_dotenv()

import subprocess
import platform
import os
from gtts import gTTS

def text_to_speech_with_gtts(input_text, output_filepath, play_audio=False):
    """
    Convert text to speech and optionally play it
    
    Args:
        input_text (str): Text to convert to speech
        output_filepath (str): Path to save the audio file
        play_audio (bool): Whether to play the audio after generation
    """
    language = "en"

    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)
    
    if play_audio:
        os_name = platform.system()
        try:
            if os_name == "Darwin":  # macOS
                subprocess.run(['afplay', output_filepath])
            elif os_name == "Windows":  # Windows
                # Use system default player instead of SoundPlayer
                os.startfile(output_filepath)  # This will use default media player
            elif os_name == "Linux":  # Linux
                subprocess.run(['aplay', output_filepath])
            else:
                print("Audio playback not supported on this OS")
        except Exception as e:
            print(f"Audio playback error: {e}")

    return output_filepath