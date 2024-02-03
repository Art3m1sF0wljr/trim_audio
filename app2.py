import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

# Load the audio file
y, sr = librosa.load('sound.wav')

# Calculate the short-time Fourier transform (STFT)
D = librosa.stft(y)

# Compute the power spectrogram
power_spectrogram = np.abs(D)**2

# Calculate the mean power across frequency bins for each time frame
mean_power = np.mean(power_spectrogram, axis=0)

# Plot the mean power over time
plt.plot(mean_power)
plt.xlabel('Time Frame')
plt.ylabel('Mean Power')
plt.title('Mean Power Spectrum')
plt.show()
