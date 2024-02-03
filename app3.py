import time
import numpy as np
import librosa
import argparse
import os
import soundfile as sf

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-audio', type=str,
                        help='path to audiofile')
    arguments = parser.parse_args()
    return arguments

def remove_high_power_segments(input_audio, output_audio, threshold=475):
    # Load the audio file
    data, sr = librosa.load(input_audio)
    
    # Calculate the short-time Fourier transform (STFT)
    D = librosa.stft(data)

    # Compute the power spectrogram
    power_spectrogram = np.abs(D)**2

    # Calculate the mean power across frequency bins for each time frame
    mean_power = np.mean(power_spectrogram, axis=0)

    # Create a mask to identify segments with mean power below the threshold
    mask = mean_power < threshold

    # Convert the mask to indices
    indices = np.nonzero(mask)[0]

    # Apply the mask to keep only segments with mean power below the threshold
    filtered_data = np.concatenate([data[idx * len(data)//len(mean_power):(idx + 1) * len(data)//len(mean_power)] for idx in indices])

    # Write the filtered audio to a new file
    sf.write(output_audio, filtered_data, sr)
    print("High power segments removed and saved as:", output_audio)

if __name__ == '__main__':
    start = time.time()
    args = get_arguments()
    
    input_audio = args.audio
    output_audio = input_audio.replace('.wav', '_filtered.wav')
    
    remove_high_power_segments(input_audio, output_audio)
    
    end = time.time()
    print('Elapsed time: {}'.format(end - start))
