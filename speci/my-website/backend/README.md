# AI-Interactive Book Backend

This is the backend service for the AI-Interactive Book with RAG Chatbot project.

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables (copy `.env.example` to `.env` and fill in values)

4. Run the development server:
   ```bash
   uvicorn backend.main:app --reload --port 8000
   ```

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /api/v1/chat` - Chat with the RAG system
- `POST /api/v1/documents/index` - Index a document
- `GET /api/v1/documents/sources` - Get available document sources

## Configuration

The backend can be configured using environment variables as defined in `config.py`.