# agents/__init__.py
from .calendar_agent import CalendarAgent
from .people_research_agent import PeopleResearchAgent, EnhancedPeopleResearchAgent
from .technical_context_agent import TechnicalContextAgent
from .slack_agent import SlackAgent
from .coordinator_agent import CoordinatorAgent, SimpleCoordinatorAgent

__all__ = [
    'CalendarAgent',
    'PeopleResearchAgent', 
    'EnhancedPeopleResearchAgent',
    'TechnicalContextAgent',
    'SlackAgent',
    'CoordinatorAgent',
    'SimpleCoordinatorAgent'
]