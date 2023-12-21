import pyaudio
import numpy as np

# Dictionary of note frequencies (in Hz)
note_frequencies = {
    'A0': 27.50, 'A#0/Bb0': 29.14, 'B0': 30.87,
    'C1': 32.70, 'C#1/Db1': 34.65, 'D1': 36.71, 'D#1/Eb1': 38.89, 'E1': 41.20, 'F1': 43.65, 'F#1/Gb1': 46.25,
    'G1': 49.00, 'G#1/Ab1': 51.91, 'A1': 55.00, 'A#1/Bb1': 58.27, 'B1': 61.74,
    'C2': 65.41, 'C#2/Db2': 69.30, 'D2': 73.42, 'D#2/Eb2': 77.78, 'E2': 82.41, 'F2': 87.31, 'F#2/Gb2': 92.50,
    'G2': 98.00, 'G#2/Ab2': 103.83, 'A2': 110.00, 'A#2/Bb2': 116.54, 'B2': 123.47,
    'C3': 130.81, 'C#3/Db3': 138.59, 'D3': 146.83, 'D#3/Eb3': 155.56, 'E3': 164.81, 'F3': 174.61, 'F#3/Gb3': 185.00,
    'G3': 196.00, 'G#3/Ab3': 207.65, 'A3': 220.00, 'A#3/Bb3': 233.08, 'B3': 246.94,
    'C4': 261.63, 'C#4/Db4': 277.18, 'D4': 293.66, 'D#4/Eb4': 311.13, 'F4': 329.63, 'E4': 349.23, 'F#4/Gb4': 369.99,
    'G4': 392.00, 'G#4/Ab4': 415.30, 'A4': 440.00, 'A#4/Bb4': 466.16, 'B4': 493.88,
    'C5': 523.25, 'C#5/Db5': 554.37, 'D5': 587.33, 'D#5/Eb5': 622.25, 'F5': 659.25, 'E5': 698.46, 'F#5/Gb5': 739.99,
    'G5': 783.99, 'G#5/Ab5': 830.61, 'A5': 880.00, 'A#5/Bb5': 932.33, 'B5': 987.77,
    'C6': 1046.50, 'C#6/Db6': 1108.73, 'D6': 1174.66, 'D#6/Eb6': 1244.51, 'E6': 1318.51, 'F6': 1396.91,
    'F#6/Gb6': 1479.98, 'G6': 1567.98, 'G#6/Ab6': 1661.22, 'A6': 1760.00, 'A#6/Bb6': 1864.66, 'B6': 1975.53,
    'C7': 2093.00, 'C#7/Db7': 2217.46, 'D7': 2349.32, 'D#7/Eb7': 2489.02, 'E7': 2637.02, 'F7': 2793.83,
    'F#7/Gb7': 2959.96, 'G7': 3135.96, 'G#7/Ab7': 3322.44, 'A7': 3520.00, 'A#7/Bb7': 3729.31, 'B7': 3951.07,
    'C8': 4186.01
}


def get_dominant_pitch(samples, rate):
    # Use a simple pitch detection algorithm
    fft_result = np.fft.fft(samples)
    freqs = np.fft.fftfreq(len(fft_result), 1.0 / rate)
    magnitude = np.abs(fft_result)

    # Get the index of the maximum magnitude
    max_index = np.argmax(magnitude)

    # Calculate the corresponding frequency
    pitch = np.abs(freqs[max_index])

    return pitch


def match_pitch_to_note(detected_pitch):
    # Find the closest note in the dictionary
    closest_note = min(note_frequencies, key=lambda x: abs(note_frequencies[x] - detected_pitch))
    frequency_diff = abs(note_frequencies[closest_note] - detected_pitch)

    return closest_note, frequency_diff


def detect_pitch(note_0):
    # Set up PyAudio
    p = pyaudio.PyAudio()

    # Set the parameters for the audio stream
    CHUNK = 512
    FORMAT = pyaudio.paFloat32
    CHANNELS = 1
    RATE = 44100

    # Open the audio stream
    stream = p.open(format=FORMAT,
                    rate=RATE,
                    channels=CHANNELS,
                    input_device_index=1,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Listening for notes...")

    # i = 0
    count = 0
    while True:
        # Read audio data
        data = stream.read(CHUNK)
        samples = np.frombuffer(data, dtype=np.float32)

        # Get the frequency of the dominant pitch
        pitch = get_dominant_pitch(samples, RATE)

        # Match the detected pitch to the closest note
        note, frequency_diff = match_pitch_to_note(pitch)

        # if i == 0:
        #     note_0 = note
        #     i += 1

        if note_0 == note:
            count += 1
            note_0 = note

        if count >= 5:
            stream.stop_stream()
            stream.close()
            p.terminate()
            return True

        # Print the detected note and frequency difference
        print(f"Detected note: {note} (Frequency diff: {frequency_diff:.2f} Hz)")




    # finally:
    #     # Close the audio stream
    #     stream.stop_stream()
    #     stream.close()
    #     p.terminate()
    #
    # if note is not None:
    #     return note


# if __name__ == "__main__":
#     detect_pitch()

