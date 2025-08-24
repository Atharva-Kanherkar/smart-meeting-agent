from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from ..models.technical_models import (
    GitHubRepositoryRequest,
    GitHubIssuesRequest,
    DocumentationRequest,
    TechnologyStackRequest,
    TechnicalContextRequest,
    TechnicalAgentResponse
)

router = APIRouter()

# Initialize service as None - will be created when first endpoint is called
technical_service = None

def get_technical_service():
    """Get technical service with lazy initialization."""
    global technical_service
    if technical_service is None:
        from ..services.technical_agent_service import TechnicalAgentService
        technical_service = TechnicalAgentService()
    return technical_service

@router.post("/technical/github/repositories", response_model=TechnicalAgentResponse)
async def search_github_repositories(request: GitHubRepositoryRequest):
    """Search for relevant GitHub repositories."""
    try:
        service = get_technical_service()
        result = await service.search_repositories(request)
        return TechnicalAgentResponse(
            agent_type="github_repository",
            status="success",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/technical/github/issues", response_model=TechnicalAgentResponse)
async def analyze_github_issues(request: GitHubIssuesRequest):
    """Analyze GitHub issues and development activity."""
    try:
        service = get_technical_service()
        result = await service.analyze_issues(request)
        return TechnicalAgentResponse(
            agent_type="github_issues",
            status="success",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/technical/documentation", response_model=TechnicalAgentResponse)
async def search_documentation(request: DocumentationRequest):
    """Search for relevant technical documentation."""
    try:
        service = get_technical_service()
        result = await service.search_documentation(request)
        return TechnicalAgentResponse(
            agent_type="documentation",
            status="success",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/technical/technology-stack", response_model=TechnicalAgentResponse)
async def analyze_technology_stack(request: TechnologyStackRequest):
    """Analyze technology stack and frameworks."""
    try:
        service = get_technical_service()
        result = await service.analyze_tech_stack(request)
        return TechnicalAgentResponse(
            agent_type="technology_stack",
            status="success",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/technical/comprehensive", response_model=TechnicalAgentResponse)
async def comprehensive_technical_analysis(request: TechnicalContextRequest):
    """Run comprehensive technical analysis using all sub-agents."""
    try:
        service = get_technical_service()
        result = await service.comprehensive_analysis(request)
        return TechnicalAgentResponse(
            agent_type="technical_context_comprehensive",
            status="success",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))