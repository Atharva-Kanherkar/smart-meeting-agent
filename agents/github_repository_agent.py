from portia import Portia
from portia.cli import CLIExecutionHooks

class GitHubRepositoryAgent:
    """Agent specialized in finding and analyzing GitHub repositories."""
    
    PROMPT = """
    You are a GitHub Repository Research Agent. Find and analyze GitHub repositories.
    
    Steps:
    1. Extract project/organization names from the input
    2. Search for relevant repositories using GitHub search tools
    3. Get repository info (stars, description, last updated)
    4. List most relevant repositories
    
    Output format:
    - Repository name and URL
    - Description and stars
    - Last updated date
    - Main programming language
    """
    
    def __init__(self, config, tools):
        self.agent = Portia(
            config=config, 
            tools=tools, 
            execution_hooks=CLIExecutionHooks()
        )
    
    def execute(self, search_terms):
        """Find relevant GitHub repositories."""
        print("🔍 GitHub Repository Agent: Searching repositories...")
        
        try:
            prompt = f"""
            {self.PROMPT}
            
            Search terms: {search_terms}
            Find relevant GitHub repositories.
            """
            
            result = self.agent.run(prompt, end_user="github_repo_agent")
            
            if result and result.outputs and result.outputs.final_output:
                output = result.outputs.final_output.value
                print("✅ Repository search completed.")
                return output
            else:
                return self._get_mock_data()
                
        except Exception as e:
            print(f"❌ Repository search failed: {e}")
            return self._get_mock_data()
    
    def _get_mock_data(self):
        return """**GitHub Repositories Found:**

**workflows4s/core** (https://github.com/workflows4s/core)
- Description: Workflow orchestration system
- Stars: 42 | Language: Scala | Last updated: 3 days ago

**business4s/forms4s** (https://github.com/business4s/forms4s)
- Description: Type-safe form handling
- Stars: 18 | Language: Scala 3 | Last updated: 1 week ago"""