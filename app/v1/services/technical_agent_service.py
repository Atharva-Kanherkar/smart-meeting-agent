import asyncio
from datetime import datetime
from typing import Dict, Any, Optional
import sys
import os

# Add project root to path for agents import
current_file = os.path.abspath(__file__)
app_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
project_root = os.path.dirname(app_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Try to import Portia configuration properly
try:
    from portia import Config, StorageClass, LLMProvider, PortiaToolRegistry
    from portia.open_source_tools.registry import open_source_tool_registry
    PORTIA_AVAILABLE = True
except ImportError:
    PORTIA_AVAILABLE = False
    # Mock classes for compatibility
    class Config:
        @staticmethod
        def from_default(**kwargs):
            return {"mock": True}
    
    class StorageClass:
        CLOUD = "cloud"
    
    class LLMProvider:
        GOOGLE = "google"

from ..models.technical_models import (
    GitHubRepositoryRequest,
    GitHubIssuesRequest,
    DocumentationRequest,
    TechnologyStackRequest,
    TechnicalContextRequest
)

def get_proper_config():
    """Get proper Portia configuration or return None if not available."""
    if not PORTIA_AVAILABLE:
        return None
        
    required_keys = ["PORTIA_API_KEY", "GOOGLE_API_KEY", "TAVILY_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    if missing_keys:
        print(f"⚠️ Missing environment variables for Portia: {', '.join(missing_keys)}")
        return None
    
    try:
        return Config.from_default(
            storage_class=StorageClass.CLOUD,
            llm_provider=LLMProvider.GOOGLE,
        )
    except Exception as e:
        print(f"⚠️ Failed to create Portia config: {e}")
        return None

class TechnicalAgentService:
    """Service for handling technical research agents with lazy initialization."""
    
    def __init__(self):
        self.config = None
        self.tools = []
        self._agents_initialized = False
        
        # Initialize agents as None - will be created when needed
        self.github_repo_agent = None
        self.github_issues_agent = None
        self.documentation_agent = None
        self.tech_stack_agent = None
    
    def _initialize_agents(self):
        """Initialize agents lazily when first needed."""
        if self._agents_initialized:
            return
            
        print("🔧 Initializing technical agents...")
        
        # Try to get proper Portia configuration
        self.config = get_proper_config()
        
        if self.config and PORTIA_AVAILABLE:
            print("✅ Using Portia configuration")
            try:
                self.tools = PortiaToolRegistry(self.config) + open_source_tool_registry
                
                # Import and initialize agents with proper config
                from agents.github_repository_agent import GitHubRepositoryAgent
                from agents.github_issues_agent import GitHubIssuesAgent
                from agents.documentation_agent import DocumentationAgent
                from agents.technology_stack_agent import TechnologyStackAgent
                
                self.github_repo_agent = GitHubRepositoryAgent(self.config, self.tools)
                self.github_issues_agent = GitHubIssuesAgent(self.config, self.tools)
                self.documentation_agent = DocumentationAgent(self.config, self.tools)
                self.tech_stack_agent = TechnologyStackAgent(self.config, self.tools)
                
                print("✅ Technical agents initialized with Portia")
            except Exception as e:
                print(f"⚠️ Failed to initialize agents with Portia: {e}")
                self._initialize_mock_agents()
        else:
            print("🔄 Using mock agents (Portia not available)")
            self._initialize_mock_agents()
        
        self._agents_initialized = True
    
    def _initialize_mock_agents(self):
        """Initialize mock agents for testing."""
        # Import mock agent classes
        from agents.github_repository_agent import MockGitHubRepositoryAgent
        from agents.github_issues_agent import MockGitHubIssuesAgent
        from agents.documentation_agent import MockDocumentationAgent
        from agents.technology_stack_agent import MockTechnologyStackAgent
        
        self.github_repo_agent = MockGitHubRepositoryAgent()
        self.github_issues_agent = MockGitHubIssuesAgent()
        self.documentation_agent = MockDocumentationAgent()
        self.tech_stack_agent = MockTechnologyStackAgent()
    
    async def search_repositories(self, request: GitHubRepositoryRequest) -> Dict[str, Any]:
        """Search for GitHub repositories."""
        self._initialize_agents()
        start_time = datetime.utcnow()
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, self.github_repo_agent.execute, request.search_terms)
        
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        return {
            "output": result,
            "execution_time": execution_time,
            "search_terms": request.search_terms,
            "filters": {
                "organization": request.organization,
                "language": request.language,
                "limit": request.limit
            }
        }
    
    async def analyze_issues(self, request: GitHubIssuesRequest) -> Dict[str, Any]:
        """Analyze GitHub issues and development activity."""
        self._initialize_agents()
        start_time = datetime.utcnow()
        
        repo_info = f"Repositories: {', '.join(request.repository_urls)}"
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, self.github_issues_agent.execute, repo_info)
        
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        return {
            "output": result,
            "execution_time": execution_time,
            "repositories": request.repository_urls,
            "filters": {
                "issue_states": request.issue_states,
                "since_days": request.since_days
            }
        }
    
    async def search_documentation(self, request: DocumentationRequest) -> Dict[str, Any]:
        """Search for technical documentation."""
        self._initialize_agents()
        start_time = datetime.utcnow()
        
        project_context = f"Projects: {', '.join(request.project_names)}"
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, self.documentation_agent.execute, project_context)
        
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        return {
            "output": result,
            "execution_time": execution_time,
            "projects": request.project_names,
            "filters": {
                "doc_types": request.doc_types
            }
        }
    
    async def analyze_tech_stack(self, request: TechnologyStackRequest) -> Dict[str, Any]:
        """Analyze technology stack."""
        self._initialize_agents()
        start_time = datetime.utcnow()
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, self.tech_stack_agent.execute, request.repository_info)
        
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        return {
            "output": result,
            "execution_time": execution_time,
            "repository_info": request.repository_info,
            "focus_areas": request.focus_areas
        }
    
    async def comprehensive_analysis(self, request: TechnicalContextRequest) -> Dict[str, Any]:
        """Run comprehensive technical analysis."""
        self._initialize_agents()
        start_time = datetime.utcnow()
        
        # Build results from multiple agents
        results = {}
        
        if request.include_github:
            # Run repository search
            repo_result = await self.search_repositories(
                GitHubRepositoryRequest(search_terms="workflow orchestration")
            )
            results["repositories"] = repo_result
            
            # Run issues analysis
            issues_result = await self.analyze_issues(
                GitHubIssuesRequest(repository_urls=["workflows4s/core"])
            )
            results["issues"] = issues_result
        
        if request.include_docs:
            docs_result = await self.search_documentation(
                DocumentationRequest(project_names=["workflows4s"])
            )
            results["documentation"] = docs_result
        
        if request.include_tech_stack:
            tech_result = await self.analyze_tech_stack(
                TechnologyStackRequest(repository_info="Scala-based workflow system")
            )
            results["technology_stack"] = tech_result
        
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        return {
            "output": self._combine_results(results),
            "execution_time": execution_time,
            "calendar_context": request.calendar_context,
            "settings": {
                "research_depth": request.research_depth,
                "focus_areas": request.focus_areas
            }
        }
    
    def _combine_results(self, results):
        """Combine results from all sub-agents."""
        combined = "# Comprehensive Technical Analysis\n\n"
        
        if "repositories" in results:
            combined += "## Repository Analysis\n"
            combined += results["repositories"]["output"] + "\n\n"
        
        if "issues" in results:
            combined += "## Development Activity\n"
            combined += results["issues"]["output"] + "\n\n"
        
        if "documentation" in results:
            combined += "## Documentation\n"
            combined += results["documentation"]["output"] + "\n\n"
        
        if "technology_stack" in results:
            combined += "## Technology Stack\n"
            combined += results["technology_stack"]["output"] + "\n\n"
        
        return combined