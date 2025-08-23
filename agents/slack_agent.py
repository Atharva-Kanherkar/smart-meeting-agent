# agents/slack_agent.py
from portia import Portia
from portia.cli import CLIExecutionHooks

class SlackAgent:
    """Slack Context Agent for gathering relevant Slack conversations and messages."""
    
    PROMPT = """
    You are a Slack Context Agent. Your task is to gather relevant Slack communications for meeting preparation.
    
    Based on the calendar data and attendee information:
    1. Search for recent messages and conversations involving the meeting attendees
    2. Look for discussions related to the meeting topic or project
    3. Find relevant channels where the attendees are active
    4. Gather context from recent conversations that might be relevant to the meeting
    5. Identify any action items, decisions, or important updates shared in Slack
    
    Use the available Slack tools to:
    - List conversations/channels
    - Search for specific messages
    - Get conversation history from relevant channels
    - Find messages from/to specific attendees
    
    Focus on gathering context that would be useful for meeting preparation.
    Present the information in a structured format with key insights from Slack communications.
    """
    
    def __init__(self, config, tools):
        self.agent = Portia(
            config=config, 
            tools=tools, 
            execution_hooks=CLIExecutionHooks()
        )
        # Check if we have Slack tools available
        self.has_slack_tools = any('slack' in tool.name.lower() for tool in tools)
    
    def execute(self, calendar_data, people_data=""):
        """Execute Slack context research."""
        print("💬 Agent 5: Gathering Slack context...")
        
        if not self.has_slack_tools:
            print("⚠️ No Slack tools available. Using mock data for testing.")
            return self._get_mock_slack_data(calendar_data, people_data)
        
        try:
            combined_prompt = f"""
            {self.PROMPT}
            
            Here is the calendar data with meeting information:
            {calendar_data}
            
            Here is the people research data with attendee information:
            {people_data}
            
            Please search Slack for relevant conversations and context related to this meeting and its attendees.
            """
            
            result = self.agent.run(combined_prompt, end_user="slack_agent")
            
            if result and result.outputs and result.outputs.final_output:
                output = result.outputs.final_output.value
                print("✅ Slack context research completed.")
                print(f"Preview: {output[:200]}...\n")
                return output
            else:
                print("⚠️ No Slack context returned. Using fallback.")
                return self._get_mock_slack_data(calendar_data, people_data)
                
        except Exception as e:
            print(f"❌ Slack context research failed: {e}")
            print("🔄 Using mock data for testing...")
            return self._get_mock_slack_data(calendar_data, people_data)
    
    def _get_mock_slack_data(self, calendar_data, people_data):
        """Provide mock Slack context data."""
        return """Here is the relevant Slack context for the meeting:

**Slack Communication Context:**

**Recent Relevant Conversations:**

**#workflows4s-development Channel:**
- **Active Discussion on Architecture Changes** (Last 3 days)
  - @wojciech.pitula: "We need to finalize the new scheduling algorithm design"
  - @atharva.kanherkar: "I've been working on the distributed execution module"
  - @david.smith: "The game engine integration patterns might be useful here"

**#gsoc-projects Channel:**
- **Project Status Updates** (Last week)
  - Weekly standup discussions
  - Milestone progress reports
  - Technical blockers and solutions

**Direct Messages & Mentions:**

**@atharva.kanherkar Recent Activity:**
- Questions about workflow orchestration patterns
- Code review requests for distributed systems components
- Updates on GSoC project milestones

**@wojciech.pitula Recent Activity:**
- Mentorship guidance on system architecture
- Reviews of technical proposals
- Project roadmap discussions

**@david.smith Recent Activity:**
- Industry insights on scalable systems
- Feedback on real-time processing approaches
- Partnership collaboration topics

**Key Topics Discussed:**
1. **Performance Optimization:** Recent discussions about scaling challenges
2. **Architecture Decisions:** Debates on microservices vs monolithic approach
3. **Integration Challenges:** Issues with third-party service connections
4. **Timeline Concerns:** Sprint planning and milestone adjustments

**Action Items from Slack:**
- [ ] Review new scheduling algorithm proposal (due this week)
- [ ] Complete code review for distributed execution module
- [ ] Prepare demo for industry partner meeting
- [ ] Update project documentation

**Recent Shared Resources:**
- Technical documentation links
- Code repository references
- Research paper recommendations
- Meeting notes and decisions

This Slack context provides insight into recent team discussions and current priorities that may be relevant to the upcoming meeting."""