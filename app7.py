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

def remove_high_power_segments(input_audio, output_audio, threshold=23, buffer_length=15):
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
    
    # Expand segments by adding buffer
    expanded_indices = set()
    for idx in indices:
        for i in range(max(0, idx - buffer_length), min(len(mean_power), idx + buffer_length + 1)):
            expanded_indices.add(i)

    # Apply the mask to keep only segments with mean power below the threshold
    segments_to_keep = set()
    for idx in expanded_indices:
        if idx in indices:
            for i in range(max(0, idx - buffer_length), min(len(mean_power), idx + buffer_length + 1)):
                segments_to_keep.add(i)

    # Concatenate segments to keep
    filtered_data = np.concatenate([data[idx * len(data)//len(mean_power):(idx + 1) * len(data)//len(mean_power)] for idx in sorted(segments_to_keep)])

    # Write the filtered audio to a new file
    sf.write(output_audio, filtered_data, sr)
    print("High power segments removed and saved as:", output_audio)

if __name__ == '__main__':
    start = time.time()
    args = get_arguments()
    
    audio_folder = args.audio
    
    # Check if the path exists and if it's a directory
    if os.path.isdir(audio_folder):
        for file_name in os.listdir(audio_folder):
            if file_name.endswith(".wav"):
                input_audio = os.path.join(audio_folder, file_name)
                output_audio = input_audio.replace('.wav', '_filtered.wav')
                remove_high_power_segments(input_audio, output_audio)
    else:
        print("Error: The provided path is not a directory or does not exist.")
    
    end = time.time()
    print('Elapsed time: {}'.format(end - start))
