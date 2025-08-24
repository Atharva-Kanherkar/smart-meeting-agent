# Smart Meeting Agent Backend: Comprehensive Technical Documentation

## Table of Contents
1. System Overview
2. Architecture & Design Patterns
3. Technology Stack
4. Project Structure
5. Core Components
6. API Layer
7. Service Layer
8. Agent System
9. Data Models
10. State Management
11. Authentication & OAuth
12. Error Handling
13. Missing Pieces & Limitations
14. Frontend Integration Guide
15. Deployment & Configuration

---

## System Overview

The Smart Meeting Agent is a **FastAPI-based microservice** that orchestrates multiple AI agents to automatically prepare comprehensive meeting briefings. The system follows a **multi-agent architecture** where specialized AI workers collaborate to gather, analyze, and synthesize meeting-relevant information.

### Core Value Proposition
- **Input**: Meeting context (title, participants, agenda)
- **Process**: Multi-agent AI research pipeline
- **Output**: Comprehensive meeting briefing with attendee profiles, technical context, and actionable insights

### System Capabilities
1. **Calendar Integration**: Google Calendar API integration for meeting data extraction
2. **People Research**: Automated attendee profiling using web research
3. **Technical Context**: GitHub repository analysis, issue tracking, documentation search
4. **Communication Analysis**: Slack/Teams conversation analysis
5. **Intelligent Agenda Building**: AI-powered agenda generation with multiple focus modes
6. **Document Collection**: Pre-read material aggregation
7. **Personalized Briefings**: Role-based context briefings

---

## Architecture & Design Patterns

### 1. Layered Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT LAYER                             │
│  Frontend Applications, API Clients, CLI Tools             │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP/REST API
┌─────────────────────▼───────────────────────────────────────┐
│                  API LAYER (FastAPI)                       │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Routes: health, meetings, agents, technical, agenda    │ │
│  │ Middleware: CORS, Error Handling, Request Validation   │ │
│  └─────────────────────┬───────────────────────────────────┘ │
└────────────────────────┼─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│                  SERVICE LAYER                              │
│  ┌──────────────────┐ ┌─────────────────────┐ ┌─────────────┐ │
│  │ MeetingService   │ │   AgentService      │ │AgendaService│ │
│  │ - Orchestration  │ │ - Agent Execution   │ │- Smart      │ │
│  │ - Job Management │ │ - Individual Agents │ │  Agenda     │ │
│  └──────────────────┘ └─────────────────────┘ └─────────────┘ │
└────────────────────────┼─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│                   AGENTS LAYER                              │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │
│  │ Calendar    │ │ People      │ │ Technical   │ │Coordinator│ │
│  │ Agent       │ │ Research    │ │ Context     │ │ Agent    │ │
│  │             │ │ Agent       │ │ Agent       │ │          │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘ │
│                                                              │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │
│  │ GitHub      │ │ GitHub      │ │ Documentation│ │Tech Stack│ │
│  │ Repository  │ │ Issues      │ │ Agent       │ │ Agent   │ │
│  │ Agent       │ │ Agent       │ │             │ │         │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘ │
└────────────────────────┼─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│                 EXTERNAL TOOLS & APIs                       │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │
│  │ Portia      │ │ Google      │ │ Tavily      │ │Browser  │ │
│  │ Platform    │ │ Calendar    │ │ Search      │ │Base     │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 2. Design Patterns Implemented

#### **Service Pattern**
- **MeetingService**: Orchestrates multi-agent workflows
- **AgentService**: Manages individual agent execution
- **TechnicalAgentService**: Coordinates technical research agents
- **AgendaService**: Handles intelligent agenda generation

#### **Factory Pattern**
- Agent initialization with lazy loading
- Service instantiation with dependency injection

#### **Observer Pattern**
- Job status updates through shared storage
- Real-time progress tracking

#### **Command Pattern**
- Background task execution
- Agent workflow orchestration

#### **Strategy Pattern**
- Multiple preparation workflows (full, custom, agenda-only)
- Different focus modes for agenda generation

---

## Technology Stack

### Core Technologies
- **Python 3.11+**: Primary programming language
- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for FastAPI applications

### AI & LLM Integration
- **Portia**: Primary AI platform for agent orchestration
- **LLM Providers**: Google AI, OpenAI (configurable)
- **Tool Registry**: Open-source tools integration

### External APIs & Services
- **Google Calendar API**: Meeting data extraction
- **GitHub API**: Repository and issue analysis
- **Tavily Search API**: Web research capabilities
- **Slack API**: Communication analysis
- **BrowserBase**: Enhanced web browsing

### Development & Deployment
- **Docker**: Containerization
- **Render**: Cloud deployment platform
- **Environment Variables**: Configuration management

---

## Project Structure

```
smart-meeting-agent/
├── 📱 app/                          # FastAPI Application Package
│   ├── main.py                      # FastAPI app instance & configuration
│   ├── shared.py                    # Global job storage & state management
│   └── v1/                          # API Version 1
│       ├── 📊 models/               # Pydantic Data Models
│       │   ├── meeting_models.py    # Meeting workflow models
│       │   ├── agent_models.py      # Individual agent models
│       │   ├── technical_models.py  # Technical agent models
│       │   └── agenda_models.py     # Agenda builder models
│       ├── 🛣️ routes/               # FastAPI Route Handlers
│       │   ├── health.py            # Health check endpoints
│       │   ├── meetings.py          # Meeting workflow endpoints
│       │   ├── agents.py            # Individual agent endpoints
│       │   ├── technical_agents.py  # Technical analysis endpoints
│       │   ├── agenda_routes.py     # Agenda builder endpoints
│       │   └── auth.py              # Authentication endpoints
│       └── 🔧 services/             # Business Logic Layer
│           ├── meeting_service.py   # Meeting orchestration service
│           ├── agent_service.py     # Agent execution service
│           ├── technical_agent_service.py # Technical analysis service
│           └── agenda_service.py    # Agenda building service
├── 🤖 agents/                       # AI Agent Implementations
│   ├── calendar_agent.py            # Calendar data retrieval
│   ├── people_research_agent.py     # Attendee profiling
│   ├── technical_context_agent.py   # Technical context coordinator
│   ├── slack_agent.py               # Slack communication analysis
│   ├── coordinator_agent.py         # Final briefing synthesis
│   ├── github_repository_agent.py   # GitHub repository search
│   ├── github_issues_agent.py       # GitHub issues analysis
│   ├── documentation_agent.py       # Technical documentation search
│   ├── technology_stack_agent.py    # Technology stack research
│   ├── agenda_builder_agent.py      # Intelligent agenda creation
│   ├── preread_collector_agent.py   # Document collection
│   └── context_briefing_agent.py    # Personalized briefings
├── 🔧 Configuration Files
│   ├── pyproject.toml               # Dependencies & project config
│   ├── Dockerfile                   # Container configuration
│   ├── render.yaml                  # Deployment configuration
│   └── .env                         # Environment variables
└── 🚀 Entry Points
    └── run_api.py                   # Development server launcher
```

---

## Core Components

### 1. FastAPI Application (`app/main.py`)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Environment detection
PORTIA_AVAILABLE = os.getenv("PORTIA_API_KEY") is not None

app = FastAPI(
    title="Smart Meeting Agent",
    description="AI-powered meeting preparation assistant",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route registration
from v1.routes import meetings, health, agents, technical_agents, agenda_routes, auth
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(meetings.router, prefix="/api/v1", tags=["meetings"])
app.include_router(agents.router, prefix="/api/v1", tags=["agents"])
app.include_router(technical_agents.router, prefix="/api/v1", tags=["technical-agents"])
app.include_router(agenda_routes.router, prefix="/api/v1", tags=["agenda-preparation"])
app.include_router(auth.router, prefix="/api/v1", tags=["authentication"])
```

### 2. Shared State Management (`app/shared.py`)

```python
from typing import Dict, Any
from datetime import datetime

# In-memory job storage (replace with database in production)
job_storage: Dict[str, Dict[str, Any]] = {}

# Job structure:
# {
#   "job_id": {
#     "status": "running" | "completed" | "failed" | "started",
#     "created_at": datetime,
#     "updated_at": datetime,
#     "progress": {
#       "current_agent": str,
#       "completed_agents": List[str],
#       "total_agents": int
#     },
#     "results": {
#       "calendar": str,
#       "people_research": str,
#       "technical_context": str,
#       "slack_context": str,
#       "coordinator": str,
#       "final_briefing": str
#     },
#     "error": str (optional)
#   }
# }
```

---

## API Layer

### 1. Health Check Routes (`v1/routes/health.py`)

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    """System health and configuration status."""
    return {
        "status": "healthy",
        "portia_available": PORTIA_AVAILABLE,
        "environment": os.getenv("ENVIRONMENT", "development"),
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }
```

**Frontend Usage**:
```typescript
const health = await fetch('/api/v1/health').then(r => r.json());
if (health.status === 'healthy') {
  // System is operational
}
```

### 2. Meeting Workflow Routes (`v1/routes/meetings.py`)

#### **POST /api/v1/meetings/prepare**
Starts full meeting preparation workflow with all agents.

```python
@router.post("/meetings/prepare", response_model=JobResponse)
async def prepare_meeting(
    request: MeetingPrepRequest,
    background_tasks: BackgroundTasks
):
    """Start meeting preparation with full agent workflow."""
    job_id = str(uuid.uuid4())
    
    background_tasks.add_task(
        meeting_service.run_full_preparation,
        job_id,
        request
    )
    
    return JobResponse(
        job_id=job_id,
        status="started",
        message="Meeting preparation started"
    )
```

**Request Model**:
```python
class MeetingPrepRequest(BaseModel):
    meeting_context: Optional[str] = None
    include_slack: bool = True
    include_agenda: bool = False
    focus_mode: str = "balanced"
    user_preferences: Dict[str, Any] = Field(default_factory=dict)
```

**Frontend Usage**:
```typescript
const response = await fetch('/api/v1/meetings/prepare', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    meeting_context: "Weekly team standup",
    include_slack: true,
    include_agenda: false
  })
});
const { job_id } = await response.json();
```

#### **POST /api/v1/meetings/prepare-custom**
Starts custom preparation with selected agents only.

```python
@router.post("/meetings/prepare-custom", response_model=JobResponse)
async def prepare_meeting_custom(
    request: CustomMeetingPrepRequest,
    background_tasks: BackgroundTasks
):
    """Start custom meeting preparation with selected agents."""
    job_id = str(uuid.uuid4())
    
    background_tasks.add_task(
        meeting_service.run_custom_preparation,
        job_id,
        request
    )
    
    return JobResponse(
        job_id=job_id,
        status="started",
        message="Custom meeting preparation started"
    )
```

**Request Model**:
```python
class CustomMeetingPrepRequest(BaseModel):
    agents: List[str] = Field(..., description="List of agents to run")
    meeting_context: Optional[str] = None
    calendar_data: Optional[Dict[str, Any]] = None
    people_data: Optional[Dict[str, Any]] = None
    technical_data: Optional[Dict[str, Any]] = None
    slack_data: Optional[Dict[str, Any]] = None
```

**Available Agents**:
- `calendar`: Calendar data extraction
- `people_research`: Attendee profiling
- `technical_context`: Technical research
- `slack_context`: Communication analysis
- `coordinator`: Final briefing synthesis

#### **POST /api/v1/meetings/prepare-agenda**
Starts agenda-focused preparation workflow.

```python
@router.post("/meetings/prepare-agenda", response_model=JobResponse)
async def prepare_meeting_agenda(
    meeting_context: Dict[str, Any],
    focus_mode: str = "balanced",
    participant_roles: Dict[str, str] = None,
    background_tasks: BackgroundTasks = None
):
    """Start comprehensive agenda preparation workflow."""
    job_id = str(uuid.uuid4())
    
    background_tasks.add_task(
        meeting_service.run_comprehensive_agenda_preparation,
        job_id,
        meeting_context,
        focus_mode,
        participant_roles
    )
    
    return JobResponse(
        job_id=job_id,
        status="started",
        message="Agenda preparation started"
    )
```

**Focus Modes**:
- `balanced`: Equal coverage of all topics
- `blockers`: Focus on current blockers and urgent decisions
- `design`: Emphasize design updates and creative discussions
- `progress`: Highlight progress updates and milestone reviews
- `planning`: Concentrate on future planning and strategy

#### **GET /api/v1/meetings/jobs/{job_id}**
Retrieves job status and results.

```python
@router.get("/meetings/jobs/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    """Get the status and results of a meeting preparation job."""
    return meeting_service.get_job_status(job_id)
```

**Response Model**:
```python
class JobStatusResponse(BaseModel):
    job_id: str
    status: str  # "started", "running", "completed", "failed"
    created_at: datetime
    updated_at: datetime
    progress: Optional[Dict[str, Any]] = None
    results: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
```

**Frontend Usage for Real-time Updates**:
```typescript
const pollJobStatus = async (jobId: string) => {
  const response = await fetch(`/api/v1/meetings/jobs/${jobId}`);
  const job = await response.json();
  
  if (job.status === 'running') {
    // Show progress: job.progress.completed_agents.length / job.progress.total_agents
    setTimeout(() => pollJobStatus(jobId), 2000); // Poll every 2 seconds
  } else if (job.status === 'completed') {
    // Show final results: job.results.final_briefing
  } else if (job.status === 'failed') {
    // Show error: job.error
  }
};
```

#### **GET /api/v1/meetings/jobs**
Retrieves all jobs for dashboard view.

```python
@router.get("/meetings/jobs")
async def get_all_jobs():
    """Get all jobs for dashboard view."""
    return meeting_service.get_all_jobs()
```

#### **DELETE /api/v1/meetings/jobs/{job_id}**
Deletes a specific job.

```python
@router.delete("/meetings/jobs/{job_id}")
async def delete_job(job_id: str):
    """Delete a specific job."""
    from shared import job_storage
    if job_id in job_storage:
        del job_storage[job_id]
        return {"message": "Job deleted successfully"}
    raise HTTPException(status_code=404, detail="Job not found")
```

### 3. Individual Agent Routes (`v1/routes/agents.py`)

These endpoints allow running individual agents directly:

#### **POST /api/v1/agents/calendar**
```python
@router.post("/agents/calendar", response_model=AgentResponse)
async def run_calendar_agent(request: CalendarRequest):
    """Execute calendar agent to fetch meeting and calendar data."""
    result = await agent_service.run_calendar_agent(request)
    return AgentResponse(
        agent="calendar",
        status="success",
        data=result
    )
```

#### **POST /api/v1/agents/people-research**
```python
@router.post("/agents/people-research", response_model=AgentResponse)
async def run_people_research_agent(request: PeopleResearchRequest):
    """Execute people research agent to gather attendee information."""
    result = await agent_service.run_people_research_agent(request)
    return AgentResponse(
        agent="people_research",
        status="success",
        data=result
    )
```

#### **POST /api/v1/agents/technical-context**
```python
@router.post("/agents/technical-context", response_model=AgentResponse)
async def run_technical_context_agent(request: TechnicalContextRequest):
    """Execute technical context agent to gather relevant technical information."""
    result = await agent_service.run_technical_context_agent(request)
    return AgentResponse(
        agent="technical_context",
        status="success",
        data=result
    )
```

#### **POST /api/v1/agents/slack-context**
```python
@router.post("/agents/slack-context", response_model=AgentResponse)
async def run_slack_context_agent(request: SlackContextRequest):
    """Execute Slack context agent to gather relevant team communications."""
    result = await agent_service.run_slack_context_agent(request)
    return AgentResponse(
        agent="slack_context",
        status="success",
        data=result
    )
```

#### **POST /api/v1/agents/coordinator**
```python
@router.post("/agents/coordinator", response_model=AgentResponse)
async def run_coordinator_agent(request: CoordinatorRequest):
    """Execute coordinator agent to compile and organize all information."""
    result = await agent_service.run_coordinator_agent(request)
    return AgentResponse(
        agent="coordinator",
        status="success",
        data=result
    )
```

### 4. Technical Analysis Routes (`v1/routes/technical_agents.py`)

Specialized technical research endpoints:

#### **POST /api/v1/technical/github/repositories**
```python
@router.post("/technical/github/repositories", response_model=TechnicalAgentResponse)
async def search_github_repositories(request: GitHubRepositoryRequest):
    """Search for relevant GitHub repositories."""
    service = get_technical_service()
    result = await service.search_repositories(request)
    return TechnicalAgentResponse(
        agent_type="github_repository",
        status="success",
        data=result
    )
```

#### **POST /api/v1/technical/github/issues**
```python
@router.post("/technical/github/issues", response_model=TechnicalAgentResponse)
async def analyze_github_issues(request: GitHubIssuesRequest):
    """Analyze GitHub issues and development activity."""
    service = get_technical_service()
    result = await service.analyze_issues(request)
    return TechnicalAgentResponse(
        agent_type="github_issues",
        status="success",
        data=result
    )
```

#### **POST /api/v1/technical/documentation**
```python
@router.post("/technical/documentation", response_model=TechnicalAgentResponse)
async def search_documentation(request: DocumentationRequest):
    """Search for relevant technical documentation."""
    service = get_technical_service()
    result = await service.search_documentation(request)
    return TechnicalAgentResponse(
        agent_type="documentation",
        status="success",
        data=result
    )
```

#### **POST /api/v1/technical/technology-stack**
```python
@router.post("/technical/technology-stack", response_model=TechnicalAgentResponse)
async def analyze_technology_stack(request: TechnologyStackRequest):
    """Analyze technology stack and frameworks."""
    service = get_technical_service()
    result = await service.analyze_tech_stack(request)
    return TechnicalAgentResponse(
        agent_type="technology_stack",
        status="success",
        data=result
    )
```

#### **POST /api/v1/technical/comprehensive**
```python
@router.post("/technical/comprehensive", response_model=TechnicalAgentResponse)
async def comprehensive_technical_analysis(request: TechnicalContextRequest):
    """Run comprehensive technical analysis using all sub-agents."""
    service = get_technical_service()
    result = await service.comprehensive_analysis(request)
    return TechnicalAgentResponse(
        agent_type="technical_context_comprehensive",
        status="success",
        data=result
    )
```

### 5. Agenda Builder Routes (`v1/routes/agenda_routes.py`)

Intelligent agenda generation endpoints:

#### **POST /api/v1/agenda/build**
```python
@router.post("/agenda/build", response_model=Dict[str, Any])
async def build_intelligent_agenda(request: AgendaBuilderRequest):
    """Build an AI-powered agenda based on meeting context."""
    service = get_agenda_service()
    result = await service.build_agenda(request)
    return {
        "agent_type": "agenda_builder",
        "status": "success",
        "data": result
    }
```

#### **POST /api/v1/agenda/preread**
```python
@router.post("/agenda/preread", response_model=Dict[str, Any])
async def collect_preread_documents(request: PreReadCollectorRequest):
    """Collect relevant pre-read documents for meeting preparation."""
    service = get_agenda_service()
    result = await service.collect_preread_documents(request)
    return {
        "agent_type": "preread_collector",
        "status": "success",
        "data": result
    }
```

#### **POST /api/v1/agenda/briefing**
```python
@router.post("/agenda/briefing", response_model=Dict[str, Any])
async def generate_context_briefing(request: ContextBriefingRequest):
    """Generate personalized context briefings for meeting participants."""
    service = get_agenda_service()
    result = await service.generate_context_briefing(request)
    return {
        "agent_type": "context_briefing",
        "status": "success",
        "data": result
    }
```

#### **POST /api/v1/agenda/comprehensive**
```python
@router.post("/agenda/comprehensive", response_model=Dict[str, Any])
async def comprehensive_agenda_preparation(
    meeting_context: Dict[str, Any],
    focus_mode: str = "balanced",
    participant_roles: Dict[str, str] = None
):
    """Run comprehensive agenda preparation including all components."""
    service = get_agenda_service()
    
    # Build agenda
    agenda_request = AgendaBuilderRequest(
        meeting_context=meeting_context,
        focus_mode=focus_mode
    )
    agenda_result = await service.build_agenda(agenda_request)
    
    # Collect pre-read documents
    preread_request = PreReadCollectorRequest(
        meeting_context=meeting_context
    )
    preread_result = await service.collect_preread_documents(preread_request)
    
    # Generate context briefings if roles provided
    briefing_result = None
    if participant_roles:
        briefing_request = ContextBriefingRequest(
            meeting_data=meeting_context,
            participant_roles=participant_roles
        )
        briefing_result = await service.generate_context_briefing(briefing_request)
    
    return {
        "agent_type": "comprehensive_agenda",
        "status": "success",
        "data": {
            "agenda": agenda_result,
            "preread_documents": preread_result,
            "context_briefings": briefing_result,
            "meeting_context": meeting_context
        }
    }
```

#### **POST /api/v1/agenda/quick/{focus_mode}**
```python
@router.post("/agenda/quick/{focus_mode}")
async def quick_agenda_generation(
    focus_mode: str,
    meeting_context: Dict[str, Any]
):
    """Quick agenda generation with specific focus mode."""
    if focus_mode not in ["blockers", "design", "progress", "planning", "balanced"]:
        raise HTTPException(status_code=400, detail="Invalid focus mode")
    
    service = get_agenda_service()
    
    agenda_request = AgendaBuilderRequest(
        meeting_context=meeting_context,
        focus_mode=focus_mode
    )
    result = await service.build_agenda(agenda_request)
    
    return {
        "agent_type": "quick_agenda",
        "focus_mode": focus_mode,
        "status": "success",
        "data": result
    }
```

### 6. Authentication Routes (`v1/routes/auth.py`)

OAuth integration for external services:

#### **GET /api/v1/auth/oauth-url**
```python
@router.get("/auth/oauth-url")
async def get_oauth_url():
    """Get OAuth URL for Google Calendar authentication."""
    result = meeting_service.get_oauth_url()
    return result
```

#### **POST /api/v1/auth/oauth-callback**
```python
@router.post("/auth/oauth-callback")
async def oauth_callback(
    code: str = Query(..., description="Authorization code from OAuth provider"),
    state: str = Query(..., description="State parameter from OAuth flow")
):
    """Handle OAuth callback and complete authentication."""
    result = await meeting_service.handle_oauth_callback(code, state)
    return result
```

---

## Service Layer

### 1. Meeting Service (`v1/services/meeting_service.py`)

The core orchestration service that manages multi-agent workflows.

```python
class MeetingService:
    """Service for handling meeting preparation workflows."""
    
    def __init__(self):
        self.agent_service = AgentService()
        # Initialize agenda service if available
        try:
            from .agenda_service import AgendaService
            self.agenda_service = AgendaService()
            self.has_agenda_service = True
        except ImportError:
            self.agenda_service = None
            self.has_agenda_service = False
```

#### **Full Preparation Workflow**
```python
async def run_full_preparation(self, job_id: str, request: MeetingPrepRequest):
    """Run the complete multi-agent meeting preparation workflow."""
    job_storage[job_id] = {
        "status": "running",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "progress": {"current_agent": "calendar", "completed_agents": [], "total_agents": 5},
        "results": {}
    }
    
    try:
        # Step 1: Calendar Agent
        calendar_result = await self.agent_service.run_calendar_agent_internal()
        job_storage[job_id]["progress"]["completed_agents"].append("calendar")
        job_storage[job_id]["results"]["calendar"] = calendar_result
        job_storage[job_id]["progress"]["current_agent"] = "people_research"
        job_storage[job_id]["updated_at"] = datetime.utcnow()
        
        # Step 2: People Research Agent
        people_result = await self.agent_service.run_people_research_agent_internal(calendar_result)
        job_storage[job_id]["progress"]["completed_agents"].append("people_research")
        job_storage[job_id]["results"]["people_research"] = people_result
        job_storage[job_id]["progress"]["current_agent"] = "technical_context"
        job_storage[job_id]["updated_at"] = datetime.utcnow()
        
        # Step 3: Technical Context Agent
        technical_result = await self.agent_service.run_technical_context_agent_internal(calendar_result)
        job_storage[job_id]["progress"]["completed_agents"].append("technical_context")
        job_storage[job_id]["results"]["technical_context"] = technical_result
        job_storage[job_id]["progress"]["current_agent"] = "slack_context"
        job_storage[job_id]["updated_at"] = datetime.utcnow()
        
        # Step 4: Slack Context Agent (if enabled)
        slack_result = ""
        if request.include_slack:
            slack_result = await self.agent_service.run_slack_context_agent_internal(calendar_result, people_result)
            job_storage[job_id]["progress"]["completed_agents"].append("slack_context")
            job_storage[job_id]["results"]["slack_context"] = slack_result

        # Step 5: Optional Agenda Generation
        agenda_result = None
        if getattr(request, 'include_agenda', False) and self.has_agenda_service:
            job_storage[job_id]["progress"]["current_agent"] = "agenda_builder"
            job_storage[job_id]["updated_at"] = datetime.utcnow()
            
            # Build meeting context from gathered data
            meeting_context = {
                "meeting_title": self._extract_meeting_title(calendar_result),
                "participants": self._extract_participants(people_result),
                "calendar_data": calendar_result,
                "people_data": people_result,
                "technical_data": technical_result,
                "slack_data": slack_result
            }
            
            from ..models.agenda_models import AgendaBuilderRequest
            agenda_request = AgendaBuilderRequest(
                meeting_context=meeting_context,
                focus_mode=getattr(request, 'focus_mode', 'balanced')
            )
            
            agenda_result = await self.agenda_service.build_agenda(agenda_request)
            job_storage[job_id]["progress"]["completed_agents"].append("agenda_builder")
            job_storage[job_id]["results"]["agenda"] = agenda_result

        job_storage[job_id]["progress"]["current_agent"] = "coordinator"
        job_storage[job_id]["updated_at"] = datetime.utcnow()
        
        # Step 6: Coordinator Agent
        final_briefing = await self.agent_service.run_coordinator_agent_internal(
            calendar_result, people_result, technical_result, slack_result
        )
        job_storage[job_id]["progress"]["completed_agents"].append("coordinator")
        job_storage[job_id]["results"]["coordinator"] = final_briefing
        job_storage[job_id]["results"]["final_briefing"] = final_briefing
        
        # Mark as completed
        job_storage[job_id]["status"] = "completed"
        job_storage[job_id]["progress"]["current_agent"] = None
        job_storage[job_id]["updated_at"] = datetime.utcnow()
        
    except Exception as e:
        job_storage[job_id]["status"] = "failed"
        job_storage[job_id]["error"] = str(e)
        job_storage[job_id]["updated_at"] = datetime.utcnow()
```

#### **Custom Preparation Workflow**
```python
async def run_custom_preparation(self, job_id: str, request: CustomMeetingPrepRequest):
    """Run custom meeting preparation with selected agents."""
    job_storage[job_id] = {
        "status": "running",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "progress": {"current_agent": None, "completed_agents": [], "requested_agents": request.agents, "total_agents": len(request.agents)},
        "results": {}
    }
    
    try:
        results = {}
        
        # Use provided data or initialize
        calendar_data = request.calendar_data
        people_data = request.people_data
        technical_data = request.technical_data
        slack_data = request.slack_data
        
        for agent_name in request.agents:
            job_storage[job_id]["progress"]["current_agent"] = agent_name
            job_storage[job_id]["updated_at"] = datetime.utcnow()
            
            if agent_name == "calendar":
                calendar_data = await self.agent_service.run_calendar_agent_internal()
                results["calendar"] = calendar_data
                
            elif agent_name == "people_research":
                people_data = await self.agent_service.run_people_research_agent_internal(calendar_data or "")
                results["people_research"] = people_data
                
            elif agent_name == "technical_context":
                technical_data = await self.agent_service.run_technical_context_agent_internal(calendar_data or "")
                results["technical_context"] = technical_data
                
            elif agent_name == "slack_context":
                slack_data = await self.agent_service.run_slack_context_agent_internal(calendar_data or "", people_data or "")
                results["slack_context"] = slack_data
                
            elif agent_name == "coordinator":
                final_briefing = await self.agent_service.run_coordinator_agent_internal(
                    calendar_data or "", people_data or "", technical_data or "", slack_data or ""
                )
                results["coordinator"] = final_briefing
                results["final_briefing"] = final_briefing
            
            job_storage[job_id]["progress"]["completed_agents"].append(agent_name)
            job_storage[job_id]["results"] = results
            job_storage[job_id]["updated_at"] = datetime.utcnow()
        
        job_storage[job_id]["status"] = "completed"
        job_storage[job_id]["progress"]["current_agent"] = None
        job_storage[job_id]["updated_at"] = datetime.utcnow()
        
    except Exception as e:
        job_storage[job_id]["status"] = "failed"
        job_storage[job_id]["error"] = str(e)
        job_storage[job_id]["updated_at"] = datetime.utcnow()
```

#### **Agenda Preparation Workflow**
```python
async def run_comprehensive_agenda_preparation(self, job_id: str, meeting_context: Dict[str, Any], focus_mode: str = "balanced", participant_roles: Dict[str, str] = None):
    """Run comprehensive agenda preparation workflow."""
    job_storage[job_id] = {
        "status": "running",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "progress": {"current_agent": "agenda_builder", "completed_agents": [], "total_agents": 3},
        "results": {}
    }
    
    if not self.has_agenda_service:
        job_storage[job_id]["status"] = "failed"
        job_storage[job_id]["error"] = "Agenda service not available"
        return
    
    try:
        # Step 1: Build Agenda
        from ..models.agenda_models import AgendaBuilderRequest
        agenda_request = AgendaBuilderRequest(
            meeting_context=meeting_context,
            focus_mode=focus_mode
        )
        agenda_result = await self.agenda_service.build_agenda(agenda_request)
        job_storage[job_id]["progress"]["completed_agents"].append("agenda_builder")
        job_storage[job_id]["results"]["agenda"] = agenda_result
        job_storage[job_id]["progress"]["current_agent"] = "preread_collector"
        job_storage[job_id]["updated_at"] = datetime.utcnow()
        
        # Step 2: Collect Pre-read Documents
        from ..models.agenda_models import PreReadCollectorRequest
        preread_request = PreReadCollectorRequest(meeting_context=meeting_context)
        preread_result = await self.agenda_service.collect_preread_documents(preread_request)
        job_storage[job_id]["progress"]["completed_agents"].append("preread_collector")
        job_storage[job_id]["results"]["preread_documents"] = preread_result
        job_storage[job_id]["progress"]["current_agent"] = "context_briefing"
        job_storage[job_id]["updated_at"] = datetime.utcnow()
        
        # Step 3: Generate Context Briefings (if roles provided)
        briefing_result = None
        if participant_roles:
            from ..models.agenda_models import ContextBriefingRequest
            briefing_request = ContextBriefingRequest(
                meeting_data=meeting_context,
                participant_roles=participant_roles
            )
            briefing_result = await self.agenda_service.generate_context_briefing(briefing_request)
            job_storage[job_id]["results"]["context_briefings"] = briefing_result
        
        job_storage[job_id]["progress"]["completed_agents"].append("context_briefing")
        job_storage[job_id]["status"] = "completed"
        job_storage[job_id]["progress"]["current_agent"] = None
        job_storage[job_id]["updated_at"] = datetime.utcnow()
        
    except Exception as e:
        job_storage[job_id]["status"] = "failed"
        job_storage[job_id]["error"] = str(e)
        job_storage[job_id]["updated_at"] = datetime.utcnow()
```

#### **Job Management Methods**
```python
def get_job_status(self, job_id: str) -> JobStatusResponse:
    """Get the status and results of a job."""
    if job_id not in job_storage:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job_data = job_storage[job_id]
    return JobStatusResponse(
        job_id=job_id,
        status=job_data["status"],
        created_at=job_data["created_at"],
        updated_at=job_data["updated_at"],
        progress=job_data.get("progress"),
        results=job_data.get("results"),
        error=job_data.get("error")
    )

def get_all_jobs(self) -> Dict[str, Any]:
    """Get all jobs for dashboard view."""
    return {
        job_id: {
            "job_id": job_id,
            "status": job_data["status"],
            "created_at": job_data["created_at"],
            "updated_at": job_data["updated_at"],
            "progress": job_data.get("progress", {}),
            "type": self._determine_job_type(job_data)
        }
        for job_id, job_data in job_storage.items()
    }
```

#### **Utility Methods**
```python
def _extract_meeting_title(self, calendar_data: str) -> str:
    """Extract meeting title from calendar data."""
    lines = calendar_data.split('\n')
    for line in lines:
        if 'Title:' in line:
            return line.split('Title:')[1].strip()
    return "Meeting"

def _extract_participants(self, people_data: str) -> list:
    """Extract participants from people data."""
    participants = []
    lines = people_data.split('\n')
    for line in lines:
        if '@' in line and 'gmail.com' in line:
            import re
            emails = re.findall(r'\S+@\S+', line)
            participants.extend(emails)
    return list(set(participants))

def _determine_job_type(self, job_data: Dict[str, Any]) -> str:
    """Determine job type based on job data."""
    progress = job_data.get("progress", {})
    if "requested_agents" in progress:
        return "custom"
    elif "agenda" in job_data.get("results", {}):
        return "agenda"
    else:
        return "full"
```

#### **OAuth Methods**
```python
async def handle_oauth_callback(self, auth_code: str, state: str) -> Dict[str, Any]:
    """Handle OAuth callback from frontend."""
    try:
        # Process OAuth with Portia/Google Calendar
        # This is where you'd integrate with Portia's OAuth flow
        return {
            "status": "success",
            "message": "Authentication successful",
            "access_token": "mock_token_123"  # In real implementation, return actual token
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Authentication failed: {str(e)}"
        }

def get_oauth_url(self) -> Dict[str, Any]:
    """Get OAuth URL for frontend to redirect user."""
    # In real implementation, this would generate the actual OAuth URL
    return {
        "oauth_url": "https://accounts.google.com/oauth/authorize?client_id=your_client_id&redirect_uri=http://localhost:3000/auth/callback&scope=https://www.googleapis.com/auth/calendar.readonly&response_type=code&state=random_state",
        "state": "random_state_123"
    }
```

### 2. Agent Service (`v1/services/agent_service.py`)

Manages individual agent execution and coordination.

```python
class AgentService:
    """Service for handling individual agent executions."""
    
    def __init__(self):
        self.config = None
        self.tools = []
        self._agents_initialized = False
        
        # Initialize agents as None - will be created when needed
        self.calendar_agent = None
        self.people_agent = None
        self.technical_agent = None
        self.slack_agent = None
        self.coordinator_agent = None
```

#### **Agent Initialization**
```python
def _initialize_agents(self):
    """Initialize agents lazily when first needed."""
    if self._agents_initialized:
        return
        
    print("🤖 Initializing AI agents...")
    
    # Try to get proper Portia configuration
    self.config = get_config()
    
    if self.config and PORTIA_AVAILABLE:
        print("✅ Using Portia configuration")
        try:
            self.tools = PortiaToolRegistry(self.config) + open_source_tool_registry
            
            # Import and initialize agents with proper config
            from agents import (
                CalendarAgent,
                EnhancedPeopleResearchAgent as PeopleResearchAgent,
                TechnicalContextAgent,
                SlackAgent,
                CoordinatorAgent
            )
            
            self.calendar_agent = CalendarAgent(self.config, self.tools)
            self.people_agent = PeopleResearchAgent(self.config, self.tools)
            self.technical_agent = TechnicalContextAgent(self.config, self.tools)
            self.slack_agent = SlackAgent(self.config, self.tools)
            self.coordinator_agent = CoordinatorAgent(self.config, self.tools)
            
            print("✅ All agents initialized with Portia")
        except Exception as e:
            print(f"⚠️ Failed to initialize agents with Portia: {e}")
            self._initialize_mock_agents()
    else:
        print("🔄 Using mock agents (Portia not available)")
        self._initialize_mock_agents()
    
    self._agents_initialized = True

def _initialize_mock_agents(self):
    """Initialize mock agents for testing."""
    from agents.calendar_agent import MockCalendarAgent
    from agents.people_research_agent import MockPeopleResearchAgent
    from agents.technical_context_agent import MockTechnicalContextAgent
    from agents.slack_agent import MockSlackAgent
    from agents.coordinator_agent import SimpleCoordinatorAgent
    
    self.calendar_agent = MockCalendarAgent()
    self.people_agent = MockPeopleResearchAgent()
    self.technical_agent = MockTechnicalContextAgent()
    self.slack_agent = MockSlackAgent()
    self.coordinator_agent = SimpleCoordinatorAgent(None, [])
```

#### **Agent Execution Methods**
```python
async def run_calendar_agent(self, request: CalendarRequest) -> Dict[str, Any]:
    """Execute calendar agent."""
    self._initialize_agents()
    start_time = datetime.utcnow()
    
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, self.calendar_agent.execute)
    
    execution_time = (datetime.utcnow() - start_time).total_seconds()
    
    return {
        "output": result,
        "execution_time": execution_time,
        "agent": "calendar",
        "request_params": request.dict() if request else {}
    }

async def run_people_research_agent(self, request: PeopleResearchRequest) -> Dict[str, Any]:
    """Execute people research agent."""
    self._initialize_agents()
    start_time = datetime.utcnow()
    
    calendar_context = request.calendar_context.get("output", "") if request.calendar_context else ""
    
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, self.people_agent.execute, calendar_context)
    
    execution_time = (datetime.utcnow() - start_time).total_seconds()
    
    return {
        "output": result,
        "execution_time": execution_time,
        "agent": "people_research",
        "request_params": request.dict()
    }

async def run_technical_context_agent(self, request: TechnicalContextRequest) -> Dict[str, Any]:
    """Execute technical context agent."""
    self._initialize_agents()
    start_time = datetime.utcnow()
    
    calendar_context = request.calendar_context.get("output", "") if request.calendar_context else ""
    
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, self.technical_agent.execute, calendar_context)
    
    execution_time = (datetime.utcnow() - start_time).total_seconds()
    
    return {
        "output": result,
        "execution_time": execution_time,
        "agent": "technical_context",
        "request_params": request.dict()
    }

async def run_slack_context_agent(self, request: SlackContextRequest) -> Dict[str, Any]:
    """Execute Slack context agent."""
    self._initialize_agents()
    start_time = datetime.utcnow()
    
    calendar_context = request.calendar_context.get("output", "") if request.calendar_context else ""
    people_context = request.people_context.get("output", "") if request.people_context else ""
    
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, self.slack_agent.execute, calendar_context, people_context)
    
    execution_time = (datetime.utcnow() - start_time).total_seconds()
    
    return {
        "output": result,
        "execution_time": execution_time,
        "agent": "slack_context",
        "request_params": request.dict()
    }

async def run_coordinator_agent(self, request: CoordinatorRequest) -> Dict[str, Any]:
    """Execute coordinator agent."""
    self._initialize_agents()
    start_time = datetime.utcnow()
    
    # Extract data from request
    calendar_data = request.calendar_data.get("output", "") if request.calendar_data else ""
    people_data = request.people_data.get("output", "") if request.people_data else ""
    technical_data = request.technical_data.get("output", "") if request.technical_data else ""
    slack_data = request.slack_data.get("output", "") if request.slack_data else ""
    
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None, 
        self.coordinator_agent.execute, 
        calendar_data, 
        people_data, 
        technical_data, 
        slack_data
    )
    
    execution_time = (datetime.utcnow() - start_time).total_seconds()
    
    return {
        "output": result,
        "execution_time": execution_time,
        "agent": "coordinator",
        "request_params": request.dict()
    }
```

#### **Internal Methods for Service Communication**
```python
async def run_calendar_agent_internal(self):
    """Internal method for service-to-service communication."""
    self._initialize_agents()
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, self.calendar_agent.execute)

async def run_people_research_agent_internal(self, calendar_data):
    """Internal method for service-to-service communication."""
    self._initialize_agents()
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, self.people_agent.execute, calendar_data)

async def run_technical_context_agent_internal(self, calendar_data):
    """Internal method for service-to-service communication."""
    self._initialize_agents()
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, self.technical_agent.execute, calendar_data)

async def run_slack_context_agent_internal(self, calendar_data, people_data):
    """Internal method for service-to-service communication."""
    self._initialize_agents()
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, self.slack_agent.execute, calendar_data, people_data)

async def run_coordinator_agent_internal(self, calendar_data, people_data, technical_data, slack_data):
    """Internal method for service-to-service communication."""
    self._initialize_agents()
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, self.coordinator_agent.execute, calendar_data, people_data, technical_data, slack_data)
```

### 3. Technical Agent Service (`v1/services/technical_agent_service.py`)

Specialized service for technical research coordination.

```python
class TechnicalAgentService:
    """Service for handling technical research agents with lazy initialization."""
    
    def __init__(self):
        self.config = None
        self.tools = []
        self._agents_initialized = False
        
        # Initialize agents as None - will be created when needed
        self.github_repo_agent = None
        self.github_issues_agent = None
        self.documentation_agent = None
        self.technology_stack_agent = None
```

#### **Technical Agent Methods**
```python
async def search_repositories(self, request: GitHubRepositoryRequest) -> Dict[str, Any]:
    """Search for GitHub repositories."""
    self._initialize_agents()
    start_time = datetime.utcnow()
    
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None, 
        self.github_repo_agent.execute, 
        request.search_terms, 
        request.limit
    )
    
    execution_time = (datetime.utcnow() - start_time).total_seconds()
    
    return {
        "output": result,
        "execution_time": execution_time,
        "agent": "github_repository",
        "search_terms": request.search_terms,
        "limit": request.limit
    }

async def analyze_issues(self, request: GitHubIssuesRequest) -> Dict[str, Any]:
    """Analyze GitHub issues and development activity."""
    self._initialize_agents()
    start_time = datetime.utcnow()
    
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None, 
        self.github_issues_agent.execute, 
        request.repository_info, 
        request.search_terms
    )
    
    execution_time = (datetime.utcnow() - start_time).total_seconds()
    
    return {
        "output": result,
        "execution_time": execution_time,
        "agent": "github_issues",
        "repository_info": request.repository_info,
        "search_terms": request.search_terms
    }

async def search_documentation(self, request: DocumentationRequest) -> Dict[str, Any]:
    """Search for technical documentation."""
    self._initialize_agents()
    start_time = datetime.utcnow()
    
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None, 
        self.documentation_agent.execute, 
        request.search_terms, 
        request.doc_types
    )
    
    execution_time = (datetime.utcnow() - start_time).total_seconds()
    
    return {
        "output": result,
        "execution_time": execution_time,
        "agent": "documentation",
        "search_terms": request.search_terms,
        "doc_types": request.doc_types
    }

async def analyze_tech_stack(self, request: TechnologyStackRequest) -> Dict[str, Any]:
    """Analyze technology stack."""
    self._initialize_agents()
    start_time = datetime.utcnow()
    
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None, 
        self.technology_stack_agent.execute, 
        request.repository_info
    )
    
    execution_time = (datetime.utcnow() - start_time).total_seconds()
    
    return {
        "output": result,
        "execution_time": execution_time,
        "agent": "technology_stack",
        "repository_info": request.repository_info
    }

async def comprehensive_analysis(self, request: TechnicalContextRequest) -> Dict[str, Any]:
    """Run comprehensive technical analysis."""
    self._initialize_agents()
    start_time = datetime.utcnow()
    
    results = {}
    
    try:
        # Extract search terms from calendar context
        search_terms = self._extract_search_terms(request.calendar_context)
        
        # Run all sub-agents if requested
        if request.include_github:
            # Repository search
            repo_result = await self.search_repositories(GitHubRepositoryRequest(
                search_terms=search_terms,
                limit=5
            ))
            results["repositories"] = repo_result
            
            # Issues analysis
            issues_result = await self.analyze_issues(GitHubIssuesRequest(
                repository_info=repo_result["output"],
                search_terms=search_terms
            ))
            results["issues"] = issues_result
        
        if request.include_docs:
            # Documentation search
            docs_result = await self.search_documentation(DocumentationRequest(
                search_terms=search_terms,
                doc_types=["API", "Tutorial", "Guide"]
            ))
            results["documentation"] = docs_result
        
        if request.include_tech_stack:
            # Technology stack analysis
            tech_result = await self.analyze_tech_stack(TechnologyStackRequest(
                repository_info=results.get("repositories", {}).get("output", search_terms)
            ))
            results["technology_stack"] = tech_result
        
        # Combine all results
        combined_output = self._combine_results(results)
        
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        return {
            "output": combined_output,
            "execution_time": execution_time,
            "agent": "technical_context_comprehensive",
            "sub_results": results,
            "request_params": request.dict()
        }
        
    except Exception as e:
        return {
            "output": f"Technical analysis failed: {str(e)}",
            "execution_time": (datetime.utcnow() - start_time).total_seconds(),
            "agent": "technical_context_comprehensive",
            "error": str(e)
        }
```

#### **Utility Methods**
```python
def _extract_search_terms(self, calendar_context: str) -> str:
    """Extract relevant search terms from calendar context."""
    # Simple keyword extraction - can be enhanced with NLP
    terms = []
    calendar_lower = calendar_context.lower()
    
    if "workflow" in calendar_lower:
        terms.append("workflow")
    if "gsoc" in calendar_lower:
        terms.append("google summer of code")
    if "business4s" in calendar_lower:
        terms.append("business4s")
    if "scala" in calendar_lower:
        terms.append("scala")
    
    return " ".join(terms) if terms else "workflow orchestration"

def _combine_results(self, results):
    """Combine results from all sub-agents."""
    combined = "# Comprehensive Technical Analysis\n\n"
    
    if "repositories" in results:
        combined += "## Repository Analysis\n"
        combined += results["repositories"]["output"] + "\n\n"
    
    if "issues" in results:
        combined += "## Development Activity\n"
        combined += results["issues"]["output"] + "\n\n"
    
    if "documentation" in results:
        combined += "## Documentation\n"
        combined += results["documentation"]["output"] + "\n\n"
    
    if "technology_stack" in results:
        combined += "## Technology Stack\n"
        combined += results["technology_stack"]["output"] + "\n\n"
    
    return combined
```

### 4. Agenda Service (`v1/services/agenda_service.py`)

Manages intelligent agenda generation and meeting preparation.

```python
class AgendaService:
    """Service for handling intelligent agenda and meeting preparation."""
    
    def __init__(self):
        self.config = None
        self.tools = []
        self._agents_initialized = False
        
        # Initialize agents as None - will be created when needed
        self.agenda_builder = None
        self.preread_collector = None
        self.context_briefing = None
```

#### **Agenda Building Methods**
```python
async def build_agenda(self, request: AgendaBuilderRequest) -> Dict[str, Any]:
    """Build intelligent agenda based on meeting context."""
    self._initialize_agents()
    start_time = datetime.utcnow()
    
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None, 
        self.agenda_builder.execute, 
        request.meeting_context, 
        request.focus_mode
    )
    
    execution_time = (datetime.utcnow() - start_time).total_seconds()
    
    return {
        "agenda": result,
        "execution_time": execution_time,
        "focus_mode": request.focus_mode,
        "meeting_context": request.meeting_context
    }

async def collect_preread_documents(self, request: PreReadCollectorRequest) -> Dict[str, Any]:
    """Collect relevant pre-read documents."""
    self._initialize_agents()
    start_time = datetime.utcnow()
    
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None, 
        self.preread_collector.execute, 
        request.meeting_context
    )
    
    execution_time = (datetime.utcnow() - start_time).total_seconds()
    
    return {
        "async def build_agenda(self, request: AgendaBuilderRequest) -> Dict[str, Any]:
    """Build intelligent agenda based on meeting context."""
    self._initialize_agents()
    start_time = datetime.utcnow()
    
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None, 
        self.agenda_builder.execute, 
        request.meeting_context, 
        request.focus_mode
    )
    
    execution_time = (datetime.utcnow() - start_time).total_seconds()
    
    return {
        "agenda": result,
        "execution_time": execution_time,
        "focus_mode": request.focus_mode,
        "meeting_context": request.meeting_context
    }

async def collect_preread_documents(self, request: PreReadCollectorRequest) -> Dict[str, Any]:
    """Collect relevant pre-read documents."""
    self._initialize_agents()
    start_time = datetime.utcnow()
    
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None, 
        self.preread_collector.execute, 
        request.meeting_context
    )
    
    execution_time = (datetime.utcnow() - start_time).total_seconds()
    
    return {
        "

Similar code found with 5 license types