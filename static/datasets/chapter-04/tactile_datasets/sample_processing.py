"""
Sample processing code for tactile datasets in Chapter 04
This script demonstrates how to load and process tactile datasets for humanoid robotics
"""
import numpy as np
import json
import matplotlib.pyplot as plt
from pathlib import Path


def load_tactile_data(dataset_path, sample_id):
    """
    Load tactile sensor data from the dataset
    
    Args:
        dataset_path: Path to the dataset directory
        sample_id: Identifier for the specific sample to load
    
    Returns:
        Dictionary containing tactile readings and metadata
    """
    # Construct paths to the data files
    tactile_path = Path(dataset_path) / f"tactile_readings/{sample_id}/readings.json"
    metadata_path = Path(dataset_path) / f"tactile_readings/{sample_id}/metadata.json"
    
    # Load tactile data
    with open(tactile_path, 'r') as f:
        tactile_data = json.load(f)
    
    # Load metadata
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    # Convert to numpy arrays for processing
    tactile_readings = np.array(tactile_data['readings'])
    timestamps = np.array(tactile_data['timestamps'])
    
    return {
        'readings': tactile_readings,
        'timestamps': timestamps,
        'metadata': metadata
    }


def visualize_tactile_data(data):
    """
    Visualize tactile sensor readings
    
    Args:
        data: Dictionary containing tactile readings and metadata
    """
    readings = data['readings']
    timestamps = data['timestamps']
    metadata = data['metadata']
    
    # Create visualization based on sensor type
    sensor_type = metadata.get('sensor_type', 'generic')
    
    if sensor_type == 'BioTac':
        # For BioTac sensors, we have multiple taxels
        n_taxels = readings.shape[1] if len(readings.shape) > 1 else 1
        
        if n_taxels > 1:
            # Plot readings for each taxel over time
            plt.figure(figsize=(15, 8))
            for i in range(min(n_taxels, 8)):  # Limit to first 8 taxels for readability
                plt.subplot(4, 2, i+1)
                plt.plot(timestamps, readings[:, i])
                plt.title(f'Taxel {i+1}')
                plt.xlabel('Time (s)')
                plt.ylabel('Pressure (a.u.)')
            plt.tight_layout()
            plt.show()
        else:
            # If only one value per reading
            plt.figure(figsize=(12, 6))
            plt.plot(timestamps, readings, linewidth=2)
            plt.title('Tactile Sensor Readings Over Time')
            plt.xlabel('Time (s)')
            plt.ylabel('Pressure (a.u.)')
            plt.grid(True)
            plt.show()
    
    elif sensor_type == 'GelSight':
        # For GelSight, we might have image-like tactile data
        if len(readings.shape) == 3:  # 3D array (time, height, width)
            # Visualize a few frames
            n_frames = min(5, readings.shape[0])
            fig, axes = plt.subplots(1, n_frames, figsize=(15, 3))
            for i in range(n_frames):
                if n_frames == 1:
                    axes.imshow(readings[i], cmap='gray')
                    axes.set_title(f'Frame {i}')
                else:
                    axes[i].imshow(readings[i], cmap='gray')
                    axes[i].set_title(f'Frame {i}')
            plt.tight_layout()
            plt.show()
        else:
            # Otherwise, plot like regular readings
            plt.figure(figsize=(12, 6))
            plt.plot(timestamps, readings, linewidth=2)
            plt.title('Tactile Sensor Readings Over Time')
            plt.xlabel('Time (s)')
            plt.ylabel('Tactile Value')
            plt.grid(True)
            plt.show()
    
    else:
        # Generic visualization
        plt.figure(figsize=(12, 6))
        if len(readings.shape) > 1:
            # Multiple channels
            for i in range(readings.shape[1]):
                plt.plot(timestamps, readings[:, i], label=f'Channel {i+1}', alpha=0.7)
            plt.legend()
        else:
            # Single channel
            plt.plot(timestamps, readings, linewidth=2)
        plt.title(f'Tactile Readings ({sensor_type})')
        plt.xlabel('Time (s)')
        plt.ylabel('Sensor Value')
        plt.grid(True)
        plt.show()


def detect_contact_events(tactile_readings, threshold=0.1):
    """
    Detect contact events from tactile readings
    
    Args:
        tactile_readings: Array of tactile sensor readings
        threshold: Threshold for contact detection
    
    Returns:
        Array of contact event timestamps
    """
    # Compute the average of all taxels for each time step
    if len(tactile_readings.shape) > 1:
        avg_readings = np.mean(tactile_readings, axis=1)
    else:
        avg_readings = tactile_readings
    
    # Detect when readings exceed threshold
    contact_events = np.where(avg_readings > threshold)[0]
    
    return contact_events


def classify_material_from_tactile(tactile_readings):
    """
    Classify material based on tactile readings
    This is a simplified example - in practice, you would use a trained classifier
    
    Args:
        tactile_readings: Tactile sensor readings (time, sensors)
    
    Returns:
        Predicted material class
    """
    # In a real implementation, this function would use a trained model
    # For this example, we'll use simple heuristics based on texture and compliance
    
    # Calculate features from the tactile readings
    avg_pressure = np.mean(tactile_readings, axis=0) if len(tactile_readings.shape) > 1 else tactile_readings
    pressure_variance = np.var(tactile_readings, axis=0) if len(tactile_readings.shape) > 1 else np.var(tactile_readings)
    
    # Simplified classification based on average pressure and variance
    mean_pressure = np.mean(avg_pressure) if isinstance(avg_pressure, np.ndarray) else avg_pressure
    mean_variance = np.mean(pressure_variance) if isinstance(pressure_variance, np.ndarray) else pressure_variance
    
    if mean_pressure < 0.2 and mean_variance < 0.05:
        return "Soft/Foam-like"
    elif mean_pressure > 0.8 and mean_variance < 0.1:
        return "Hard/Smooth"
    elif mean_variance > 0.2:
        return "Rough/Textured"
    else:
        return "Medium/Mixed"
    

def process_tactile_dataset(dataset_path):
    """
    Complete pipeline for processing a tactile dataset
    
    Args:
        dataset_path: Path to the tactile dataset directory
    """
    print("Processing tactile dataset...")
    
    # Example: Load a sample
    sample_data = load_tactile_data(dataset_path, "sample_001")
    
    # Visualize the tactile data
    print("Visualizing tactile data...")
    visualize_tactile_data(sample_data)
    
    # Detect contact events
    print("Detecting contact events...")
    contact_events = detect_contact_events(sample_data['readings'])
    print(f"Detected {len(contact_events)} contact events")
    
    # Classify material
    print("Classifying material from tactile data...")
    material_class = classify_material_from_tactile(sample_data['readings'])
    print(f"Predicted material: {material_class}")
    
    print("Tactile dataset processing complete.")


if __name__ == "__main__":
    # Example usage
    # Note: This is a demonstration script - you would need to provide actual paths to the dataset
    dataset_path = "path/to/tactile_dataset"
    
    # Since we don't have the actual dataset, we can't run the full pipeline
    # But we can show what the functions do
    print("Tactile dataset processing functions ready.")
    print("To use these functions, call process_tactile_dataset() with the path to your dataset.")