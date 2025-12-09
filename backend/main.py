from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import openai
import os
import logging
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Physical AI & Humanoid Robotics Course API",
    description="API for the Physical AI & Humanoid Robotics Course",
    version="1.0.0"
)

# Configuration
QDRANT_URL = os.getenv("QDRANT_URL", "YOUR_QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "YOUR_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_KEY")

# Initialize clients
qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Initialize embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

class MessageRequest(BaseModel):
    message: str
    context: Optional[str] = None
    selected_text: Optional[str] = None

class MessageResponse(BaseModel):
    response: str
    sources: List[str]

@app.get("/")
def read_root():
    return {"message": "Physical AI & Humanoid Robotics Course API is running!"}

@app.post("/api/chat", response_model=MessageResponse)
async def chat_with_robotics_kb(request: MessageRequest):
    """
    Main endpoint for chat functionality about Physical AI and Robotics
    """
    try:
        logger.info(f"Received message: {request.message}")

        # Combine the user's query with any selected text context
        enhanced_query = request.message
        if request.selected_text:
            enhanced_query = f"{request.message}\n\nAdditional context from selected text: {request.selected_text}"

        # Generate embedding for the query
        query_embedding = embedding_model.encode(enhanced_query).tolist()

        # Search in Qdrant for relevant documents
        search_result = qdrant_client.search(
            collection_name="robotics_content",
            query_vector=query_embedding,
            limit=5  # Retrieve top 5 most relevant documents
        )

        # Extract content from search results to use as context
        context_parts = []
        sources = []

        for hit in search_result:
            content = hit.payload.get("content", "")
            source = hit.payload.get("source", "Unknown")
            context_parts.append(content)
            sources.append(source)

        # Combine all context parts
        full_context = "\n\n".join(context_parts)

        # Prepare the system message with context
        system_message = f"""
        You are an AI assistant for the Physical AI & Humanoid Robotics Course.
        You help students understand concepts related to robotics, ROS 2, Gazebo simulation,
        NVIDIA Isaac, and Vision-Language-Action systems.
        Use the following context to answer the user's question.
        If the context doesn't contain relevant information, respond that you don't have enough information from the book to answer the question.

        Context: {full_context}
        """

        # Create the conversation for OpenAI
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": request.message}
        ]

        # Get response from OpenAI
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )

        # Extract the response content
        ai_response = response.choices[0].message.content

        return MessageResponse(
            response=ai_response,
            sources=sources
        )

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/api/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}

@app.post("/api/robot-control")
async def robot_control_command(command: str):
    """
    Endpoint for sending high-level commands to simulated robots
    """
    try:
        # Use OpenAI to convert natural language to robot commands
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a robot command interpreter. Convert natural language commands into specific robot action sequences. Respond with JSON containing action type and parameters. Possible actions: 'move', 'grasp', 'turn', 'stop', 'navigate'. Example: {'action': 'navigate', 'params': {'x': 1.0, 'y': 2.0}}"
                },
                {"role": "user", "content": f"Convert this command to robot action: {command}"}
            ]
        )

        action_sequence = response.choices[0].message.content
        logger.info(f"Generated robot action sequence: {action_sequence}")

        # In a real implementation, this would send commands to the robot via ROS 2
        # For this demo, we'll just return the action sequence

        return {"action_sequence": action_sequence}

    except Exception as e:
        logger.error(f"Error processing robot command: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing robot command: {str(e)}")

if __name__ == "__main__":
    # This allows running the app directly with Python for testing
    uvicorn.run(app, host="0.0.0.0", port=8000)