from .github_repository_agent import GitHubRepositoryAgent
from .github_issues_agent import GitHubIssuesAgent
from .documentation_agent import DocumentationAgent
from .technology_stack_agent import TechnologyStackAgent

class TechnicalContextAgent:
    """Coordinator for technical context research using specialized sub-agents."""
    
    def __init__(self, config, tools):
        self.github_repo_agent = GitHubRepositoryAgent(config, tools)
        self.github_issues_agent = GitHubIssuesAgent(config, tools)
        self.documentation_agent = DocumentationAgent(config, tools)
        self.tech_stack_agent = TechnologyStackAgent(config, tools)
    
    def execute(self, calendar_data):
        """Execute comprehensive technical context research."""
        print("🔧 Technical Context Agent: Starting comprehensive research...")
        
        try:
            # Extract search terms from calendar data
            search_terms = self._extract_search_terms(calendar_data)
            
            # Step 1: Find repositories
            repo_info = self.github_repo_agent.execute(search_terms)
            
            # Step 2: Analyze issues and development activity
            issues_info = self.github_issues_agent.execute(repo_info)
            
            # Step 3: Find documentation
            docs_info = self.documentation_agent.execute(f"{search_terms} {repo_info}")
            
            # Step 4: Research technology stack
            tech_info = self.tech_stack_agent.execute(repo_info)
            
            # Combine all results
            combined_result = self._combine_results(repo_info, issues_info, docs_info, tech_info)
            
            print("✅ Technical context research completed.")
            return combined_result
            
        except Exception as e:
            print(f"❌ Technical context research failed: {e}")
            return self._get_fallback_data()
    
    def _extract_search_terms(self, calendar_data):
        """Extract relevant search terms from calendar data."""
        terms = []
        if "workflow" in calendar_data.lower():
            terms.append("workflow")
        if "gsoc" in calendar_data.lower():
            terms.append("google summer of code")
        if "business4s" in calendar_data.lower():
            terms.append("business4s")
        
        return " ".join(terms) if terms else "workflow orchestration"
    
    def _combine_results(self, repo_info, issues_info, docs_info, tech_info):
        """Combine results from all sub-agents."""
        return f"""# Technical Context Research Results

## Repository Analysis
{repo_info}

## Development Activity
{issues_info}

## Documentation & Resources
{docs_info}

## Technology Stack
{tech_info}

## Summary
Meeting will focus on workflow orchestration systems, particularly Workflows4s project. 
Key discussion points: recent development challenges, system architecture, upcoming features.
"""
    
    def _get_fallback_data(self):
        """Fallback data when all agents fail."""
        return """# Technical Context (Limited Information)

## Project Overview
- Focus on workflow orchestration and distributed systems
- Scala-based implementation with modern architecture
- Integration with cloud platforms

## Key Areas for Discussion
- System architecture and design patterns
- Performance optimization strategies
- Deployment considerations
- Recent development progress

*Note: Limited context available. Review project documentation before meeting.*
"""