from portia import Portia
from portia.cli import CLIExecutionHooks
from typing import Dict, List, Any
import json

class AgendaBuilderAgent:
    """AI-powered agenda builder that suggests meeting topics based on context."""
    
    PROMPT = """
    You are an AI Agenda Builder Agent. Your task is to intelligently create meeting agendas.
    
    Based on the provided context data:
    1. Analyze calendar information (meeting title, participants, previous meetings)
    2. Review recent GitHub activity (PRs, issues, commits)
    3. Examine Slack/communication patterns
    4. Identify current blockers and open tasks
    5. Consider stakeholder priorities and recent updates
    
    Generate a prioritized agenda with:
    - High-priority items (blockers, urgent decisions)
    - Medium-priority items (updates, progress reviews)
    - Low-priority items (planning, discussions)
    
    For each agenda item, provide:
    - Title and brief description
    - Priority level (High/Medium/Low)
    - Estimated time allocation
    - Relevant context/background
    - Key stakeholders involved
    
    Output format: JSON structure with prioritized agenda items.
    """
    
    def __init__(self, config, tools):
        try:
            self.agent = Portia(
                config=config, 
                tools=tools, 
                execution_hooks=CLIExecutionHooks()
            )
            self.has_portia = True
        except:
            self.has_portia = False
    
    def execute(self, context_data: Dict[str, Any], focus_mode: str = "balanced") -> Dict[str, Any]:
        """Generate intelligent agenda based on context."""
        print("📋 Agenda Builder Agent: Creating intelligent agenda...")
        
        if not self.has_portia:
            return self._generate_mock_agenda(context_data, focus_mode)
        
        try:
            focus_instructions = self._get_focus_instructions(focus_mode)
            
            prompt = f"""
            {self.PROMPT}
            
            Focus Mode: {focus_mode}
            {focus_instructions}
            
            Context Data:
            {json.dumps(context_data, indent=2)}
            
            Generate a prioritized agenda for this meeting.
            """
            
            result = self.agent.run(prompt, end_user="agenda_builder")
            
            if result and result.outputs and result.outputs.final_output:
                output = result.outputs.final_output.value
                print("✅ Intelligent agenda created.")
                return self._parse_agenda_response(output)
            else:
                return self._generate_mock_agenda(context_data, focus_mode)
                
        except Exception as e:
            print(f"❌ Agenda generation failed: {e}")
            return self._generate_mock_agenda(context_data, focus_mode)
    
    def _get_focus_instructions(self, focus_mode: str) -> str:
        """Get specific instructions based on focus mode."""
        focus_modes = {
            "blockers": "Prioritize current blockers, technical issues, and urgent decisions that need resolution.",
            "design": "Focus on design updates, architectural decisions, UI/UX reviews, and creative discussions.",
            "progress": "Emphasize progress updates, milestone reviews, and project status discussions.",
            "planning": "Concentrate on future planning, roadmap discussions, and strategic decisions.",
            "balanced": "Create a balanced agenda covering all important aspects proportionally."
        }
        return focus_modes.get(focus_mode, focus_modes["balanced"])
    
    def _parse_agenda_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response into structured agenda format."""
        try:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        # Fallback to structured parsing
        return self._create_fallback_agenda(response)
    
    def _generate_mock_agenda(self, context_data: Dict[str, Any], focus_mode: str) -> Dict[str, Any]:
        """Generate mock agenda when Portia is unavailable."""
        meeting_title = context_data.get('meeting_title', 'Team Meeting')
        participants = context_data.get('participants', [])
        
        base_agenda = {
            "meeting_title": meeting_title,
            "estimated_duration": "60 minutes",
            "focus_mode": focus_mode,
            "agenda_items": []
        }
        
        if focus_mode == "blockers":
            base_agenda["agenda_items"] = [
                {
                    "title": "Critical Blockers Review",
                    "description": "Review and resolve current technical blockers",
                    "priority": "High",
                    "time_allocation": "20 minutes",
                    "stakeholders": participants[:2] if participants else ["Team Lead"],
                    "context": "Address immediate issues preventing progress"
                },
                {
                    "title": "Resource Allocation",
                    "description": "Assign resources to unblock development",
                    "priority": "High", 
                    "time_allocation": "15 minutes",
                    "stakeholders": participants,
                    "context": "Ensure proper resource allocation for critical items"
                }
            ]
        elif focus_mode == "design":
            base_agenda["agenda_items"] = [
                {
                    "title": "Design System Updates",
                    "description": "Review latest design system changes and guidelines",
                    "priority": "High",
                    "time_allocation": "25 minutes",
                    "stakeholders": [p for p in participants if 'design' in p.lower()] or participants[:2],
                    "context": "Align team on design standards and new components"
                },
                {
                    "title": "UI/UX Feedback Session",
                    "description": "Gather feedback on recent interface changes",
                    "priority": "Medium",
                    "time_allocation": "20 minutes",
                    "stakeholders": participants,
                    "context": "Ensure user experience meets requirements"
                }
            ]
        else:  # balanced or other modes
            base_agenda["agenda_items"] = [
                {
                    "title": "Project Status Update",
                    "description": "Review current project progress and milestones",
                    "priority": "High",
                    "time_allocation": "20 minutes",
                    "stakeholders": participants,
                    "context": "Ensure alignment on project progress and timeline"
                },
                {
                    "title": "Technical Discussion",
                    "description": "Address technical challenges and architectural decisions",
                    "priority": "Medium",
                    "time_allocation": "25 minutes",
                    "stakeholders": [p for p in participants if any(role in p.lower() for role in ['dev', 'eng', 'tech'])] or participants,
                    "context": "Resolve technical questions and plan implementation"
                },
                {
                    "title": "Next Steps Planning",
                    "description": "Plan upcoming sprint and assign action items",
                    "priority": "Medium",
                    "time_allocation": "15 minutes",
                    "stakeholders": participants,
                    "context": "Define clear next steps and responsibilities"
                }
            ]
        
        return base_agenda
    
    def _create_fallback_agenda(self, response: str) -> Dict[str, Any]:
        """Create fallback agenda from text response."""
        return {
            "meeting_title": "Generated Meeting",
            "estimated_duration": "60 minutes",
            "focus_mode": "balanced",
            "agenda_items": [
                {
                    "title": "AI-Generated Agenda",
                    "description": response[:200] + "...",
                    "priority": "Medium",
                    "time_allocation": "Full meeting",
                    "stakeholders": ["All participants"],
                    "context": "AI-generated content based on available context"
                }
            ]
        }


class MockAgendaBuilderAgent:
    """Mock version for when Portia is unavailable."""
    
    def __init__(self):
        pass
    
    def execute(self, context_data: Dict[str, Any], focus_mode: str = "balanced") -> Dict[str, Any]:
        agent = AgendaBuilderAgent(None, [])
        return agent._generate_mock_agenda(context_data, focus_mode)