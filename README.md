# Smart Meeting Agent

An AI-powered agent that automatically generates comprehensive meeting briefings by analyzing upcoming calendar events, researching attendees, and gathering relevant technical context.

## Features

- 📅 **Calendar Integration**: Fetches upcoming meetings from your calendar
- 👥 **Attendee Research**: Profiles meeting participants using company directory
- 🔧 **Technical Context**: Gathers recent commits, tickets, and discussions
- 📋 **Smart Briefings**: Generates comprehensive meeting briefings

## Project Structure

```
smart-meeting-agent/
├── agents/                 # AI agents for different tasks
│   ├── calendar_agent.py           # Calendar data fetching
│   ├── people_research_agent.py    # Attendee profiling
│   ├── technical_context_agent.py  # Technical context gathering
│   └── coordinator_agent.py        # Orchestrates all agents
├── app/                    # FastAPI web application
│   └── v1/
│       └── api.py         # REST API endpoints
├── tools/                  # Portia tools and utilities
│   └── directory_tool.py  # Company directory lookup tool
├── user_context/          # User-specific context and preferences
├── .portia/               # Portia SDK cache and configuration
├── main.py               # Main application entry point
├── pyproject.toml        # Project dependencies and metadata
└── .env                  # Environment variables
```

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -e .
   ```

2. **Configure Environment**:
   Copy `.env` and add your API keys:
   ```bash
   PORTIA_API_KEY=your_portia_api_key_here
   BROWSERBASE_API_KEY=your_browserbase_api_key_here
   ```

3. **Run the Application**:
   ```bash
   python main.py
   ```

4. **Start the API Server**:
   ```bash
   python app/v1/api.py
   ```

## API Usage

### Generate Meeting Briefing

```bash
curl -X POST "http://localhost:8000/v1/briefing" \
     -H "Content-Type: application/json" \
     -d '{
       "attendee_emails": ["emma.hr@example-corp.com", "bob.developer@example-corp.com"]
     }'
```

### Health Check

```bash
curl "http://localhost:8000/v1/health"
```

## Development

The project uses a multi-agent architecture:

1. **CalendarAgent**: Fetches meeting data from calendar systems
2. **PeopleResearchAgent**: Researches attendee backgrounds and roles
3. **TechnicalContextAgent**: Gathers relevant technical context
4. **CoordinatorAgent**: Orchestrates other agents and generates final briefing

Each agent can be developed and tested independently, making the system modular and maintainable.

## License

MIT License

Excellent! The API is working! Let me explain the complete architecture and workflow, then provide the .gitignore.

## 🏗️ Architecture Overview

Your Smart Meeting Agent API follows a **multi-layered FastAPI architecture** with a **multi-agent workflow system**:

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT (Frontend/API Calls)              │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP Requests
┌─────────────────────▼───────────────────────────────────────┐
│                 FASTAPI APPLICATION                         │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                   ROUTES LAYER                          │ │
│  │  /api/v1/health     /api/v1/meetings    /api/v1/agents │ │
│  └─────────────────────┬───────────────────────────────────┘ │
└────────────────────────┼─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│                   SERVICES LAYER                            │
│  ┌──────────────────┐              ┌─────────────────────┐  │
│  │ MeetingService   │              │   AgentService      │  │
│  │ - Orchestration  │◄────────────►│ - Agent Execution   │  │
│  │ - Job Management │              │ - Individual Agents │  │
│  └──────────────────┘              └─────────────────────┘  │
└────────────────────────┼─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│                   AGENTS LAYER                              │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │
│  │ Calendar    │ │ People      │ │ Technical   │ │Coordinator│ │
│  │ Agent       │ │ Research    │ │ Context     │ │ Agent    │ │
│  │             │ │ Agent       │ │ Agent       │ │          │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘ │
└────────────────────────┼─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│                 EXTERNAL TOOLS                              │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │
│  │ Portia      │ │ Google      │ │ Tavily      │ │Browser  │ │
│  │ Tools       │ │ Calendar    │ │ Search      │ │Use      │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 📁 File Structure Breakdown

```
smart-meeting-agent/
├── app/                          # FastAPI Application Package
│   ├── main.py                   # FastAPI app instance & config
│   ├── shared.py                 # Global job storage
│   └── v1/                       # API Version 1
│       ├── models/               # Pydantic Data Models
│       │   ├── meeting_models.py # Meeting-related models
│       │   └── agent_models.py   # Agent-specific models
│       ├── routes/               # FastAPI Route Handlers
│       │   ├── health.py         # Health check endpoint
│       │   ├── meetings.py       # Meeting workflow endpoints
│       │   └── agents.py         # Individual agent endpoints
│       └── services/             # Business Logic Layer
│           ├── meeting_service.py # Meeting orchestration
│           └── agent_service.py   # Agent execution
├── agents/                       # Your Agent Implementations
│   ├── calendar_agent.py
│   ├── people_research_agent.py
│   ├── technical_context_agent.py
│   └── coordinator_agent.py
└── run_api.py                    # Entry point script
```

## 🔄 Complete Workflow

### 1. **Single Agent Execution** (Direct Agent Call)
```
Client → POST /api/v1/agents/calendar
  ↓
AgentService.run_calendar_agent()
  ↓
CalendarAgent.execute()
  ↓
Returns result immediately
```

### 2. **Full Meeting Preparation** (Multi-Agent Workflow)
```
Client → POST /api/v1/meetings/prepare
  ↓
MeetingService.run_full_preparation() [Background Task]
  ↓
Sequential Agent Execution:
  1. CalendarAgent.execute()
  2. PeopleResearchAgent.execute(calendar_output)
  3. TechnicalContextAgent.execute(calendar_output)
  4. CoordinatorAgent.execute(all_outputs)
  ↓
Job completed, results stored
```

### 3. **Custom Workflow** (Selected Agents)
```
Client → POST /api/v1/meetings/prepare-custom
  ↓
MeetingService.run_custom_preparation() [Background Task]
  ↓
Run only selected agents in sequence
  ↓
Job completed, results stored
```

## 🌐 API Endpoints Detailed

### **Health & Status**
- `GET /api/v1/health` - API health check

### **Meeting Workflows**
- `POST /api/v1/meetings/prepare` - Start full meeting preparation
- `POST /api/v1/meetings/prepare-custom` - Start custom agent selection
- `GET /api/v1/meetings/jobs/{job_id}` - Get job status & results

### **Individual Agents**
- `POST /api/v1/agents/calendar` - Run calendar agent only
- `POST /api/v1/agents/people-research` - Run people research agent
- `POST /api/v1/agents/technical-context` - Run technical context agent
- `POST /api/v1/agents/coordinator` - Run coordinator agent

## 🔧 Key Components Interaction

### **1. Route Layer**
- **Purpose**: Handle HTTP requests, validation, response formatting
- **Responsibilities**: Request parsing, authentication, error handling
- **Interaction**: Calls Service Layer for business logic

### **2. Service Layer**
- **MeetingService**: Orchestrates multi-agent workflows, manages job lifecycle
- **AgentService**: Handles individual agent execution, async processing
- **Interaction**: Manages state in `shared.job_storage`, calls Agent Layer

### **3. Agent Layer**
- **Individual Agents**: Each agent has specific responsibilities
- **Tools Integration**: Uses Portia tools + open source tools
- **Data Flow**: Sequential processing with output chaining

### **4. Data Flow**
```
Request Data → Pydantic Models → Service Logic → Agent Execution → Tool Calls → Results
```

## 💾 State Management

### **Job Storage** (`shared.py`)
```python
job_storage = {
    "job_123": {
        "status": "running",
        "created_at": "2025-01-01T10:00:00",
        "updated_at": "2025-01-01T10:05:00",
        "progress": {
            "current_agent": "people_research",
            "completed_agents": ["calendar"]
        },
        "results": {
            "calendar": "Meeting data...",
            "people_research": "Attendee info..."
        }
    }
}
```

## 🔄 Async Processing

### **Background Tasks**
- Long-running agent workflows run as FastAPI background tasks
- Client gets immediate response with `job_id`
- Client polls `/jobs/{job_id}` for status updates
- Non-blocking for multiple concurrent requests

## 🛠️ Configuration & Dependencies

### **Environment Variables** (Required)
- `PORTIA_API_KEY` - Portia platform access
- `GOOGLE_API_KEY` - Google services access
- `TAVILY_API_KEY` - Tavily search access

### **Key Dependencies**
- **FastAPI**: Web framework
- **Portia**: Agent tools and LLM access
- **Pydantic**: Data validation
- **uvicorn**: ASGI server

 

## 🚀 Usage Examples

### **1. Start Full Meeting Preparation**
```bash
curl -X POST "http://localhost:8000/api/v1/meetings/prepare" \
  -H "Content-Type: application/json" \
  -d '{"meeting_context": "Weekly team standup"}'
```

### **2. Check Job Status**
```bash
curl "http://localhost:8000/api/v1/meetings/jobs/{job_id}"
```

### **3. Run Individual Agent**
```bash
curl -X POST "http://localhost:8000/api/v1/agents/calendar" \
  -H "Content-Type: application/json" \
  -d '{}'
```

Your API is now a fully functional, scalable meeting preparation system that can handle multiple concurrent requests and provide real-time status updates! 🎉

Similar code found with 5 license types