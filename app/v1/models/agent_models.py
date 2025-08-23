from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class CalendarRequest(BaseModel):
    """Request model for calendar agent."""
    date_range: Optional[Dict[str, str]] = Field(None, description="Start and end dates for calendar lookup")
    user_context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="User-specific context")

class PeopleResearchRequest(BaseModel):
    """Request model for people research agent."""
    attendee_emails: Optional[List[str]] = Field(None, description="List of attendee email addresses")
    calendar_context: Optional[Dict[str, Any]] = Field(None, description="Calendar data from previous agent")
    research_depth: Optional[str] = Field("standard", description="Research depth: basic, standard, comprehensive")

class TechnicalContextRequest(BaseModel):
    """Request model for technical context agent."""
    meeting_topics: Optional[List[str]] = Field(None, description="List of meeting topics or projects")
    calendar_context: Optional[Dict[str, Any]] = Field(None, description="Calendar data from previous agent")
    technical_focus: Optional[List[str]] = Field(None, description="Specific technical areas to focus on")

class SlackContextRequest(BaseModel):
    """Request model for Slack context agent."""
    calendar_context: Optional[Dict[str, Any]] = Field(None, description="Calendar data from previous agent")
    people_context: Optional[Dict[str, Any]] = Field(None, description="People research data from previous agent")
    search_channels: Optional[List[str]] = Field(None, description="Specific Slack channels to search")
    search_timeframe: Optional[str] = Field("7d", description="Time frame for Slack search (1d, 7d, 30d)")
    search_keywords: Optional[List[str]] = Field(None, description="Specific keywords to search for in Slack")

class CoordinatorRequest(BaseModel):
    """Request model for coordinator agent."""
    calendar_data: Optional[Dict[str, Any]] = Field(None, description="Output from calendar agent")
    people_data: Optional[Dict[str, Any]] = Field(None, description="Output from people research agent")
    technical_data: Optional[Dict[str, Any]] = Field(None, description="Output from technical context agent")
    slack_data: Optional[Dict[str, Any]] = Field(None, description="Output from Slack context agent")
    briefing_style: Optional[str] = Field("comprehensive", description="Style of final briefing")

class AgentResponse(BaseModel):
    """Generic response model for individual agents."""
    agent: str
    status: str
    data: Dict[str, Any]
    execution_time: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)