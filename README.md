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
