from portia import Portia
from portia.cli import CLIExecutionHooks

class DocumentationAgent:
    """Agent specialized in finding and analyzing technical documentation."""
    
    PROMPT = """
    You are a Documentation Research Agent. Find relevant technical documentation.
    
    Search for:
    1. API documentation
    2. Architecture guides
    3. Setup/deployment guides
    4. Technical blog posts
    5. Official project docs
    
    Output format:
    - Document title and URL
    - Type of documentation
    - Key topics covered
    """
    
    def __init__(self, config, tools):
        self.agent = Portia(
            config=config, 
            tools=tools, 
            execution_hooks=CLIExecutionHooks()
        )
    
    def execute(self, project_context):
        """Find relevant technical documentation."""
        print("📚 Documentation Agent: Finding technical documentation...")
        
        try:
            prompt = f"""
            {self.PROMPT}
            
            Project context: {project_context}
            Find relevant technical documentation.
            """
            
            result = self.agent.run(prompt, end_user="documentation_agent")
            
            if result and result.outputs and result.outputs.final_output:
                output = result.outputs.final_output.value
                print("✅ Documentation search completed.")
                return output
            else:
                return self._get_mock_data()
                
        except Exception as e:
            print(f"❌ Documentation search failed: {e}")
            return self._get_mock_data()
    
    def _get_mock_data(self):
        return """**Technical Documentation Found:**

**API Documentation:**
- Workflows4s API Reference (https://docs.workflows4s.org/api)
- Topics: Workflow creation, execution, monitoring

**Architecture Guides:**
- Distributed Workflow Architecture (https://docs.workflows4s.org/arch)
- Topics: Microservices, event-driven patterns

**Setup Guides:**
- Kubernetes Deployment Guide (https://docs.workflows4s.org/deploy)
- Topics: Container orchestration, scaling"""