# AI Inventory Assistant

A LangChain-based AI system for managing and querying computer inventory through natural language.

## Structure

```
├── langchain_server/     # Core LangChain service
│   ├── chat_engine.py   # Chat processing and response generation
│   ├── inventory.py     # Inventory management logic
│   ├── inventory_service.py  # Main service entry point
│   ├── models.py        # Data models and schemas
│   └── websocket_manager.py  # WebSocket communication handler
├── websocket_server/     # WebSocket server for AI communication
│   └── chat_app.py      # Chat application server
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose configuration
└── requirements.txt      # Python dependencies
```

## Setup

### Local Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```
OPENAI_API_KEY=your_key_here
```

### Docker Setup

1. Make sure you have Docker and Docker Compose installed
2. Create a `.env` file with your OpenAI API key
3. Build and start the service:
```bash
docker-compose up --build
```

## Running the Service

### Local Run
Start the LangChain server:
```bash
python langchain_server/inventory_service.py
```

### Docker Run
```bash
# Start the service
docker-compose up

# Run in background
docker-compose up -d

# Stop the service
docker-compose down
```

The service will be available via WebSocket for client applications to connect.

## Features

- Natural language processing for inventory queries
- Persistent conversation memory
- Product inventory management and tracking
- Smart product comparisons and recommendations
- Inventory statistics and analytics
- Extensible agent-based architecture

## API Capabilities

The AI assistant can handle queries like:
- Inventory status and availability
- Detailed product information and specifications
- Product comparisons and recommendations
- Price range analysis
- Stock management operations 