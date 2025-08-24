import asyncio
from datetime import datetime
from typing import Dict, Any
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

from ..models.agenda_models import (
    AgendaBuilderRequest,
    PreReadCollectorRequest,
    ContextBriefingRequest
)

def get_agenda_config():
    """Get Portia configuration for agenda services."""
    if not PORTIA_AVAILABLE:
        return None
        
    required_keys = ["PORTIA_API_KEY", "GOOGLE_API_KEY", "TAVILY_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    if missing_keys:
        print(f"⚠️ Missing environment variables for Agenda services: {', '.join(missing_keys)}")
        return None
    
    try:
        return Config.from_default(
            storage_class=StorageClass.CLOUD,
            llm_provider=LLMProvider.GOOGLE,
        )
    except Exception as e:
        print(f"⚠️ Failed to create Agenda config: {e}")
        return None

class AgendaService:
    """Service for handling intelligent agenda and meeting preparation."""
    
    def __init__(self):
        self.config = None
        self.tools = []
        self._agents_initialized = False
        
        # Initialize agents as None - will be created when needed
        self.agenda_builder = None
        self.preread_collector = None
        self.context_briefing = None
    
    def _initialize_agents(self):
        """Initialize agenda agents lazily when first needed."""
        if self._agents_initialized:
            return
            
        print("📋 Initializing agenda and preparation agents...")
        
        # Try to get proper Portia configuration
        self.config = get_agenda_config()
        
        if self.config and PORTIA_AVAILABLE:
            print("✅ Using Portia configuration for agenda services")
            try:
                self.tools = PortiaToolRegistry(self.config) + open_source_tool_registry
                
                # Import and initialize agents with proper config
                from agents.agenda_builder_agent import AgendaBuilderAgent
                from agents.preread_collector_agent import PreReadCollectorAgent
                from agents.context_briefing_agent import ContextBriefingAgent
                
                self.agenda_builder = AgendaBuilderAgent(self.config, self.tools)
                self.preread_collector = PreReadCollectorAgent(self.config, self.tools)
                self.context_briefing = ContextBriefingAgent(self.config, self.tools)
                
                print("✅ Agenda agents initialized with Portia")
            except Exception as e:
                print(f"⚠️ Failed to initialize agenda agents with Portia: {e}")
                self._initialize_mock_agents()
        else:
            print("🔄 Using mock agenda agents (Portia not available)")
            self._initialize_mock_agents()
        
        self._agents_initialized = True
    
    def _initialize_mock_agents(self):
        """Initialize mock agents for testing."""
        from agents.agenda_builder_agent import MockAgendaBuilderAgent
        from agents.preread_collector_agent import MockPreReadCollectorAgent
        from agents.context_briefing_agent import MockContextBriefingAgent
        
        self.agenda_builder = MockAgendaBuilderAgent()
        self.preread_collector = MockPreReadCollectorAgent()
        self.context_briefing = MockContextBriefingAgent()
    
    async def build_agenda(self, request: AgendaBuilderRequest) -> Dict[str, Any]:
        """Build intelligent agenda based on meeting context."""
        self._initialize_agents()
        start_time = datetime.utcnow()
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None, 
            self.agenda_builder.execute, 
            request.meeting_context, 
            request.focus_mode
        )
        
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        return {
            "agenda": result,
            "execution_time": execution_time,
            "focus_mode": request.focus_mode,
            "meeting_context": request.meeting_context
        }
    
    async def collect_preread_documents(self, request: PreReadCollectorRequest) -> Dict[str, Any]:
        """Collect relevant pre-read documents."""
        self._initialize_agents()
        start_time = datetime.utcnow()
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None, 
            self.preread_collector.execute, 
            request.meeting_context
        )
        
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        return {
            "preread_packet": result,
            "execution_time": execution_time,
            "document_sources": request.document_sources,
            "relevance_threshold": request.relevance_threshold
        }
    
    async def generate_context_briefing(self, request: ContextBriefingRequest) -> Dict[str, Any]:
        """Generate personalized context briefings."""
        self._initialize_agents()
        start_time = datetime.utcnow()
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None, 
            self.context_briefing.execute, 
            request.meeting_data,
            request.participant_roles
        )
        
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        return {
            "briefings": result,
            "execution_time": execution_time,
            "participant_roles": request.participant_roles,
            "personalization_level": request.personalization_level
        }