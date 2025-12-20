"""
Sample processing code for auditory datasets in Chapter 04
This script demonstrates how to load and process auditory datasets for humanoid robotics
"""
import librosa
import numpy as np
import json
import matplotlib.pyplot as plt
from pathlib import Path
import scipy.signal


def load_audio_data(dataset_path, sample_id):
    """
    Load audio data from the dataset
    
    Args:
        dataset_path: Path to the dataset directory
        sample_id: Identifier for the specific audio sample to load
    
    Returns:
        Dictionary containing audio signal, sample rate, and metadata
    """
    # Construct paths to the data files
    audio_path = Path(dataset_path) / f"audio_samples/{sample_id}/audio.wav"
    metadata_path = Path(dataset_path) / f"audio_samples/{sample_id}/metadata.json"
    
    # Load audio signal
    audio_signal, sample_rate = librosa.load(str(audio_path), sr=None)  # Keep original sample rate
    
    # Load metadata
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    return {
        'signal': audio_signal,
        'sample_rate': sample_rate,
        'metadata': metadata
    }


def visualize_audio_data(audio_data):
    """
    Visualize audio signal in time and frequency domains
    
    Args:
        audio_data: Dictionary containing 'signal' and 'sample_rate' keys
    """
    signal = audio_data['signal']
    sample_rate = audio_data['sample_rate']
    
    # Create time axis
    time_axis = np.linspace(0, len(signal) / sample_rate, len(signal))
    
    # Plot time domain
    plt.figure(figsize=(15, 10))
    
    plt.subplot(3, 1, 1)
    plt.plot(time_axis, signal)
    plt.title('Audio Signal - Time Domain')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    
    # Plot spectrogram
    plt.subplot(3, 1, 2)
    nperseg = min(1024, len(signal))  # Ensure nperseg is not greater than signal length
    f, t, Sxx = scipy.signal.spectrogram(signal, fs=sample_rate, nperseg=nperseg)
    im = plt.pcolormesh(t, f, 10 * np.log10(Sxx + 1e-10), shading='gouraud')
    plt.ylabel('Frequency (Hz)')
    plt.xlabel('Time (s)')
    plt.title('Spectrogram')
    plt.colorbar(im, label='Power (dB)')
    
    # Plot MFCCs (Mel-Frequency Cepstral Coefficients)
    plt.subplot(3, 1, 3)
    mfccs = librosa.feature.mfcc(y=signal, sr=sample_rate, n_mfcc=13)
    librosa.display.specshow(mfccs, sr=sample_rate, x_axis='time')
    plt.ylabel('MFCC Coefficient')
    plt.xlabel('Time (s)')
    plt.title('Mel-Frequency Cepstral Coefficients')
    plt.colorbar()
    
    plt.tight_layout()
    plt.show()


def detect_speech(audio_signal, sample_rate):
    """
    Detect speech segments in the audio signal
    
    Args:
        audio_signal: Audio signal as numpy array
        sample_rate: Sample rate of the audio signal
    
    Returns:
        List of speech segment start and end times in seconds
    """
    # Use librosa's voice activity detection based on spectral features
    # This is a simplified approach - real VAD systems are more sophisticated
    
    # Compute spectral features
    spectral_centroids = librosa.feature.spectral_centroid(y=audio_signal, sr=sample_rate)[0]
    rms = librosa.feature.rms(y=audio_signal)[0]
    
    # Normalize features
    spectral_centroids_norm = (spectral_centroids - np.mean(spectral_centroids)) / np.std(spectral_centroids)
    rms_norm = (rms - np.mean(rms)) / np.std(rms)
    
    # Combine features to detect speech activity
    activity = (spectral_centroids_norm > 0.5) & (rms_norm > 0.5)
    
    # Find contiguous segments of activity
    # This is a simplified approach - real systems would use more sophisticated methods
    speech_segments = []
    in_speech = False
    start_idx = 0
    
    # Time step for each frame (using hop_length of 512 samples by default)
    hop_length = 512
    frame_duration = hop_length / sample_rate
    
    for i, active in enumerate(activity):
        if active and not in_speech:
            # Start of speech segment
            start_idx = i
            in_speech = True
        elif not active and in_speech:
            # End of speech segment
            start_time = start_idx * frame_duration
            end_time = i * frame_duration
            speech_segments.append({'start': start_time, 'end': end_time})
            in_speech = False
    
    # Handle case where speech continues to end of signal
    if in_speech:
        start_time = start_idx * frame_duration
        end_time = len(activity) * frame_duration
        speech_segments.append({'start': start_time, 'end': end_time})
    
    return speech_segments


def classify_sound_type(audio_signal, sample_rate):
    """
    Classify the type of sound in the audio signal
    This is a simplified example - in practice, you would use a trained classifier
    
    Args:
        audio_signal: Audio signal as numpy array
        sample_rate: Sample rate of the audio signal
    
    Returns:
        Predicted sound type
    """
    # Calculate features for classification
    # Zero crossing rate - indicates frequency content
    zcr = librosa.feature.zero_crossing_rate(audio_signal)[0]
    avg_zcr = np.mean(zcr)
    
    # Spectral rolloff - shows frequency distribution
    rolloff = librosa.feature.spectral_rolloff(y=audio_signal, sr=sample_rate)[0]
    avg_rolloff = np.mean(rolloff)
    
    # RMS energy - indicates loudness
    rms = librosa.feature.rms(y=audio_signal)[0]
    avg_rms = np.mean(rms)
    
    # Bandwidth features
    bandwidth = librosa.feature.spectral_bandwidth(y=audio_signal, sr=sample_rate)[0]
    avg_bandwidth = np.mean(bandwidth)
    
    # Simplified classification based on features
    if avg_rms > 0.05 and avg_zcr > 0.02:
        return "Speech"
    elif avg_rms > 0.02 and avg_zcr < 0.01:
        return "Environmental Noise"
    elif avg_rolloff > 2000 and avg_zcr > 0.04:
        return "Mechanical Sound"
    elif avg_zcr < 0.005:
        return "Music"
    else:
        return "Other"


def estimate_sound_direction(audio_signals, sample_rate):
    """
    Estimate sound direction from multichannel audio
    This is a simplified approach using inter-channel time differences
    
    Args:
        audio_signals: Dictionary of audio signals from different channels/microphones
        sample_rate: Sample rate of the audio signals
    
    Returns:
        Estimated direction in radians or degrees
    """
    # This is a simplified approach - real systems use more sophisticated methods like GCC-PHAT
    if len(audio_signals) < 2:
        return 0.0  # Cannot estimate direction with single channel
    
    # Use first two channels for demonstration
    signal1 = audio_signals[0]
    signal2 = audio_signals[1]
    
    # Compute cross-correlation to find time delay
    correlation = scipy.signal.correlate(signal1, signal2, mode='full')
    lags = scipy.signal.correlation_lags(len(signal1), len(signal2), mode='full')
    
    # Find the lag with maximum correlation
    max_lag_idx = np.argmax(correlation)
    max_lag = lags[max_lag_idx]
    
    # Convert lag to time difference
    time_diff = max_lag / sample_rate
    
    # Convert time difference to angle (simplified)
    # Assuming microphone distance of 0.1m and speed of sound 343 m/s
    mic_distance = 0.1  # meters
    speed_of_sound = 343.0  # m/s
    
    # Calculate angle using simple geometric relationship
    angle_rad = np.arcsin(time_diff * speed_of_sound / mic_distance)
    
    return np.degrees(angle_rad)


def process_auditory_dataset(dataset_path):
    """
    Complete pipeline for processing an auditory dataset
    
    Args:
        dataset_path: Path to the auditory dataset directory
    """
    print("Processing auditory dataset...")
    
    # Example: Load a sample
    sample_data = load_audio_data(dataset_path, "sample_001")
    
    # Visualize the audio data
    print("Visualizing audio data...")
    visualize_audio_data(sample_data)
    
    # Detect speech segments
    print("Detecting speech segments...")
    speech_segments = detect_speech(sample_data['signal'], sample_data['sample_rate'])
    print(f"Detected {len(speech_segments)} speech segments")
    for i, seg in enumerate(speech_segments[:3]):  # Show first 3 segments
        print(f"  Segment {i+1}: {seg['start']:.2f}s to {seg['end']:.2f}s")
    
    # Classify sound type
    print("Classifying sound type...")
    sound_type = classify_sound_type(sample_data['signal'], sample_data['sample_rate'])
    print(f"Predicted sound type: {sound_type}")
    
    print("Auditory dataset processing complete.")


if __name__ == "__main__":
    # Example usage
    # Note: This is a demonstration script - you would need to provide actual paths to the dataset
    dataset_path = "path/to/auditory_dataset"
    
    # Since we don't have the actual dataset, we can't run the full pipeline
    # But we can show what the functions do
    print("Auditory dataset processing functions ready.")
    print("To use these functions, call process_auditory_dataset() with the path to your dataset.")