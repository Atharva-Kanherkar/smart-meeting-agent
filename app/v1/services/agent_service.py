import asyncio
import os
import sys
from datetime import datetime
from typing import Dict, Any

from portia import PortiaToolRegistry, Config, StorageClass, LLMProvider
from portia.open_source_tools.registry import open_source_tool_registry

# Add project root to path for agents import
current_file = os.path.abspath(__file__)
app_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
project_root = os.path.dirname(app_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from ..models.agent_models import (
    CalendarRequest,
    PeopleResearchRequest,
    TechnicalContextRequest,
    SlackContextRequest,
    CoordinatorRequest
)

from agents import (
    CalendarAgent,
    EnhancedPeopleResearchAgent as PeopleResearchAgent,
    TechnicalContextAgent,
    SlackAgent,
    CoordinatorAgent
)

def get_config():
    """Get Portia configuration."""
    required_keys = ["PORTIA_API_KEY", "GOOGLE_API_KEY", "TAVILY_API_KEY"]
    if not all(os.getenv(key) for key in required_keys):
        raise ValueError(f"Missing required environment variables: {', '.join(required_keys)}")
    
    return Config.from_default(
        storage_class=StorageClass.CLOUD,
        llm_provider=LLMProvider.GOOGLE,
    )

class AgentService:
    """Service for handling individual agent executions."""
    
    def __init__(self):
        self.config = get_config()
        self.all_tools = PortiaToolRegistry(self.config) + open_source_tool_registry
        
        # Initialize agents
        self.calendar_agent = CalendarAgent(self.config, self.all_tools)
        self.people_agent = PeopleResearchAgent(self.config, self.all_tools)
        self.technical_agent = TechnicalContextAgent(self.config, self.all_tools)
        self.slack_agent = SlackAgent(self.config, self.all_tools)
        self.coordinator_agent = CoordinatorAgent(self.config, self.all_tools)
    
    async def run_calendar_agent(self, request: CalendarRequest) -> Dict[str, Any]:
        """Execute calendar agent with API request."""
        start_time = datetime.utcnow()
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, self.calendar_agent.execute)
        
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        return {
            "output": result,
            "execution_time": execution_time,
            "request_context": request.dict()
        }
    
    async def run_calendar_agent_internal(self) -> str:
        """Internal method for calendar agent execution."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.calendar_agent.execute)
    
    async def run_people_research_agent(self, request: PeopleResearchRequest) -> Dict[str, Any]:
        """Execute people research agent with API request."""
        start_time = datetime.utcnow()
        
        calendar_context = request.calendar_context or ""
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, self.people_agent.execute, calendar_context)
        
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        return {
            "output": result,
            "execution_time": execution_time,
            "request_context": request.dict()
        }
    
    async def run_people_research_agent_internal(self, calendar_output: str) -> str:
        """Internal method for people research agent execution."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.people_agent.execute, calendar_output)
    
    async def run_technical_context_agent(self, request: TechnicalContextRequest) -> Dict[str, Any]:
        """Execute technical context agent with API request."""
        start_time = datetime.utcnow()
        
        calendar_context = request.calendar_context or ""
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, self.technical_agent.execute, calendar_context)
        
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        return {
            "output": result,
            "execution_time": execution_time,
            "request_context": request.dict()
        }
    
    async def run_technical_context_agent_internal(self, calendar_output: str) -> str:
        """Internal method for technical context agent execution."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.technical_agent.execute, calendar_output)
    
    async def run_slack_context_agent(self, request: SlackContextRequest) -> Dict[str, Any]:
        """Execute Slack context agent with API request."""
        start_time = datetime.utcnow()
        
        calendar_context = request.calendar_context or ""
        people_context = request.people_context or ""
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, self.slack_agent.execute, calendar_context, people_context)
        
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        return {
            "output": result,
            "execution_time": execution_time,
            "request_context": request.dict()
        }
    
    async def run_slack_context_agent_internal(self, calendar_output: str, people_output: str) -> str:
        """Internal method for Slack context agent execution."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.slack_agent.execute, calendar_output, people_output)
    
    async def run_coordinator_agent(self, request: CoordinatorRequest) -> Dict[str, Any]:
        """Execute coordinator agent with API request."""
        start_time = datetime.utcnow()
        
        calendar_data = request.calendar_data or ""
        people_data = request.people_data or ""
        technical_data = request.technical_data or ""
        slack_data = request.slack_data or ""
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None, 
            self.coordinator_agent.execute,
            calendar_data,
            people_data,
            technical_data,
            slack_data
        )
        
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        return {
            "output": result,
            "execution_time": execution_time,
            "request_context": request.dict()
        }
    
    async def run_coordinator_agent_internal(self, calendar_output: str, people_output: str, technical_output: str, slack_output: str = "") -> str:
        """Internal method for coordinator agent execution."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.coordinator_agent.execute,
            calendar_output,
            people_output,
            technical_output,
            slack_output
        )