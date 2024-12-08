import numpy as np
import librosa
import matplotlib.pyplot as plt

# Define a chunk size (in samples), e.g., 10 seconds of audio
chunk_duration = 10  # seconds
chunk_size = 22050 * chunk_duration  # Assuming 22.05 kHz sample rate

# Initialize arrays for mean power
mean_power_over_time = []

# Load the audio file in chunks
file_path = '../recordSDR/20241208_000100_sound.wav'

# Use librosa.stream to process in chunks (stream-based processing)
stream = librosa.stream(file_path, block_length=chunk_duration, frame_length=2048, hop_length=512)

for y in stream:
    # Compute STFT on the chunk
    D = librosa.stft(y, n_fft=2048, hop_length=512)
    power_spectrogram = np.abs(D)**2

    # Calculate mean power across frequency bins for this chunk
    mean_power = np.mean(power_spectrogram, axis=0)
    mean_power_over_time.extend(mean_power)

# Plot the mean power over time
plt.plot(mean_power_over_time)
plt.xlabel('Time Frame')
plt.ylabel('Mean Power')
plt.title('Mean Power Spectrum (Streamed Processing)')
plt.show()
