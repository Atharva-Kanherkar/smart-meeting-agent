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
        # Initialize agenda service if available
        try:
            from .agenda_service import AgendaService
            self.agenda_service = AgendaService()
            self.has_agenda_service = True
        except ImportError:
            self.agenda_service = None
            self.has_agenda_service = False

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

    def _extract_meeting_title(self, calendar_data: str) -> str:
        """Extract meeting title from calendar data."""
        lines = calendar_data.split('\n')
        for line in lines:
            if 'Title:' in line:
                return line.split('Title:')[1].strip()
        return "Meeting"

    def _extract_participants(self, people_data: str) -> list:
        """Extract participants from people data."""
        # Simple extraction - in real implementation, use more sophisticated parsing
        participants = []
        lines = people_data.split('\n')
        for line in lines:
            if '@' in line and 'gmail.com' in line:
                # Extract email addresses
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