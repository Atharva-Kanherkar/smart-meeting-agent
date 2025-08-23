# agents/coordinator_agent.py
from portia import Portia
from portia.cli import CLIExecutionHooks

class CoordinatorAgent:
    """Meeting Preparation Coordinator Agent for synthesizing all research."""
    
    PROMPT = """
    You are a Meeting Preparation Coordinator Agent. Your task is to synthesize research from multiple sources into a comprehensive meeting briefing.
    
    Create a structured meeting preparation document that includes:
    1. Meeting Overview (title, date, time, attendees)
    2. Attendee Profiles (key information about each person)
    3. Technical Context (relevant background information)
    4. Slack Communication Context (recent discussions and team dynamics)
    5. Key Discussion Points (likely topics based on all context)
    6. Preparation Recommendations (what to review or prepare)
    7. Action Items & Follow-ups (from Slack and other sources)
    
    Keep the briefing concise but comprehensive, focusing on actionable insights from all available data sources.
    """
    
    def __init__(self, config, tools):
        self.agent = Portia(
            config=config, 
            tools=tools, 
            execution_hooks=CLIExecutionHooks()
        )
    
    def execute(self, calendar_data, people_data, technical_data, slack_data=""):
        """Execute meeting preparation coordination."""
        print("🎯 Agent 6: Coordinating final meeting briefing...")
        
        try:
            combined_prompt = f"""
            {self.PROMPT}
            
            Here is the research data from other agents:
            
            CALENDAR DATA:
            {calendar_data}
            
            PEOPLE RESEARCH:
            {people_data}
            
            TECHNICAL CONTEXT:
            {technical_data}
            
            SLACK COMMUNICATION CONTEXT:
            {slack_data}
            
            Please create a comprehensive meeting briefing based on this information.
            """
            
            # Check if prompt is too long
            if len(combined_prompt) > 4000:
                combined_prompt = self._truncate_prompt(combined_prompt)
                
            result = self.agent.run(combined_prompt, end_user="coordinator_agent")
            
            if result and result.outputs and result.outputs.final_output:
                output = result.outputs.final_output.value
                print("✅ Meeting briefing completed.")
                print(f"Preview: {output[:200]}...")
                return output
            else:
                print("⚠️ No coordinator output returned. Using fallback.")
                return self._create_simple_briefing(calendar_data, people_data, technical_data, slack_data)
                
        except Exception as e:
            print(f"❌ Coordinator failed: {e}")
            print("🔄 Creating simple briefing...")
            return self._create_simple_briefing(calendar_data, people_data, technical_data, slack_data)
    
    def _truncate_prompt(self, prompt):
        """Truncate prompt if too long while preserving structure."""
        sections = prompt.split('\n\n')
        truncated_sections = []
        
        for section in sections:
            if len(section) > 800:
                truncated_sections.append(section[:800] + "... [truncated]")
            else:
                truncated_sections.append(section)
        
        return '\n\n'.join(truncated_sections)
    
    def _create_simple_briefing(self, calendar_data, people_data, technical_data, slack_data):
        """Create a simple briefing when the main agent fails."""
        return f"""# Meeting Preparation Briefing

## Meeting Overview
{calendar_data[:300] if calendar_data else "No calendar data available"}...

## Attendee Profiles
{people_data[:300] if people_data else "No people research available"}...

## Technical Context
{technical_data[:300] if technical_data else "No technical context available"}...

## Slack Communication Context
{slack_data[:300] if slack_data else "No Slack context available"}...

## Preparation Recommendations
- Review the attendee profiles and recent Slack discussions
- Prepare talking points based on technical context
- Be ready to discuss recent team communications and decisions
- Consider follow-up actions from Slack conversations

*This briefing was generated automatically. Please review all sections for accuracy.*
"""

class SimpleCoordinatorAgent:
    """Simplified coordinator that doesn't rely on LLM calls."""
    
    def __init__(self, config, tools):
        pass
    
    def execute(self, calendar_data, people_data, technical_data, slack_data=""):
        """Create a simple structured briefing."""
        return f"""# Meeting Preparation Briefing

## Meeting Overview
{calendar_data}

## Attendee Information
{people_data}

## Technical Context
{technical_data}

## Slack Communications
{slack_data}

## Key Preparation Points
- Review attendee backgrounds and recent work
- Understand technical context and current challenges
- Note recent team discussions and decisions from Slack
- Prepare for likely discussion topics based on all available context

---
*Generated by Smart Meeting Agent*
"""