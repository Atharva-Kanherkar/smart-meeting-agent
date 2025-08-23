from fastapi import APIRouter, HTTPException

from ..services.agent_service import AgentService
from ..models.agent_models import (
    CalendarRequest,
    PeopleResearchRequest,
    TechnicalContextRequest,
    CoordinatorRequest,
    AgentResponse
)

router = APIRouter()
agent_service = AgentService()

@router.post("/agents/calendar", response_model=AgentResponse)
async def run_calendar_agent(request: CalendarRequest):
    """Execute calendar agent to fetch meeting and calendar data."""
    try:
        result = await agent_service.run_calendar_agent(request)
        return AgentResponse(
            agent="calendar",
            status="success",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/agents/people-research", response_model=AgentResponse)
async def run_people_research_agent(request: PeopleResearchRequest):
    """Execute people research agent to gather attendee information."""
    try:
        result = await agent_service.run_people_research_agent(request)
        return AgentResponse(
            agent="people_research",
            status="success",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/agents/technical-context", response_model=AgentResponse)
async def run_technical_context_agent(request: TechnicalContextRequest):
    """Execute technical context agent to gather relevant technical information."""
    try:
        result = await agent_service.run_technical_context_agent(request)
        return AgentResponse(
            agent="technical_context",
            status="success",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/agents/coordinator", response_model=AgentResponse)
async def run_coordinator_agent(request: CoordinatorRequest):
    """Execute coordinator agent to compile and organize all information."""
    try:
        result = await agent_service.run_coordinator_agent(request)
        return AgentResponse(
            agent="coordinator",
            status="success",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))