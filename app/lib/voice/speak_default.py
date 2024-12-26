import os
from fastapi.responses import FileResponse
from app.helpers.voice_helpers import configure_voice_engine, get_detected_voice, pre_process_text, process_saved_file
from main import root_path

def speak_english(text, audio_dir):
    engine=None
    engine = configure_voice_engine()

    # List available voices and choose one supporting Arabic
    detected_voice = get_detected_voice(engine, "en")
    print("detected_voice", detected_voice)
    
    # Set the detected voice, expected voice is english
    # engine.setProperty('voice', detected_voice)
    
    output_file = os.path.join(audio_dir, "response_en.wav")
    try:
        humanized_text = pre_process_text(text)
        print("humanized_text", humanized_text)
        engine.save_to_file(humanized_text, output_file)
        # engine.stop()  # Stop any current speech tasks
        engine.runAndWait()
        return process_saved_file(output_file, "output_en.wav")
    except Exception as error:
        if 'PatchedNSSpeechDriver' in str(error):
            engine.stop()
            print("Voice Engine have been stopped")
        return process_saved_file(output_file, "output_en.wav")


