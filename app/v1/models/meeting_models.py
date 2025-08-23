from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class MeetingPrepRequest(BaseModel):
    """Request model for full meeting preparation."""
    meeting_context: Optional[str] = Field(None, description="Additional context about the meeting")
    user_preferences: Optional[Dict[str, Any]] = Field(default_factory=dict, description="User-specific preferences")
    include_slack: Optional[bool] = Field(True, description="Whether to include Slack context in preparation")

class CustomMeetingPrepRequest(BaseModel):
    """Request model for custom meeting preparation with selected agents."""
    agents: List[str] = Field(..., description="List of agents to run: calendar, people_research, technical_context, slack_context, coordinator")
    meeting_context: Optional[str] = Field(None, description="Additional context about the meeting")
    calendar_data: Optional[Dict[str, Any]] = Field(None, description="Pre-existing calendar data")
    people_data: Optional[Dict[str, Any]] = Field(None, description="Pre-existing people research data")
    technical_data: Optional[Dict[str, Any]] = Field(None, description="Pre-existing technical context data")
    slack_data: Optional[Dict[str, Any]] = Field(None, description="Pre-existing Slack context data")
    user_preferences: Optional[Dict[str, Any]] = Field(default_factory=dict, description="User-specific preferences")

class JobResponse(BaseModel):
    """Response model for job initiation."""
    job_id: str
    status: str
    message: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class JobStatusResponse(BaseModel):
    """Response model for job status and results."""
    job_id: str
    status: str  # started, running, completed, failed
    created_at: datetime
    updated_at: datetime
    progress: Optional[Dict[str, Any]] = None
    results: Optional[Dict[str, Any]] = None
    error: Optional[str] = None