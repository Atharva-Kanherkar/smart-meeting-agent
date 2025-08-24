import asyncio
from datetime import datetime
from typing import Dict, Any
import sys
import os
import importlib
import traceback

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
    """Get Portia configuration for agenda services if available and env keys present."""
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


def import_any(possible_module_names: list, attr_name: str):
    """
    Try multiple module paths and return the attribute (class/function) if found.
    Returns None if none found.
    """
    for mod in possible_module_names:
        try:
            module = importlib.import_module(mod)
            if hasattr(module, attr_name):
                return getattr(module, attr_name)
        except Exception:
            continue
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
        """Initialize agenda agents lazily and robustly when first needed."""
        if self._agents_initialized:
            return

        print("📋 Initializing agenda and preparation agents...")

        # Try to get proper Portia configuration
        self.config = get_agenda_config()

        if self.config and PORTIA_AVAILABLE:
            print("✅ Using Portia configuration for agenda services")
            try:
                self.tools = PortiaToolRegistry(self.config) + open_source_tool_registry

                # Best-effort imports — try multiple possible module names
                AgendaBuilder = import_any(
                    ["agents.agenda_builder", "agents.agenda_builder_agent"], "AgendaBuilderAgent"
                )
                PreReadCollector = import_any(
                    ["agents.pre_read_agent", "agents.pre_read_collector_agent", "agents.preread_collector_agent"],
                    "PreReadCollectorAgent"
                )
                ContextBriefing = import_any(
                    ["agents.context_briefings_agent", "agents.context_briefing_agent", "agents.context_briefings"],
                    "ContextBriefingAgent"
                )

                # If any main agent class missing, raise to trigger mock initialization
                if not (AgendaBuilder and PreReadCollector and ContextBriefing):
                    missing = []
                    if not AgendaBuilder:
                        missing.append("AgendaBuilderAgent")
                    if not PreReadCollector:
                        missing.append("PreReadCollectorAgent")
                    if not ContextBriefing:
                        missing.append("ContextBriefingAgent")
                    raise ImportError(f"Missing agenda agent classes: {', '.join(missing)}")

                # Instantiate agents with config and tools
                self.agenda_builder = AgendaBuilder(self.config, self.tools)
                self.preread_collector = PreReadCollector(self.config, self.tools)
                self.context_briefing = ContextBriefing(self.config, self.tools)

                print("✅ Agenda agents initialized with Portia")
            except Exception as e:
                print(f"⚠️ Failed to initialize agenda agents with Portia: {e}")
                traceback.print_exc()
                self._initialize_mock_agents()
        else:
            print("🔄 Using mock agenda agents (Portia not available or config missing)")
            self._initialize_mock_agents()

        self._agents_initialized = True

    def _initialize_mock_agents(self):
        """Initialize mock agents for testing. Try to import mocks, else create lightweight fallbacks."""
        # Try importing mock classes from standard places
        MockAgenda = import_any(
            ["agents.agenda_builder", "agents.agenda_builder_agent"],
            "MockAgendaBuilderAgent"
        )
        MockPreRead = import_any(
            ["agents.pre_read_agent", "agents.preread_collector_agent", "agents.preread_collector_agent"],
            "MockPreReadCollectorAgent"
        )
        MockContext = import_any(
            ["agents.context_briefings_agent", "agents.context_briefing_agent"],
            "MockContextBriefingAgent"
        )

        # If true mock classes not found, create simple local fallbacks that mimic interface
        if not MockAgenda:
            AgendaBuilderAgent = import_any(["agents.agenda_builder"], "AgendaBuilderAgent")
            if AgendaBuilderAgent:
                class SimpleMockAgenda:
                    def execute(self, context_data: Dict[str, Any], focus_mode: str = "balanced") -> Dict[str, Any]:
                        return AgendaBuilderAgent(None, [])._generate_mock_agenda(context_data or {}, focus_mode)
                MockAgenda = SimpleMockAgenda
            else:
                class MinimalMockAgenda:
                    def execute(self, context_data: Dict[str, Any], focus_mode: str = "balanced") -> Dict[str, Any]:
                        return {
                            "meeting_title": (context_data or {}).get("meeting_title", "Team Meeting"),
                            "focus_mode": focus_mode,
                            "agenda_items": [
                                {"title": "Status Update", "priority": "High", "time_allocation": "20m"}
                            ]
                        }
                MockAgenda = MinimalMockAgenda

        if not MockPreRead:
            # Try to import PreRead real class for using its mock method
            PreReadAgent = import_any(["agents.pre_read_agent"], "PreReadCollectorAgent")
            if PreReadAgent and hasattr(PreReadAgent, "_generate_mock_preread"):
                class SimpleMockPreRead:
                    def execute(self, meeting_context: Dict[str, Any]) -> Dict[str, Any]:
                        return PreReadAgent(None, [])._generate_mock_preread(meeting_context or {})
                MockPreRead = SimpleMockPreRead
            else:
                class MinimalMockPreRead:
                    def execute(self, meeting_context: Dict[str, Any]) -> Dict[str, Any]:
                        return {"documents": [], "summary": "No prereads available (mock)"}
                MockPreRead = MinimalMockPreRead

        if not MockContext:
            ContextAgent = import_any(["agents.context_briefings_agent", "agents.context_briefing_agent"], "ContextBriefingAgent")
            if ContextAgent and hasattr(ContextAgent, "_generate_mock_briefings"):
                class SimpleMockContext:
                    def execute(self, meeting_data: Dict[str, Any], participant_roles: Dict[str, str]) -> Dict[str, Any]:
                        return ContextAgent(None, [])._generate_mock_briefings(meeting_data or {}, participant_roles or {})
                MockContext = SimpleMockContext
            else:
                class MinimalMockContext:
                    def execute(self, meeting_data: Dict[str, Any], participant_roles: Dict[str, str]) -> Dict[str, Any]:
                        # Create a simple briefing per participant role
                        briefings = {}
                        for p, r in (participant_roles or {}).items():
                            briefings[p] = {"role": r, "summary": "No detailed briefing available (mock)"}
                        return briefings
                MockContext = MinimalMockContext

        # instantiate mocks
        try:
            self.agenda_builder = MockAgenda() if callable(MockAgenda) else MockAgenda
        except Exception:
            self.agenda_builder = MockAgenda

        try:
            self.preread_collector = MockPreRead() if callable(MockPreRead) else MockPreRead
        except Exception:
            self.preread_collector = MockPreRead

        try:
            self.context_briefing = MockContext() if callable(MockContext) else MockContext
        except Exception:
            self.context_briefing = MockContext

        print("🔧 Mock agenda agents initialized")

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
            "document_sources": getattr(request, "document_sources", None),
            "relevance_threshold": getattr(request, "relevance_threshold", None)
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
            "personalization_level": getattr(request, "personalization_level", None)
        }