import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
# import sounddevice as sd
# import numpy as np
import wave
import time

# def record_audio(output_file, duration=5, samplerate=16000):
#     print("Recording...")
#     sd.default.device = 0
#     audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
#     sd.wait()  # Wait until recording is finished
#     wav.write(output_file, samplerate, np.array(audio))
#     return output_file




def record_audio(filename, samplerate=16000, silence_threshold=500, chunk_duration=0.5):
    print("Recording... Speak into the microphone.")
    # Initialize variables
    audio = []
    silence_start = None
    
    # Create a stream
    with sd.InputStream(samplerate=samplerate, channels=1, dtype='int16') as stream:
        while True:
            # Read audio chunks
            data, _ = stream.read(int(chunk_duration * samplerate))
            audio.append(data)

            # Check if the audio contains significant sound
            max_amplitude = np.max(np.abs(data))
            if max_amplitude < silence_threshold:
                if silence_start is None:
                    silence_start = time.time()
                elif time.time() - silence_start > 2:  # Stop after 2 seconds of silence
                    break
            else:
                silence_start = None  # Reset if sound is detected
    
    print("Recording complete.")
    # Save the audio to a file
    audio = np.concatenate(audio, axis=0)
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit audio
        wf.setframerate(samplerate)
        wf.writeframes(audio.tobytes())
    
    print(f"Audio saved to {filename}")
    return filename
