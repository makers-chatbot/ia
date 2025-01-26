from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
import json

from models import ChatMessage, ChatResponse
from websocket_manager import WebSocketManager

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Inventory Chat Service")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize WebSocket manager
ws_manager = WebSocketManager()


@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """HTTP endpoint for Streamlit compatibility"""
    try:
        response = await ws_manager.chat_engine.process_message(
            message.message, message.session_id or "default"
        )
        return ChatResponse(message=response)
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return ChatResponse(message="Lo siento, hubo un error al procesar tu mensaje.")


@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    session_id = await ws_manager.connect(websocket)
    try:
        while True:
            try:
                data = await websocket.receive_text()
                message_data = json.loads(data)
                user_message = message_data.get("message", "")
                await ws_manager.process_message(websocket, user_message, session_id)
            except json.JSONDecodeError:
                await websocket.send_json(
                    {
                        "message": "Formato de mensaje inválido. Por favor envía un objeto JSON con un campo 'message'."
                    }
                )
            except WebSocketDisconnect:
                ws_manager.disconnect(session_id)
                break
    except Exception as e:
        print(f"WebSocket error: {e}")
        ws_manager.disconnect(session_id)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
