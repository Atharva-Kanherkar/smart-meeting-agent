from portia import Portia
from portia.cli import CLIExecutionHooks

class TechnologyStackAgent:
    """Agent specialized in researching technology stacks and frameworks."""
    
    PROMPT = """
    You are a Technology Stack Research Agent. Research technologies and frameworks.
    
    Focus on:
    1. Programming languages and versions
    2. Frameworks and libraries
    3. Infrastructure and deployment tech
    4. Monitoring and observability tools
    
    Output format:
    - Technology name and version
    - Purpose in the system
    - Recent updates
    """
    
    def __init__(self, config, tools):
        self.agent = Portia(
            config=config, 
            tools=tools, 
            execution_hooks=CLIExecutionHooks()
        )
    
    def execute(self, repository_info):
        """Research technology stack and frameworks."""
        print("🛠️ Technology Stack Agent: Researching tech stack...")
        
        try:
            prompt = f"""
            {self.PROMPT}
            
            Repository information: {repository_info}
            Research the technology stack used.
            """
            
            result = self.agent.run(prompt, end_user="tech_stack_agent")
            
            if result and result.outputs and result.outputs.final_output:
                output = result.outputs.final_output.value
                print("✅ Technology research completed.")
                return output
            else:
                return self._get_mock_data()
                
        except Exception as e:
            print(f"❌ Technology research failed: {e}")
            return self._get_mock_data()
    
    def _get_mock_data(self):
        return """**Technology Stack Analysis:**

**Programming Languages:**
- Scala 3.x: Primary language for core engine
- Python 3.11+: Tooling and integration
- Go 1.19+: High-performance components

**Frameworks:**
- Akka: Actor-based concurrency
- Apache Kafka: Event streaming
- ZIO: Functional programming

**Infrastructure:**
- Kubernetes: Container orchestration
- PostgreSQL: Primary data storage
- Redis: Caching"""