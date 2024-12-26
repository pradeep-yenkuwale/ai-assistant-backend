import os
import time
from langdetect import detect
from fastapi.responses import FileResponse
import ffmpeg
import pyttsx3
from main import root_path
import time
import re
import ffmpeg

TEMP_AUDIO_DIR = root_path + "/temp_audio"

def configure_voice_engine(rate=150):
    engine = pyttsx3.init(driverName="nsss")  
    # Set properties for the voice
    engine.setProperty('rate', rate)  # Default is around 200; lower value slows down
    engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
    return engine


def process_saved_file(output_file, compare_file):
    # Wait for the file to exist and be complete
    while not os.path.exists(output_file):
        time.sleep(0.1)

    # Optional: Verify file size stabilizes to confirm it's fully written
    previous_size = -1
    while previous_size != os.path.getsize(output_file):
        previous_size = os.path.getsize(output_file)
        time.sleep(0.1)

    ffmpeg.input(output_file).output(TEMP_AUDIO_DIR + '/' + compare_file, acodec='pcm_s16le').overwrite_output().run()
    return FileResponse(output_file, media_type="audio/wav", filename=compare_file)


def pre_process_text(text):
    # Remove numeric notations like "1.", "2.", etc.
    text = re.sub(r'\d+\.', '', text)
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove special characters like colons, semicolons, commas, and extra spaces
    text = re.sub(r'[;:]', '', text)  # Remove semicolons and colons
    text = re.sub(r',', '', text)    # Remove commas
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)


    sentences = text.split('.')
    humanized_text = '. '.join(sentence.strip().capitalize() for sentence in sentences if sentence.strip())
    return humanized_text


def detect_language(text):
    detected_language = detect(text)  # Returns language code, e.g., 'fr' for French
    print("Detected Lanuguage => ", detected_language)
    if detected_language not in ['ar', 'en']:
        print("Could not detect the lanugage from input, setting default labuguage to => en")
        detected_language = 'en'
    print("Final Detected Lanuguage =>", detected_language)
    return detected_language

def get_detected_voice(engine, language):
    voices = engine.getProperty('voices')
    detected_voice = None
    ARABIC = os.getenv("ARABIC_VOICE") or "mariam (enhanced)"
    ENGLISH = os.getenv("ENGLISH_VOICE") or "samantha (enhanced)"
    DEFAULT = os.getenv("DEFAULT")
    print("Configured for Arabic", ARABIC)
    print("Configured for English", ENGLISH)

    for voice in voices:
        print("voice.languages", voice.languages)
        if 'en_GB' in voice.languages:
            print(f"ID: {voice.id}, Name: {voice.name}, Language: {voice.languages}")

    for voice in voices:
        # print("language", language, language == 'ar' and 'ar_001' in voice.languages and voice.name.lower() == ARABIC.lower())
        if(language == 'ar' and 'ar_001' in voice.languages and voice.name.lower() == ARABIC.lower()):
            print(f"Selected Voice => ID: {voice.id}, Name: {voice.name}, Language: {voice.languages}")
            detected_voice = voice.id
            break
        elif(language == 'en' and 'en_US' in voice.languages and voice.name.lower() == ENGLISH.lower()):
            print(f"Selected Voice => ID: {voice.id}, Name: {voice.name}, Language: {voice.languages}")
            detected_voice = voice.id
            break
        # else:
        #     detected_voice = "com.apple.voice.compact.en-US.Samantha"
        #     break
    print("detected_voice", detected_voice)
    return detected_voice
