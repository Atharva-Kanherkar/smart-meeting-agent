# agents/technical_context_agent.py
from portia import Portia
from portia.cli import CLIExecutionHooks

class TechnicalContextAgent:
    """Technical Context Agent for gathering relevant technical information."""
    
    PROMPT = """
    You are a Technical Context Agent. Your task is to gather relevant technical context for the meeting.
    
    Based on the calendar data and attendee information:
    1. Research recent technical developments related to the meeting topic
    2. Look for relevant documentation, code repositories, or technical discussions
    3. Identify key technical concepts or technologies that might be discussed
    4. Gather information about current project status, recent changes, or technical challenges
    5. Use web search tools to find recent news, blog posts, or technical articles related to the topic
    
    Focus on providing technical background that would be useful for meeting preparation.
    Present the information in a structured format with key technical insights.
    """
    
    def __init__(self, config, tools):
        self.agent = Portia(
            config=config, 
            tools=tools, 
            execution_hooks=CLIExecutionHooks()
        )
    
    def execute(self, calendar_data):
        """Execute technical context research."""
        print("🔧 Agent 3: Gathering technical context...")
        
        try:
            combined_prompt = f"""
            {self.PROMPT}
            
            Here is the calendar data to base your research on:
            {calendar_data}
            
            Please research and provide relevant technical context for this meeting.
            """
            
            result = self.agent.run(combined_prompt, end_user="technical_context_agent")
            
            if result and result.outputs and result.outputs.final_output:
                output = result.outputs.final_output.value
                print("✅ Technical context research completed.")
                print(f"Preview: {output[:200]}...\n")
                return output
            else:
                print("⚠️ No technical context returned. Using fallback.")
                return self._get_mock_technical_data()
                
        except Exception as e:
            print(f"❌ Technical context research failed: {e}")
            print("🔄 Using mock data for testing...")
            return self._get_mock_technical_data()
    
    def _get_mock_technical_data(self):
        """Provide mock technical context data."""
        return """Here is the technical context for the meeting:

**Technical Context for GSoC Workflows4s Project:**

**Project Overview:**
- Workflows4s: A workflow orchestration system for distributed computing
- Focus on scalable, fault-tolerant workflow execution
- Integration with modern cloud platforms and container orchestration

**Key Technical Areas:**
1. **Workflow Orchestration:**
   - Distributed task scheduling and execution
   - Dependency management between workflow steps
   - Error handling and retry mechanisms

2. **System Architecture:**
   - Microservices-based design
   - Event-driven architecture
   - Container orchestration (Kubernetes)

3. **Recent Developments:**
   - Implementation of new scheduling algorithms
   - Enhanced monitoring and observability features
   - Performance optimizations for large-scale workflows

**Technical Challenges:**
- Handling complex workflow dependencies
- Ensuring fault tolerance and recovery
- Scaling to handle high-throughput scenarios
- Integration with existing enterprise systems

**Technologies Involved:**
- Programming Languages: Scala, Python, Go
- Frameworks: Akka, Apache Kafka, Kubernetes
- Databases: PostgreSQL, Redis
- Monitoring: Prometheus, Grafana

This context should help frame technical discussions during the meeting."""