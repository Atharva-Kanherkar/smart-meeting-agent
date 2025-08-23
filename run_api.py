import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    print("🚀 Starting Smart Meeting Agent API...")
    print("📊 API docs will be available at: http://localhost:8000/docs")
    print("🔗 Health check: http://localhost:8000/api/v1/health")
    print("🔧 Available endpoints:")
    print("   - POST /api/v1/meetings/prepare")
    print("   - POST /api/v1/meetings/prepare-custom") 
    print("   - GET /api/v1/meetings/jobs/{job_id}")
    print("   - POST /api/v1/agents/calendar")
    print("   - POST /api/v1/agents/people-research")
    print("   - POST /api/v1/agents/technical-context")
    print("   - POST /api/v1/agents/slack-context")  # NEW!
    print("   - POST /api/v1/agents/coordinator")
    print("   - GET /api/v1/health")
    print("\n" + "="*50)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )