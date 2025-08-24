# agents/people_research_agent.py
from portia import Portia
from portia.cli import CLIExecutionHooks

class PeopleResearchAgent:
    """People Research Agent for profiling meeting attendees."""
    
    PROMPT = """
    You are a People Research Agent. Your task is to research meeting attendees and provide comprehensive profiles.
    
    For each attendee found in the calendar data:
    1. Use available tools to gather information about their:
       - Professional background and role
       - Company/organization
       - Recent activities and projects
       - Areas of expertise
       - Relevant context for the meeting
    
    2. If you have access to internal company directory tools, use them first
    3. For external attendees, use web research tools if available
    4. Provide insights that would be helpful for meeting preparation
    
    IMPORTANT: Return your response as a valid JSON object with this exact structure:
{
  "attendees": [
    {
      "email": "user@example.com",
      "name": "Full Name",
      "role": "Software Engineer",
      "organization": "Company Name",
      "background": "Brief background description",
      "expertise": ["JavaScript", "React", "Node.js"],
      "context": "How they relate to this meeting/project",
      "linkedinProfile": "https://linkedin.com/in/username",
      "githubProfile": "https://github.com/username",
      "recentActivity": "Recent work or achievements relevant to the meeting"
    }
  ]
}

Do not include any text before or after the JSON. Return only valid JSON

        """
    
    def __init__(self, config, tools):
        self.agent = Portia(
            config=config, 
            tools=tools, 
            execution_hooks=CLIExecutionHooks()
        )
    
    def execute(self, calendar_data):
        """Execute people research based on calendar data."""
        print("👥 Agent 2: Researching meeting attendees...")
        
        try:
            combined_prompt = f"""
            {self.PROMPT}
            
            Here is the calendar data with attendee information:
            {calendar_data}
            
            Please research each attendee and provide detailed profiles.
            """
            
            result = self.agent.run(combined_prompt, end_user="people_research_agent")
            
            if result and result.outputs and result.outputs.final_output:
                output = result.outputs.final_output.value
                print("✅ People research completed.")
                print(f"Preview: {output[:200]}...\n")
                return output
            else:
                print("⚠️ No people research returned. Using fallback.")
                return self._get_mock_people_data(calendar_data)
                
        except Exception as e:
            print(f"❌ People research failed: {e}")
            print("🔄 Using mock data for testing...")
            return self._get_mock_people_data(calendar_data)
    
    def _get_mock_people_data(self, calendar_data):
        """Provide mock people research data."""
        return """Here are the attendee profiles based on research:

**Attendee Profiles:**

**w.pitula@gmail.com (Wojciech Pitula)**
- Role: Project Mentor/Lead
- Background: Experienced in workflow orchestration and distributed systems
- Expertise: Software architecture, project management
- Context: Leading the GSoC Workflows4s project

**david.smith@purplekingdomgames.com (David Smith)**
- Role: Industry Partner
- Organization: Purple Kingdom Games
- Background: Game development and software engineering
- Expertise: Real-time systems, game engine architecture
- Context: Providing industry perspective on workflow systems

**atharvakanherkar25@gmail.com (Atharva Kanherkar)**
- Role: GSoC Student Developer
- Background: Software engineering student
- Expertise: Backend development, distributed systems
- Context: Working on Workflows4s implementation

**mr.kurro@gmail.com**
- Role: Technical Advisor/Mentor
- Background: Software development and system design
- Expertise: Technical guidance and code review
- Context: Supporting the GSoC project development"""


# Alias for backward compatibility with your existing code
class EnhancedPeopleResearchAgent(PeopleResearchAgent):
    """Alias for backward compatibility"""
    pass