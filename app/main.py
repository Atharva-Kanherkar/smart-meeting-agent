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

from portia import Config, StorageClass, LLMProvider

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Smart Meeting Agent API starting up...")
    yield
    # Shutdown
    print("📴 Smart Meeting Agent API shutting down...")

app = FastAPI(
    title="Smart Meeting Agent API",
    description="Multi-agent system for comprehensive meeting preparation",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Portia configuration
def get_config():
    required_keys = ["PORTIA_API_KEY", "GOOGLE_API_KEY", "TAVILY_API_KEY"]
    if not all(os.getenv(key) for key in required_keys):
        raise ValueError(f"Missing required environment variables: {', '.join(required_keys)}")
    
    return Config.from_default(
        storage_class=StorageClass.CLOUD,
        llm_provider=LLMProvider.GOOGLE,
    )

# Import and include routes after app creation
from v1.routes import meetings, health, agents

app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(meetings.router, prefix="/api/v1", tags=["meetings"])
app.include_router(agents.router, prefix="/api/v1", tags=["agents"])