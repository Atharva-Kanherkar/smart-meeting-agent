import asyncio
from datetime import datetime
from typing import Dict, Any
from fastapi import HTTPException
import sys
import os

# Import from shared module to avoid circular imports
current_file = os.path.abspath(__file__)
app_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

from shared import job_storage
from .agent_service import AgentService
from ..models.meeting_models import (
    MeetingPrepRequest,
    CustomMeetingPrepRequest,
    JobStatusResponse
)

class MeetingService:
    """Service for handling meeting preparation workflows."""
    
    def __init__(self):
        self.agent_service = AgentService()
    
    async def run_full_preparation(self, job_id: str, request: MeetingPrepRequest):
        """Run the complete multi-agent meeting preparation workflow."""
        job_storage[job_id] = {
            "status": "running",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "progress": {"current_agent": "calendar", "completed_agents": []},
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
            job_storage[job_id]["progress"]["current_agent"] = "coordinator"
            job_storage[job_id]["updated_at"] = datetime.utcnow()
            
            # Step 4: Coordinator Agent
            final_briefing = await self.agent_service.run_coordinator_agent_internal(
                calendar_result, people_result, technical_result
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
    
    async def run_custom_preparation(self, job_id: str, request: CustomMeetingPrepRequest):
        """Run custom meeting preparation with selected agents."""
        job_storage[job_id] = {
            "status": "running",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "progress": {"current_agent": None, "completed_agents": [], "requested_agents": request.agents},
            "results": {}
        }
        
        try:
            results = {}
            
            # Use provided data or initialize
            calendar_data = request.calendar_data
            people_data = request.people_data
            technical_data = request.technical_data
            
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
                    
                elif agent_name == "coordinator":
                    final_briefing = await self.agent_service.run_coordinator_agent_internal(
                        calendar_data or "", people_data or "", technical_data or ""
                    )
                    results["coordinator"] = final_briefing
                    results["final_briefing"] = final_briefing
                
                job_storage[job_id]["progress"]["completed_agents"].append(agent_name)
                job_storage[job_id]["results"] = results
            
            job_storage[job_id]["status"] = "completed"
            job_storage[job_id]["progress"]["current_agent"] = None
            job_storage[job_id]["updated_at"] = datetime.utcnow()
            
        except Exception as e:
            job_storage[job_id]["status"] = "failed"
            job_storage[job_id]["error"] = str(e)
            job_storage[job_id]["updated_at"] = datetime.utcnow()
    
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