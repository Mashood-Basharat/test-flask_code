import pyaudio
import wave

audio = pyaudio.PyAudio()
frames = []

try:
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    print("Audio record initiated...")

    while True:
        try:
            data = stream.read(1024, exception_on_overflow=False)
            frames.append(data)
        except OSError as e:
            print(f"Stream read error: {e}")
            break

except KeyboardInterrupt:
    print("Audio record terminated!")

finally:
    try:
        stream.stop_stream()
        stream.close()
    except Exception as e:
        print(f"Error closing stream: {e}")
    audio.terminate()

    # Save the recorded frames to a .wav file
    sound_file = wave.open("myrecording.wav", "wb")
    sound_file.setnchannels(1)
    sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    sound_file.setframerate(44100)
    sound_file.writeframes(b''.join(frames))
    sound_file.close()
    print("Audio saved as myrecording.wav.")
