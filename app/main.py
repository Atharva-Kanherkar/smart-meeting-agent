import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Add project root to path for agents import
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Try to import Portia, fallback if not available
try:
    from portia import Config, StorageClass, LLMProvider
    PORTIA_AVAILABLE = True
    print("✅ Portia SDK loaded successfully")
except ImportError as e:
    print(f"⚠️ Portia not available: {e}")
    print("🔄 Running in compatibility mode")
    PORTIA_AVAILABLE = False
    
    # Create mock classes for compatibility
    class Config:
        @staticmethod
        def from_default(**kwargs):
            return {"mock": True}
    
    class StorageClass:
        CLOUD = "cloud"
    
    class LLMProvider:
        GOOGLE = "google"

# Load environment variables (only in development)
if os.getenv("RENDER") != "true":
    load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    if PORTIA_AVAILABLE:
        print("🚀 Smart Meeting Agent API starting up with Portia...")
    else:
        print("🚀 Smart Meeting Agent API starting up in compatibility mode...")
    yield
    # Shutdown
    print("📴 Smart Meeting Agent API shutting down...")

app = FastAPI(
    title="Smart Meeting Agent API",
    description="Multi-agent system for comprehensive meeting preparation",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if os.getenv("ENVIRONMENT") != "production" else None,
    redoc_url="/redoc" if os.getenv("ENVIRONMENT") != "production" else None
)

# CORS middleware
allowed_origins = ["*"] if os.getenv("ENVIRONMENT") != "production" else [
    "https://your-frontend-domain.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize configuration
def get_config():
    if not PORTIA_AVAILABLE:
        print("⚠️ Portia not available, using mock configuration")
        return {"mock": True}
        
    required_keys = ["PORTIA_API_KEY", "GOOGLE_API_KEY", "TAVILY_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    if missing_keys:
        print(f"⚠️ Missing environment variables: {', '.join(missing_keys)}")
        return {"mock": True}
    
    return Config.from_default(
        storage_class=StorageClass.CLOUD,
        llm_provider=LLMProvider.GOOGLE,
    )

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "Smart Meeting Agent API is running", 
        "status": "healthy",
        "portia_available": PORTIA_AVAILABLE,
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "portia_available": PORTIA_AVAILABLE,
        "environment": os.getenv("ENVIRONMENT", "development"),
        "timestamp": "2025-01-01T00:00:00Z"
    }

# Basic meeting endpoint for testing
@app.post("/api/v1/meetings/prepare")
async def prepare_meeting(meeting_data: dict):
    if not PORTIA_AVAILABLE:
        return {
            "job_id": "mock_job_123",
            "status": "started",
            "message": "Meeting preparation started (mock mode)",
            "data": meeting_data,
            "note": "Running in compatibility mode without Portia"
        }
    
    # Your actual meeting preparation logic here
    return {
        "job_id": "real_job_456", 
        "status": "started",
        "message": "Meeting preparation started with Portia"
    }

# Include other routes if they exist and are compatible
try:
    from v1.routes import meetings, health, agents
    app.include_router(health.router, prefix="/api/v1", tags=["health"])
    app.include_router(meetings.router, prefix="/api/v1", tags=["meetings"])
    app.include_router(agents.router, prefix="/api/v1", tags=["agents"])
    print("✅ All routes loaded successfully")
except ImportError as e:
    print(f"⚠️ Some routes not available: {e}")
    print("🔄 Running with basic routes only")