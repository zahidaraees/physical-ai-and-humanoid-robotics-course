"""
Sample processing code for visual datasets in Chapter 04
This script demonstrates how to load and process visual datasets for humanoid robotics
"""
import cv2
import numpy as np
import json
import matplotlib.pyplot as plt
from pathlib import Path


def load_rgbd_scene(dataset_path, scene_id):
    """
    Load an RGB-D scene from the dataset
    
    Args:
        dataset_path: Path to the dataset directory
        scene_id: Identifier for the specific scene to load
    
    Returns:
        Dictionary containing RGB image, depth map, and camera parameters
    """
    # Construct paths to the data files
    rgb_path = Path(dataset_path) / f"scenes/{scene_id}/rgb.png"
    depth_path = Path(dataset_path) / f"scenes/{scene_id}/depth.png"
    camera_params_path = Path(dataset_path) / f"scenes/{scene_id}/camera_params.json"
    
    # Load RGB image
    rgb_image = cv2.imread(str(rgb_path))
    rgb_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2RGB)  # Convert to RGB
    
    # Load depth map
    depth_map = cv2.imread(str(depth_path), cv2.IMREAD_UNCHANGED).astype(np.float32)
    
    # Normalize depth if needed (depends on storage format)
    # If depth is stored as 16-bit, it might be in millimeters
    if depth_map.dtype == np.uint16:
        depth_map = depth_map / 1000.0  # Convert from mm to meters
    
    # Load camera parameters
    with open(camera_params_path, 'r') as f:
        camera_params = json.load(f)
    
    return {
        'rgb': rgb_image,
        'depth': depth_map,
        'camera_params': camera_params
    }


def visualize_rgbd_data(data):
    """
    Visualize RGB-D data with matplotlib
    
    Args:
        data: Dictionary containing 'rgb' and 'depth' keys
    """
    fig, axes = plt.subplots(1, 2, figsize=(15, 7))
    
    # Visualize RGB image
    axes[0].imshow(data['rgb'])
    axes[0].set_title('RGB Image')
    axes[0].axis('off')
    
    # Visualize depth map
    im = axes[1].imshow(data['depth'], cmap='viridis')
    axes[1].set_title('Depth Map')
    axes[1].axis('off')
    plt.colorbar(im, ax=axes[1], label='Depth (m)')
    
    plt.tight_layout()
    plt.show()


def detect_objects_in_scene(rgb_image, model_path=None):
    """
    Perform object detection in the RGB image
    This is a simplified example - in practice, you would use a trained model
    
    Args:
        rgb_image: RGB image as numpy array
        model_path: Path to pre-trained object detection model (optional)
    
    Returns:
        Detected objects with bounding boxes and class labels
    """
    # In a real implementation, this function would:
    # 1. Load a pre-trained object detection model
    # 2. Run inference on the image
    # 3. Return detected objects
    
    # For this example, we'll return dummy data
    height, width = rgb_image.shape[:2]
    
    # Generate some example bounding boxes and labels
    objects = [
        {
            'bbox': [int(0.1*width), int(0.2*height), int(0.3*width), int(0.4*height)],
            'label': 'chair',
            'confidence': 0.92
        },
        {
            'bbox': [int(0.5*width), int(0.1*height), int(0.7*width), int(0.3*height)],
            'label': 'person',
            'confidence': 0.98
        },
        {
            'bbox': [int(0.3*width), int(0.6*height), int(0.4*width), int(0.8*height)],
            'label': 'table',
            'confidence': 0.87
        }
    ]
    
    return objects


def visualize_detections(rgb_image, objects):
    """
    Visualize object detections on the RGB image
    
    Args:
        rgb_image: RGB image as numpy array
        objects: List of detected objects with bbox, label, and confidence
    """
    # Create a copy of the image for visualization
    vis_image = rgb_image.copy()
    
    for obj in objects:
        # Extract bounding box coordinates
        x1, y1, x2, y2 = obj['bbox']
        
        # Draw bounding box
        cv2.rectangle(vis_image, (x1, y1), (x2, y2), (255, 0, 0), 2)
        
        # Add label and confidence
        label = f"{obj['label']} ({obj['confidence']:.2f})"
        cv2.putText(vis_image, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    
    # Display the image with detections
    plt.figure(figsize=(10, 7))
    plt.imshow(vis_image)
    plt.title('Object Detections')
    plt.axis('off')
    plt.show()


def process_visual_dataset(dataset_path):
    """
    Complete pipeline for processing a visual dataset
    
    Args:
        dataset_path: Path to the visual dataset directory
    """
    print("Processing visual dataset...")
    
    # Example: Load a sample scene
    scene_data = load_rgbd_scene(dataset_path, "sample_scene_001")
    
    # Visualize the RGB-D data
    print("Visualizing RGB-D data...")
    visualize_rgbd_data(scene_data)
    
    # Perform object detection
    print("Performing object detection...")
    objects = detect_objects_in_scene(scene_data['rgb'])
    
    # Visualize detections
    print("Visualizing detections...")
    visualize_detections(scene_data['rgb'], objects)
    
    print("Visual dataset processing complete.")


if __name__ == "__main__":
    # Example usage
    # Note: This is a demonstration script - you would need to provide actual paths to the dataset
    dataset_path = "path/to/rgbd_scenes_dataset"
    
    # Since we don't have the actual dataset, we can't run the full pipeline
    # But we can show what the functions do
    print("Visual dataset processing functions ready.")
    print("To use these functions, call process_visual_dataset() with the path to your dataset.")