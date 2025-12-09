# Physical AI & Humanoid Robotics Course

This repository contains an interactive course on Physical AI and Humanoid Robotics with an integrated AI chatbot. The course covers ROS 2, Gazebo, NVIDIA Isaac, and Vision-Language-Action systems.

## Structure

- `website/`: Docusaurus-based course site with embedded chatbot
- `backend/`: FastAPI backend for the AI chatbot with RAG capabilities
- `docs/`: Course content in Markdown format

## Prerequisites

- Node.js (v20 or higher)
- Python (v3.8 or higher)
- npm

## Frontend Setup (Docusaurus Book)

1. Navigate to the website directory:
```bash
cd website
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The book will be available at `http://localhost:3000`.

## Backend Setup (FastAPI Chatbot)

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Create a .env file with your API keys
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
OPENAI_API_KEY=your_openai_api_key
```

5. Run the backend:
```bash
python main.py
```

The backend will be available at `http://localhost:8000`.

## How It Works

The book integrates with the backend API through the embedded chatbot component. When users ask questions about the content, the frontend sends the query to the backend, which retrieves relevant information from the indexed documentation and generates a response using OpenAI.

## Deployment

This project is configured for GitHub Pages deployment using GitHub Actions. When you push to the `main` branch, the workflow will automatically build and deploy the Docusaurus site to GitHub Pages at `https://panaversity.github.io/hackathon01/`.

## Technologies Used

- **Docusaurus**: Static site generator for documentation
- **React**: Frontend component development
- **FastAPI**: Backend API framework
- **OpenAI**: Language model for text generation
- **Qdrant**: Vector database for document similarity search
- **ROS 2**: Middleware for robot control and communication
- **Gazebo**: Physics simulation environment
- **NVIDIA Isaac**: Advanced perception and training systems