from .calendar_agent import CalendarAgent
from .people_research_agent import PeopleResearchAgent, EnhancedPeopleResearchAgent
from .technical_context_agent import TechnicalContextAgent
from .slack_agent import SlackAgent
from .coordinator_agent import CoordinatorAgent, SimpleCoordinatorAgent

# New specialized technical agents
from .github_repository_agent import GitHubRepositoryAgent
from .github_issues_agent import GitHubIssuesAgent
from .documentation_agent import DocumentationAgent
from .technology_stack_agent import TechnologyStackAgent

__all__ = [
    'CalendarAgent',
    'PeopleResearchAgent', 
    'EnhancedPeopleResearchAgent',
    'TechnicalContextAgent',
    'SlackAgent',
    'CoordinatorAgent',
    'SimpleCoordinatorAgent',
    'GitHubRepositoryAgent',
    'GitHubIssuesAgent', 
    'DocumentationAgent',
    'TechnologyStackAgent'
]