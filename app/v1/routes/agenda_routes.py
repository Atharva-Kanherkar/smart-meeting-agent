from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from ..services.agenda_service import AgendaService
from ..models.agenda_models import (
    AgendaBuilderRequest,
    PreReadCollectorRequest,
    ContextBriefingRequest,
    AgendaResponse,
    PreReadResponse,
    ContextBriefingResponse
)

router = APIRouter()

# Initialize service as None - will be created when first endpoint is called
agenda_service = None

def get_agenda_service():
    """Get agenda service with lazy initialization."""
    global agenda_service
    if agenda_service is None:
        from ..services.agenda_service import AgendaService
        agenda_service = AgendaService()
    return agenda_service

@router.post("/agenda/build", response_model=Dict[str, Any])
async def build_intelligent_agenda(request: AgendaBuilderRequest):
    """Build an AI-powered agenda based on meeting context."""
    try:
        service = get_agenda_service()
        result = await service.build_agenda(request)
        return {
            "agent_type": "agenda_builder",
            "status": "success",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/agenda/preread", response_model=Dict[str, Any])
async def collect_preread_documents(request: PreReadCollectorRequest):
    """Collect relevant pre-read documents for meeting preparation."""
    try:
        service = get_agenda_service()
        result = await service.collect_preread_documents(request)
        return {
            "agent_type": "preread_collector",
            "status": "success",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/agenda/briefing", response_model=Dict[str, Any])
async def generate_context_briefing(request: ContextBriefingRequest):
    """Generate personalized context briefings for meeting participants."""
    try:
        service = get_agenda_service()
        result = await service.generate_context_briefing(request)
        return {
            "agent_type": "context_briefing",
            "status": "success",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/agenda/comprehensive", response_model=Dict[str, Any])
async def comprehensive_agenda_preparation(
    meeting_context: Dict[str, Any],
    focus_mode: str = "balanced",
    participant_roles: Dict[str, str] = None
):
    """Run comprehensive agenda preparation including all components."""
    try:
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Quick agenda generation with focus modes
@router.post("/agenda/quick/{focus_mode}")
async def quick_agenda_generation(
    focus_mode: str,
    meeting_context: Dict[str, Any]
):
    """Quick agenda generation with specific focus mode."""
    if focus_mode not in ["blockers", "design", "progress", "planning", "balanced"]:
        raise HTTPException(status_code=400, detail="Invalid focus mode")
    
    try:
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))