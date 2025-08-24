from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class GitHubRepositoryRequest(BaseModel):
    """Request model for GitHub repository agent."""
    search_terms: str = Field(..., description="Terms to search for repositories")
    organization: Optional[str] = Field(None, description="Specific GitHub organization")
    language: Optional[str] = Field(None, description="Programming language filter")
    limit: Optional[int] = Field(10, description="Max repositories to return")

class GitHubIssuesRequest(BaseModel):
    """Request model for GitHub issues agent."""
    repository_urls: List[str] = Field(..., description="Repository URLs to analyze")
    issue_states: Optional[List[str]] = Field(["open"], description="Issue states")
    since_days: Optional[int] = Field(30, description="Days back to search")

class DocumentationRequest(BaseModel):
    """Request model for documentation agent."""
    project_names: List[str] = Field(..., description="Project names to search docs for")
    doc_types: Optional[List[str]] = Field(["api", "guide"], description="Doc types")

class TechnologyStackRequest(BaseModel):
    """Request model for technology stack agent."""
    repository_info: str = Field(..., description="Repository info to analyze")
    focus_areas: Optional[List[str]] = Field(None, description="Tech areas to focus on")

class TechnicalContextRequest(BaseModel):
    """Enhanced request model for technical context agent."""
    calendar_context: str = Field(..., description="Calendar data to base research on")
    focus_areas: Optional[List[str]] = Field(None, description="Technical areas to focus")
    research_depth: Optional[str] = Field("standard", description="Research depth")
    include_github: Optional[bool] = Field(True, description="Include GitHub analysis")
    include_docs: Optional[bool] = Field(True, description="Include documentation search")
    include_tech_stack: Optional[bool] = Field(True, description="Include tech stack analysis")

class TechnicalAgentResponse(BaseModel):
    """Response model for technical agents."""
    agent_type: str
    status: str
    data: Dict[str, Any]
    execution_time: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)