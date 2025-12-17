from fastapi import FastAPI
from .routers import chat, documents
from .routers import auth
from .routers import personalization
from .routers import translation

app = FastAPI(title="AI-Interactive Book Backend", version="1.0.0")

# Include routers
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
app.include_router(documents.router, prefix="/api/v1", tags=["documents"])
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(personalization.router, prefix="/api/v1", tags=["personalization"])
app.include_router(translation.router, prefix="/api/v1", tags=["translation"])

@app.get("/")
def read_root():
    return {"message": "AI-Interactive Book Backend API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}