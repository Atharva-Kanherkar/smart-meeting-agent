from fastapi import APIRouter, BackgroundTasks, HTTPException
from typing import Dict, Any, List
import uuid
from datetime import datetime
from shared import job_storage  # 🔥 Import here if needed  # 🔥 ADD THIS LINE!
from ..services.meeting_service import MeetingService
from ..models.meeting_models import (
    MeetingPrepRequest,
    CustomMeetingPrepRequest,
    JobResponse,
    JobStatusResponse
)

router = APIRouter()
meeting_service = MeetingService()

@router.post("/meetings/prepare", response_model=JobResponse)
async def prepare_meeting(
    request: MeetingPrepRequest,
    background_tasks: BackgroundTasks
):
    """Start meeting preparation with full agent workflow."""
    job_id = str(uuid.uuid4())

    job_storage[job_id] = {
        "status": "started",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "progress": {"current_agent": None, "completed_agents": [], "total_agents": 5},
        "results": {}
    }
    
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

@router.post("/meetings/prepare-custom", response_model=JobResponse)
async def prepare_meeting_custom(
    request: CustomMeetingPrepRequest,
    background_tasks: BackgroundTasks
):
    """Start custom meeting preparation with selected agents."""
    job_id = str(uuid.uuid4())
    job_storage[job_id] = {
        "status": "started",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "progress": {"current_agent": None, "completed_agents": [], "total_agents": 5},
        "results": {}
    }
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

@router.get("/meetings/jobs/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    """Get the status and results of a meeting preparation job."""
    return meeting_service.get_job_status(job_id)

@router.get("/meetings/jobs")
async def get_all_jobs():
    """Get all jobs for dashboard view."""
    return meeting_service.get_all_jobs()

@router.delete("/meetings/jobs/{job_id}")
async def delete_job(job_id: str):
    """Delete a specific job."""
    from shared import job_storage
    if job_id in job_storage:
        del job_storage[job_id]
        return {"message": "Job deleted successfully"}
    raise HTTPException(status_code=404, detail="Job not found")