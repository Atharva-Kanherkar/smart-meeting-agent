from fastapi import APIRouter, BackgroundTasks, HTTPException
from typing import Dict, Any
import uuid

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

@router.get("/meetings/jobs/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    """Get the status and results of a meeting preparation job."""
    return meeting_service.get_job_status(job_id)