# Chapter 06: Human-Robot Interaction - FastAPI Endpoints

This repository contains the FastAPI endpoints that serve as the reproducibility checkpoint for Chapter 06 of the Physical AI and Humanoid Robotics Course. These endpoints demonstrate key concepts in human-robot interaction through well-documented APIs.

## Contents

- `api/`: Main API implementation with endpoints, models, and services
  - `endpoints/`: API route definitions
    - `speech.py`: Endpoints for speech recognition and synthesis
    - `gestures.py`: Endpoints for gesture recognition and generation
    - `emotions.py`: Endpoints for emotion detection and response
    - `multimodal.py`: Endpoints for multi-modal interaction
  - `models/`: Pydantic models for request/response validation
    - `hri_requests.py`: Request models for HRI interactions
    - `hri_responses.py`: Response models for HRI interactions
    - `interaction_models.py`: Core HRI data models
  - `services/`: Business logic implementations
    - `speech_recognition.py`: Speech processing services
    - `emotion_analysis.py`: Emotion recognition services
    - `interaction_manager.py`: Core interaction management

- `docs/`: API documentation and specifications
  - `api_spec.yaml`: OpenAPI specification in YAML format
  - `api_spec.json`: OpenAPI specification in JSON format
  - `user_guide.md`: Usage guide for the API

- `tests/`: Unit and integration tests
  - `test_speech.py`: Tests for speech endpoints
  - `test_gestures.py`: Tests for gesture endpoints
  - `test_emotions.py`: Tests for emotion endpoints
  - `integration_tests.py`: End-to-end integration tests

- `config/`: Configuration settings
  - `settings.py`: Application settings and configuration

- `notebooks/`: Jupyter notebooks with API usage tutorials
  - `tutorial_1_speech_interactions.ipynb`: Speech interaction examples
  - `tutorial_2_emotion_recognition.ipynb`: Emotion recognition examples
  - `tutorial_3_multimodal_interaction.ipynb`: Multi-modal examples

## Getting Started

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Start the API server:
```bash
python run_server.py
```

3. Access the API documentation at `http://localhost:8000/docs`

## API Endpoints

### Speech Interaction
- `POST /api/v1/speech/recognize`: Convert audio to text
- `POST /api/v1/speech/synthesize`: Convert text to speech
- `POST /api/v1/speech/diarize`: Identify speakers in audio

### Gesture Recognition
- `POST /api/v1/gestures/detect`: Detect gestures from video feed
- `POST /api/v1/gestures/generate`: Generate appropriate robot gestures
- `GET /api/v1/gestures/list`: Get available gesture types

### Emotion Detection
- `POST /api/v1/emotions/detect`: Detect emotions from facial expressions or voice
- `POST /api/v1/emotions/respond`: Get appropriate emotional responses
- `GET /api/v1/emotions/list`: Get available emotion types

### Multi-modal Interaction
- `POST /api/v1/multimodal/process`: Process combined modalities
- `POST /api/v1/multimodal/generate`: Generate multi-modal responses

## Reproducibility

All endpoints are documented with:
- Detailed parameter descriptions
- Example requests and responses
- Expected behavior and output
- Performance benchmarks

## Validation

Run the validation script to ensure all endpoints work correctly:
```bash
pytest tests/
```

## Security

The API includes authentication and authorization:
- API key authentication for all endpoints
- Rate limiting to prevent abuse
- Input validation to prevent injection attacks