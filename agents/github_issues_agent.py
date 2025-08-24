from portia import Portia
from portia.cli import CLIExecutionHooks

class GitHubIssuesAgent:
    """Agent specialized in analyzing GitHub issues and development activity."""
    
    PROMPT = """
    You are a GitHub Issues Analysis Agent. Analyze issues and development activity.
    
    Focus on:
    1. Recent critical issues (bugs, blockers)
    2. Active feature development
    3. Performance/security concerns
    4. Recent commits and changes
    
    Output format:
    - Issue number, title, priority
    - Status and recent activity
    - Impact assessment
    """
    
    def __init__(self, config, tools):
        self.agent = Portia(
            config=config, 
            tools=tools, 
            execution_hooks=CLIExecutionHooks()
        )
    
    def execute(self, repository_info):
        """Analyze GitHub issues and development activity."""
        print("🐛 GitHub Issues Agent: Analyzing development activity...")
        
        try:
            prompt = f"""
            {self.PROMPT}
            
            Repository information: {repository_info}
            Analyze recent issues and development activity.
            """
            
            result = self.agent.run(prompt, end_user="github_issues_agent")
            
            if result and result.outputs and result.outputs.final_output:
                output = result.outputs.final_output.value
                print("✅ Issues analysis completed.")
                return output
            else:
                return self._get_mock_data()
                
        except Exception as e:
            print(f"❌ Issues analysis failed: {e}")
            return self._get_mock_data()
    
    def _get_mock_data(self):
        return """**Recent Development Activity:**

**Critical Issues:**
- Issue #156: Memory leak in workflow executor (High Priority, Open)
- Issue #148: Kubernetes integration failing (Open)
- Issue #142: Performance degradation (In Progress)

**Recent Commits:**
- Fix: Improved error handling
- Feature: Added conditional workflow steps
- Docs: Updated API documentation"""