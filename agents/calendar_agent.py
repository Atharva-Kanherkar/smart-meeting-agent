# agents/calendar_agent.py
from portia import Portia
from portia.cli import CLIExecutionHooks

class CalendarAgent:
    """Calendar Data Retrieval Agent for extracting meeting information."""
    
    PROMPT = """
    You are a Calendar Data Retrieval Agent. Your task is to:
    
    1. Use the available tools to retrieve calendar events for the current user
    2. Extract key information from each event including:
       - Meeting title
       - Date and time
       - Attendee email addresses
       - Meeting location (if available)
       - Meeting description/context (if available)
    3. Present the information in a clear, structured format
    
    Focus on upcoming meetings and recent meetings that might be relevant for preparation.
    Return the data in a structured format that can be easily processed by other agents.
    """
    
    def __init__(self, config, tools):
        self.agent = Portia(
            config=config, 
            tools=tools, 
            execution_hooks=CLIExecutionHooks()
        )
        # Check if we have calendar tools available
        self.has_calendar_tools = any('calendar' in tool.name.lower() for tool in tools)
    
    def execute(self):
        """Execute calendar data retrieval."""
        print("📅 Agent 1: Retrieving calendar data...")
        
        if not self.has_calendar_tools:
            print("⚠️ No calendar tools available. Using mock data for testing.")
            return self._get_mock_calendar_data()
        
        try:
            result = self.agent.run(self.PROMPT, end_user="calendar_agent")
            
            if result and result.outputs and result.outputs.final_output:
                output = result.outputs.final_output.value
                print("✅ Calendar data retrieved.")
                print(f"Preview: {output[:200]}...\n")
                return output
            else:
                print("⚠️ No calendar data returned. Using fallback.")
                return self._get_mock_calendar_data()
                
        except Exception as e:
            print(f"❌ Calendar retrieval failed: {e}")
            print("🔄 Using mock data for testing...")
            return self._get_mock_calendar_data()
    
    def _get_mock_calendar_data(self):
        """Provide mock calendar data for testing when tools aren't available."""
        return """Here is the extracted information from the calendar events in a clear, structured format:

**Meeting 1:**
  Title: GSoC Workflows4s
  Date: 2025-05-16
  Time: 18:30
  Attendees: w.pitula@gmail.com, david.smith@purplekingdomgames.com, atharvakanherkar25@gmail.com, mr.kurro@gmail.com
  Location: Virtual Meeting
  Context: Google Summer of Code project discussion

**Meeting 2:**
  Title: GSoC Workflows4s Follow-up
  Date: 2025-08-25
  Time: 18:00
  Attendees: w.pitula@gmail.com, david.smith@purplekingdomgames.com, atharvakanherkar25@gmail.com, mr.kurro@gmail.com
  Location: Virtual Meeting
  Context: Follow-up discussion on Workflows4s implementation"""