import os

from app.lib.voice.audio_to_text import transcribe_audio
from app.lib.voice.record_user_audio import record_audio
from app.lib.voice.speak_default import speak_english

def voice_to_voice_pipeline():
    # Step 1: Record Audio
    input_audio = "input.wav"
    input_audio = record_audio(input_audio)
    
    # Step 2: Speech-to-Text
    user_text = transcribe_audio(input_audio)
    print("User:", user_text)
    
    # Step 3: Get ChatGPT Response
    ai_response =  user_text #"I am happy to share, that i am starting a new position at almatar which is one of the leading startups" #get_chat_response(user_text)
    print("AI:", ai_response)
    
    # Step 4: Text-to-Speech
    print("AI is speaking...")
    speak_english(ai_response)


def text_to_voice(ai_response):    
    # Text-to-Speech
    print("AI is speaking...")
    speak_english(ai_response)
