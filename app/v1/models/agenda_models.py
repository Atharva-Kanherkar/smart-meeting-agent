from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class AgendaBuilderRequest(BaseModel):
    """Request model for agenda builder agent."""
    meeting_context: Dict[str, Any] = Field(..., description="Meeting context including title, participants, etc.")
    focus_mode: Optional[str] = Field("balanced", description="Focus mode: blockers, design, progress, planning, balanced")
    previous_meeting_notes: Optional[str] = Field(None, description="Notes from previous meetings")
    github_activity: Optional[Dict[str, Any]] = Field(None, description="Recent GitHub activity data")
    slack_activity: Optional[Dict[str, Any]] = Field(None, description="Recent Slack/communication data")

class PreReadCollectorRequest(BaseModel):
    """Request model for pre-read collector agent."""
    meeting_context: Dict[str, Any] = Field(..., description="Meeting context and participant information")
    document_sources: Optional[List[str]] = Field(["github", "notion", "slack"], description="Sources to search for documents")
    relevance_threshold: Optional[int] = Field(6, description="Minimum relevance score (1-10) for documents")

class ContextBriefingRequest(BaseModel):
    """Request model for context briefing agent."""
    meeting_data: Dict[str, Any] = Field(..., description="Complete meeting data and context")
    participant_roles: Dict[str, str] = Field(..., description="Mapping of participants to their roles")
    personalization_level: Optional[str] = Field("standard", description="Level of personalization: basic, standard, detailed")

class AgendaItem(BaseModel):
    """Model for individual agenda items."""
    title: str
    description: str
    priority: str  # High, Medium, Low
    time_allocation: str
    stakeholders: List[str]
    context: str

class AgendaResponse(BaseModel):
    """Response model for agenda builder."""
    meeting_title: str
    estimated_duration: str
    focus_mode: str
    agenda_items: List[AgendaItem]
    generated_at: datetime = Field(default_factory=datetime.utcnow)

class Document(BaseModel):
    """Model for pre-read documents."""
    title: str
    type: str
    source: str
    relevance_score: int
    summary: str
    key_points: List[str]
    link: str
    last_updated: str

class PreReadResponse(BaseModel):
    """Response model for pre-read collector."""
    meeting_title: str
    preread_summary: str
    documents: List[Document]
    action_items_context: List[str]
    generated_at: datetime = Field(default_factory=datetime.utcnow)

class PersonalizedBriefing(BaseModel):
    """Model for individual participant briefings."""
    role_focus: str
    key_changes: List[str]
    current_blockers: List[str]
    pending_decisions: List[str]
    relevant_metrics: Dict[str, Any]
    action_items: List[str]

class ContextBriefingResponse(BaseModel):
    """Response model for context briefing."""
    meeting_title: str
    briefings: Dict[str, PersonalizedBriefing]
    generated_at: datetime = Field(default_factory=datetime.utcnow)