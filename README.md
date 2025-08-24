# Smart Meeting Agent 🤖📅

An AI-powered multi-agent system that automatically generates comprehensive meeting briefings by analyzing upcoming calendar events, researching attendees, gathering technical context, and synthesizing Slack communications.

## 🌟 Overview

The Smart Meeting Agent is a FastAPI-based application that uses specialized AI agents to prepare you for meetings by automatically researching and organizing relevant information. It transforms meeting preparation from a manual, time-consuming task into an automated, intelligent workflow.

## 🏗️ System Architecture

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
│  │  /api/v1/technical/*                                   │ │
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

## 📁 Project Structure

```
smart-meeting-agent/
├── 📱 app/                          # FastAPI Application Package
│   ├── main.py                      # FastAPI app instance & configuration
│   ├── shared.py                    # Global job storage & state management
│   └── v1/                          # API Version 1
│       ├── 📊 models/               # Pydantic Data Models
│       │   ├── meeting_models.py    # Meeting workflow models
│       │   ├── agent_models.py      # Individual agent models
│       │   └── technical_models.py  # Technical agent models
│       ├── 🛣️ routes/               # FastAPI Route Handlers
│       │   ├── health.py            # Health check endpoints
│       │   ├── meetings.py          # Meeting workflow endpoints
│       │   ├── agents.py            # Individual agent endpoints
│       │   └── technical_agents.py  # Technical analysis endpoints
│       └── 🔧 services/             # Business Logic Layer
│           ├── meeting_service.py   # Meeting orchestration service
│           ├── agent_service.py     # Agent execution service
│           └── technical_agent_service.py # Technical analysis service
├── 🤖 agents/                       # AI Agent Implementations
│   ├── calendar_agent.py            # Calendar data retrieval
│   ├── people_research_agent.py     # Attendee profiling
│   ├── technical_context_agent.py   # Technical context coordinator
│   ├── slack_agent.py               # Slack communication analysis
│   ├── coordinator_agent.py         # Final briefing synthesis
│   ├── github_repository_agent.py   # GitHub repository search
│   ├── github_issues_agent.py       # GitHub issues analysis
│   ├── documentation_agent.py       # Technical documentation search
│   └── technology_stack_agent.py    # Technology stack research
├── 🔧 Configuration Files
│   ├── pyproject.toml               # Dependencies & project config
│   ├── Dockerfile                   # Container configuration
│   ├── render.yaml                  # Deployment configuration
│   └── .env                         # Environment variables
└── 🚀 Entry Points
    └── run_api.py                   # Development server launcher
```

## 🎯 Core Components

### **1. AI Agents (The Brain)**
Each agent is a specialized AI that performs a specific research task:

- **📅 Calendar Agent**: Extracts meeting details from calendar systems
- **👥 People Research Agent**: Profiles meeting attendees using various data sources
- **🔧 Technical Context Agent**: Coordinates technical research through sub-agents
  - **📦 GitHub Repository Agent**: Searches for relevant code repositories
  - **🐛 GitHub Issues Agent**: Analyzes development activity and issues
  - **📚 Documentation Agent**: Finds technical documentation
  - **🛠️ Technology Stack Agent**: Researches frameworks and technologies
- **💬 Slack Agent**: Analyzes recent team communications
- **🎯 Coordinator Agent**: Synthesizes all research into a comprehensive briefing

### **2. Service Layer (The Orchestrator)**
- **Meeting Service**: Manages multi-agent workflows and job lifecycle
- **Agent Service**: Handles individual agent execution
- **Technical Agent Service**: Coordinates technical research sub-agents

### **3. API Layer (The Interface)**
- **Meeting Endpoints**: Full workflow management
- **Agent Endpoints**: Individual agent execution
- **Technical Endpoints**: Specialized technical analysis
- **Health Endpoints**: System status monitoring

## 🌊 Complete User Flow: From Zero to One

### **Phase 1: Setup & Configuration**

1. **Environment Setup**
   ```bash
   # Clone and install
   git clone <repository>
   cd smart-meeting-agent
   pip install -e .
   
   # Configure environment variables
   cp .env.example .env
   # Add your API keys:
   # PORTIA_API_KEY, GOOGLE_API_KEY, TAVILY_API_KEY
   ```

2. **Start the System**
   ```bash
   python run_api.py
   # API becomes available at http://localhost:8000
   ```

### **Phase 2: Meeting Preparation Request**

**Scenario**: Sarah has a "GSoC Workflows4s" meeting tomorrow and wants to prepare.

#### **Option A: Full Automatic Preparation** 🚀
```bash
curl -X POST "http://localhost:8000/api/v1/meetings/prepare" \
  -H "Content-Type: application/json" \
  -d '{
    "meeting_context": "GSoC Workflows4s weekly standup",
    "include_slack": true
  }'

# Response:
{
  "job_id": "abc-123-def",
  "status": "started",
  "message": "Meeting preparation started"
}
```

#### **Option B: Custom Agent Selection** 🎛️
```bash
curl -X POST "http://localhost:8000/api/v1/meetings/prepare-custom" \
  -H "Content-Type: application/json" \
  -d '{
    "agents": ["calendar", "people_research", "technical_context"],
    "meeting_context": "Focus on technical discussion"
  }'
```

#### **Option C: Individual Agent Execution** 🔍
```bash
# Run just the technical analysis
curl -X POST "http://localhost:8000/api/v1/technical/comprehensive" \
  -H "Content-Type: application/json" \
  -d '{
    "calendar_context": "GSoC Workflows4s meeting",
    "research_depth": "comprehensive"
  }'
```

### **Phase 3: Multi-Agent Workflow Execution** 🔄

When Sarah triggers full preparation, here's what happens behind the scenes:

#### **Step 1: Calendar Agent Activation** 📅
```
Calendar Agent → Google Calendar API → Extract Meeting Data
```
**Output Example**:
```
Meeting: GSoC Workflows4s
Date: 2025-08-25, 18:00
Attendees: w.pitula@gmail.com, david.smith@purplekingdomgames.com, 
           atharvakanherkar25@gmail.com, mr.kurro@gmail.com
Location: https://meet.google.com/cbc-jmvk-txk
```

#### **Step 2: People Research Agent Activation** 👥
```
People Agent → Portia Tools → Web Research → Attendee Profiles
```
**Output Example**:
```
Wojciech Pitula: Project Mentor, Scala expert, business4s ecosystem
David Smith: Industry Partner, Purple Kingdom Games, Game Engine Architecture
Atharva Kanherkar: GSoC Student, Backend Developer
Mr. Kurro: Technical Advisor, Code Review Specialist
```

#### **Step 3: Technical Context Agent Coordination** 🔧
This agent coordinates 4 sub-agents:

**3a. GitHub Repository Agent**
```
GitHub Repo Agent → GitHub API → Repository Search
```
Finds: workflows4s/core, business4s/forms4s, business4s/decisions4s

**3b. GitHub Issues Agent**
```
GitHub Issues Agent → GitHub API → Issues Analysis
```
Finds: Recent bugs, feature requests, performance issues

**3c. Documentation Agent**
```
Documentation Agent → Tavily Search → Technical Docs
```
Finds: API docs, architecture guides, deployment guides

**3d. Technology Stack Agent**
```
Tech Stack Agent → Web Research → Framework Analysis
```
Finds: Scala 3, Akka, Kubernetes, PostgreSQL stack

#### **Step 4: Slack Agent Activation** 💬
```
Slack Agent → Slack API → Communication Analysis
```
**Output Example**:
```
Recent Discussions:
- #workflows4s-development: Architecture changes discussion
- #gsoc-projects: Weekly progress updates
- Direct messages: Technical blockers and solutions
```

#### **Step 5: Coordinator Agent Synthesis** 🎯
```
Coordinator Agent → LLM Processing → Final Briefing Generation
```

### **Phase 4: Real-Time Status Monitoring** 📊

Sarah can monitor progress in real-time:

```bash
curl "http://localhost:8000/api/v1/meetings/jobs/abc-123-def"

# Response shows current progress:
{
  "job_id": "abc-123-def",
  "status": "running",
  "progress": {
    "current_agent": "technical_context",
    "completed_agents": ["calendar", "people_research"]
  },
  "results": {
    "calendar": "Meeting data...",
    "people_research": "Attendee profiles..."
  }
}
```

### **Phase 5: Final Briefing Delivery** 📋

After 3-5 minutes, Sarah receives her complete briefing:

```bash
# Final status check
curl "http://localhost:8000/api/v1/meetings/jobs/abc-123-def"

# Response:
{
  "job_id": "abc-123-def",
  "status": "completed",
  "results": {
    "final_briefing": "# Meeting Preparation Briefing\n\n## Meeting Overview\n..."
  }
}
```

**Final Briefing Structure**:
```markdown
# Meeting Preparation Briefing

## 1. Meeting Overview
- Title: GSoC Workflows4s
- Date/Time: 2025-08-25, 18:00-18:25 (Europe/Warsaw)
- Attendees: [4 participants with roles]
- Location: Google Meet

## 2. Attendee Profiles
- Wojciech Pitula: [Background, expertise, recent work]
- David Smith: [Industry context, relevant experience]
- Atharva Kanherkar: [GSoC student, current projects]
- Mr. Kurro: [Technical advisor role]

## 3. Technical Context
- Current Workflows4s development status
- Recent GitHub activity and issues
- Technology stack overview
- Architecture decisions pending

## 4. Slack Communication Context
- Recent team discussions
- Current blockers and solutions
- Project milestone updates

## 5. Key Discussion Points
- Performance optimization challenges
- Architecture decision reviews
- GSoC milestone planning
- Industry partnership opportunities

## 6. Preparation Recommendations
- Review latest commit changes
- Prepare updates on current work
- Consider technical questions for David
- Ready demo materials if applicable

## 7. Action Items & Follow-ups
- [Items from recent Slack discussions]
- [Decisions needed in this meeting]
```

## 🔄 System Workflow Types

### **1. Full Automatic Workflow** (Recommended)
```
User Request → Calendar → People → Technical → Slack → Coordinator → Briefing
```
**Use Case**: Complete meeting preparation with minimal input
**Time**: 3-5 minutes
**Coverage**: Comprehensive

### **2. Custom Selective Workflow**
```
User Request → [Selected Agents] → Coordinator → Briefing
```
**Use Case**: Focus on specific aspects (technical-only, people-only, etc.)
**Time**: 1-3 minutes
**Coverage**: Targeted

### **3. Individual Agent Execution**
```
User Request → Single Agent → Direct Result
```
**Use Case**: Quick specific research (just GitHub analysis, just attendee lookup)
**Time**: 30 seconds - 1 minute
**Coverage**: Focused

### **4. Technical Deep-Dive Workflow**
```
User Request → GitHub Repos → GitHub Issues → Documentation → Tech Stack → Combined Analysis
```
**Use Case**: Technical meetings requiring deep technical context
**Time**: 2-3 minutes
**Coverage**: Technical-focused

## 📊 State Management & Job Tracking

The system uses an in-memory job storage system:

```python
job_storage = {
    "job_123": {
        "status": "running",           # started, running, completed, failed
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

## 🛠️ Technical Implementation Details

### **Agent Communication Pattern**
```python
# Sequential data flow
calendar_output = calendar_agent.execute()
people_output = people_agent.execute(calendar_output)
technical_output = technical_agent.execute(calendar_output)
slack_output = slack_agent.execute(calendar_output, people_output)
final_briefing = coordinator_agent.execute(
    calendar_output, people_output, technical_output, slack_output
)
```

### **Async Processing Architecture**
```python
# Background task execution
@router.post("/meetings/prepare")
async def prepare_meeting(request, background_tasks):
    job_id = str(uuid.uuid4())
    background_tasks.add_task(meeting_service.run_full_preparation, job_id, request)
    return {"job_id": job_id, "status": "started"}
```

### **Error Handling & Fallbacks**
- **Graceful Degradation**: If one agent fails, others continue
- **Mock Data Fallbacks**: System works even without API keys (for testing)
- **Retry Logic**: Automatic retries for transient failures
- **Partial Results**: Briefing generated even with incomplete data

## 🚀 API Endpoints Reference

### **Meeting Workflows**
```bash
POST /api/v1/meetings/prepare              # Full automatic preparation
POST /api/v1/meetings/prepare-custom       # Custom agent selection
GET  /api/v1/meetings/jobs/{job_id}        # Job status & results
```

### **Individual Agents**
```bash
POST /api/v1/agents/calendar               # Calendar data only
POST /api/v1/agents/people-research        # Attendee research only
POST /api/v1/agents/technical-context      # Technical analysis only
POST /api/v1/agents/slack-context          # Slack analysis only
POST /api/v1/agents/coordinator            # Briefing synthesis only
```

### **Technical Analysis**
```bash
POST /api/v1/technical/github/repositories # GitHub repository search
POST /api/v1/technical/github/issues       # GitHub issues analysis
POST /api/v1/technical/documentation       # Documentation search
POST /api/v1/technical/technology-stack    # Tech stack analysis
POST /api/v1/technical/comprehensive       # All technical agents
```

### **System Health**
```bash
GET  /api/v1/health                        # Health check
GET  /                                     # Root status
```

## 🔧 Configuration & Setup

### **Required Environment Variables**
```bash
PORTIA_API_KEY="your_portia_api_key"       # Portia platform access
GOOGLE_API_KEY="your_google_api_key"       # Google Calendar & services
TAVILY_API_KEY="your_tavily_api_key"       # Web search capabilities
```

### **Optional Environment Variables**
```bash
BROWSERBASE_API_KEY="your_browserbase_key" # Enhanced web browsing
SLACK_BOT_TOKEN="your_slack_token"         # Slack integration
ENVIRONMENT="development"                   # Environment setting
```

### **Development Setup**
```bash
# 1. Clone repository
git clone <repository-url>
cd smart-meeting-agent

# 2. Install dependencies
pip install -e .

# 3. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 4. Start development server
python run_api.py

# 5. Access API documentation
# http://localhost:8000/docs
```

### **Production Deployment**
```bash
# Using Docker
docker build -t smart-meeting-agent .
docker run -p 8000:8000 --env-file .env smart-meeting-agent

# Using Render (configured in render.yaml)
# Push to git → Automatic deployment
```

## 🧪 Testing the System

### **Quick Health Check**
```bash
curl http://localhost:8000/api/v1/health
```

### **Test Individual Agent**
```bash
curl -X POST "http://localhost:8000/api/v1/agents/calendar" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### **Test Technical Analysis**
```bash
curl -X POST "http://localhost:8000/api/v1/technical/github/repositories" \
  -H "Content-Type: application/json" \
  -d '{"search_terms": "workflow scala", "limit": 5}'
```

### **Test Full Workflow**
```bash
# Start preparation
JOB_ID=$(curl -X POST "http://localhost:8000/api/v1/meetings/prepare" \
  -H "Content-Type: application/json" \
  -d '{"meeting_context": "Team standup"}' | jq -r .job_id)

# Check status
curl "http://localhost:8000/api/v1/meetings/jobs/$JOB_ID"
```

## 🎯 Use Cases & Examples

### **Use Case 1: Weekly Team Standup**
Sarah needs to prepare for her weekly engineering standup:
```bash
curl -X POST "http://localhost:8000/api/v1/meetings/prepare" \
  -H "Content-Type: application/json" \
  -d '{
    "meeting_context": "Weekly engineering standup",
    "include_slack": true
  }'
```
**Result**: Briefing with team updates, recent Slack discussions, current technical blockers

### **Use Case 2: Client Technical Review**
David needs technical context for a client architecture review:
```bash
curl -X POST "http://localhost:8000/api/v1/technical/comprehensive" \
  -H "Content-Type: application/json" \
  -d '{
    "calendar_context": "Architecture review with TechCorp",
    "research_depth": "comprehensive",
    "include_github": true,
    "include_docs": true,
    "include_tech_stack": true
  }'
```
**Result**: Deep technical analysis with repository status, documentation, and technology overview

### **Use Case 3: GSoC Mentorship Meeting**
Wojciech prepares for GSoC student mentorship:
```bash
curl -X POST "http://localhost:8000/api/v1/meetings/prepare-custom" \
  -H "Content-Type: application/json" \
  -d '{
    "agents": ["calendar", "people_research", "technical_context"],
    "meeting_context": "GSoC mentorship session"
  }'
```
**Result**: Student background, recent project work, technical progress analysis

## 🔒 Security & Privacy

- **API Key Management**: Secure environment variable handling
- **Data Privacy**: No persistent storage of meeting content
- **Rate Limiting**: Built-in protection against API abuse
- **Error Sanitization**: Sensitive information removed from error messages

## 🚀 Performance & Scalability

- **Async Processing**: Non-blocking background task execution
- **Concurrent Agents**: Multiple agents can run simultaneously
- **Lazy Initialization**: Services created only when needed
- **Memory Efficient**: In-memory job storage with automatic cleanup
- **Fallback Systems**: Graceful degradation when services unavailable

## 🔮 Future Enhancements

- **Persistent Storage**: Database integration for job history
- **Real-time Updates**: WebSocket support for live progress updates
- **AI Learning**: Personalized briefing styles based on user preferences
- **Integration Expansion**: Microsoft Teams, Zoom, additional calendar systems
- **Mobile App**: Native mobile application for on-the-go preparation
- **Analytics Dashboard**: Meeting preparation analytics and insights

## 📈 System Benefits

### **For Users**
- ⏰ **Time Savings**: 30+ minutes of manual research → 3 minutes automated
- 🎯 **Better Preparation**: Comprehensive context vs. scattered information
- 🤖 **Consistent Quality**: AI ensures nothing important is missed
- 📱 **Accessibility**: Available anywhere with API access

### **For Teams**
- 📊 **Improved Meetings**: Better-prepared participants lead to more productive meetings
- 🔄 **Standardization**: Consistent preparation process across the organization
- 💡 **Knowledge Sharing**: Automated discovery of relevant team knowledge
- 📈 **Scalability**: Handles increasing meeting volume without linear cost increase

### **For Organizations**
- 💰 **Cost Efficiency**: Reduced time spent on meeting preparation
- 🚀 **Productivity Boost**: More effective meetings and decision-making
- 🔍 **Knowledge Discovery**: Automatic surfacing of relevant organizational knowledge
- 📋 **Process Optimization**: Data-driven insights into meeting effectiveness

---

## 📞 Support & Contact

- **Issues**: Open GitHub issues for bugs and feature requests
- **Documentation**: Comprehensive API docs at `/docs` endpoint
- **Contributing**: See CONTRIBUTING.md for development guidelines

**The Smart Meeting Agent transforms meeting preparation from a manual chore into an intelligent, automated workflow. Never walk into an unprepared meeting again!** 🚀