import os
import pyttsx3

from app.helpers.voice_helpers import configure_voice_engine, get_detected_voice, pre_process_text, process_saved_file


# def speak_arabic(text, rate=500):
#     engine = pyttsx3.init()

#     # List available voices and choose one supporting Arabic
#     arabic_voice = get_arabic_voice(engine)

#     # Set the Arabic voice
#     engine.setProperty('voice', arabic_voice)
#     engine.setProperty('rate', rate)  # Adjust speech speed

#     # Speak the Arabic text
#     engine.say(text)
#     engine.runAndWait()


def speak_arabic(text, audio_dir):

    engine = configure_voice_engine()
    # List available voices and choose one supporting Arabic
    arabic_voice = get_detected_voice(engine, "ar")
    print("arabic_voice", arabic_voice)
    print("arabic_voice", arabic_voice)
    # Set the Arabic voice
    engine.setProperty('voice', arabic_voice)

    output_file = os.path.join(audio_dir, "response_ar.wav")
    try:
        humanized_text = pre_process_text(text)

        print("text", text)
        print("humanized_text", humanized_text)

        engine.save_to_file(text, output_file)
        engine.runAndWait()
        return process_saved_file(output_file, "output_ar.wav")
    except Exception as error:
        if 'PatchedNSSpeechDriver' in str(error):
            engine.stop()
        return process_saved_file(output_file, "output_ar.wav")


