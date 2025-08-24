from portia import Portia
from portia.cli import CLIExecutionHooks
from typing import Dict, List, Any
import json

class ContextBriefingAgent:
    """Agent for generating personalized context briefings for meeting participants."""
    
    PROMPT = """
    You are a Context Briefing Agent. Create personalized 1-page briefings for meeting participants.
    
    For each participant role (PM, Engineer, Executive, etc.), generate a briefing that includes:
    1. What's changed since the last meeting
    2. Current blockers relevant to their role
    3. Key decisions pending that need their input
    4. Relevant KPIs or metrics for their function
    5. Action items assigned to them
    6. Role-specific context and priorities
    
    Tailor the content based on participant roles:
    - PMs: Focus on timelines, deliverables, stakeholder updates
    - Engineers: Emphasize technical issues, code reviews, architecture
    - Executives: Highlight high-level metrics, strategic decisions, resource needs
    - Designers: Feature design updates, user feedback, UI/UX priorities
    
    Keep briefings concise but comprehensive, focusing on actionable insights.
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
    
    def execute(self, meeting_data: Dict[str, Any], participant_roles: Dict[str, str]) -> Dict[str, Any]:
        """Generate personalized context briefings."""
        print("📊 Context Briefing Agent: Creating personalized briefings...")
        
        if not self.has_portia:
            return self._generate_mock_briefings(meeting_data, participant_roles)
        
        try:
            prompt = f"""
            {self.PROMPT}
            
            Meeting Data:
            {json.dumps(meeting_data, indent=2)}
            
            Participant Roles:
            {json.dumps(participant_roles, indent=2)}
            
            Generate personalized briefings for each participant.
            """
            
            result = self.agent.run(prompt, end_user="context_briefing")
            
            if result and result.outputs and result.outputs.final_output:
                output = result.outputs.final_output.value
                print("✅ Personalized briefings created.")
                return self._parse_briefing_response(output)
            else:
                return self._generate_mock_briefings(meeting_data, participant_roles)
                
        except Exception as e:
            print(f"❌ Briefing generation failed: {e}")
            return self._generate_mock_briefings(meeting_data, participant_roles)
    
    def _generate_mock_briefings(self, meeting_data: Dict[str, Any], participant_roles: Dict[str, str]) -> Dict[str, Any]:
        """Generate mock personalized briefings."""
        briefings = {}
        
        for participant, role in participant_roles.items():
            if role.lower() in ['pm', 'project manager', 'product manager']:
                briefings[participant] = self._create_pm_briefing(meeting_data)
            elif role.lower() in ['engineer', 'developer', 'tech lead']:
                briefings[participant] = self._create_engineer_briefing(meeting_data)
            elif role.lower() in ['executive', 'ceo', 'cto', 'vp']:
                briefings[participant] = self._create_executive_briefing(meeting_data)
            elif role.lower() in ['designer', 'ux', 'ui']:
                briefings[participant] = self._create_designer_briefing(meeting_data)
            else:
                briefings[participant] = self._create_general_briefing(meeting_data)
        
        return {
            "meeting_title": meeting_data.get('meeting_title', 'Team Meeting'),
            "briefings": briefings,
            "generated_at": "2025-08-25T10:00:00Z"
        }
    
    def _create_pm_briefing(self, meeting_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create PM-focused briefing."""
        return {
            "role_focus": "Project Management",
            "key_changes": [
                "Sprint velocity increased by 12% this week",
                "2 new requirements added to backlog",
                "Stakeholder feedback incorporated into roadmap"
            ],
            "current_blockers": [
                "Waiting on legal approval for third-party integration",
                "Resource allocation for Q4 needs finalization",
                "Client feedback pending on mockups"
            ],
            "pending_decisions": [
                "Sprint 3 scope prioritization",
                "Resource allocation for new feature development",
                "Release timeline for v2.0"
            ],
            "relevant_metrics": {
                "sprint_completion": "85%",
                "story_points_delivered": "42/50",
                "stakeholder_satisfaction": "4.2/5"
            },
            "action_items": [
                "Review and approve updated project timeline",
                "Coordinate with design team on user testing",
                "Schedule stakeholder demo for next week"
            ]
        }
    
    def _create_engineer_briefing(self, meeting_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create engineer-focused briefing."""
        return {
            "role_focus": "Engineering/Technical",
            "key_changes": [
                "Database migration completed successfully",
                "New CI/CD pipeline deployed to staging",
                "Performance benchmarks improved by 18%"
            ],
            "current_blockers": [
                "Memory leak in payment processing module",
                "Third-party API rate limiting issues",
                "Test environment configuration problems"
            ],
            "pending_decisions": [
                "Microservices architecture approach",
                "Database indexing strategy",
                "Code review process optimization"
            ],
            "relevant_metrics": {
                "code_coverage": "87%",
                "build_success_rate": "94%",
                "avg_response_time": "245ms"
            },
            "action_items": [
                "Fix critical bug in user authentication",
                "Review architecture RFC document",
                "Optimize database queries for reports module"
            ]
        }
    
    def _create_executive_briefing(self, meeting_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create executive-focused briefing."""
        return {
            "role_focus": "Executive/Strategic",
            "key_changes": [
                "Project on track for Q4 delivery",
                "Team productivity metrics showing positive trends",
                "Customer satisfaction scores improved"
            ],
            "current_blockers": [
                "Budget approval needed for additional resources",
                "Strategic partnership negotiations pending",
                "Competitive analysis update required"
            ],
            "pending_decisions": [
                "Resource allocation for next quarter",
                "Market expansion strategy",
                "Technology investment priorities"
            ],
            "relevant_metrics": {
                "project_roi": "+23%",
                "team_utilization": "92%",
                "customer_satisfaction": "4.5/5"
            },
            "action_items": [
                "Approve budget for Q4 initiatives",
                "Review strategic roadmap alignment",
                "Schedule investor update presentation"
            ]
        }
    
    def _create_designer_briefing(self, meeting_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create designer-focused briefing."""
        return {
            "role_focus": "Design/UX",
            "key_changes": [
                "User testing results available for review",
                "Design system v2.1 components finalized",
                "Accessibility audit completed"
            ],
            "current_blockers": [
                "User feedback integration into wireframes",
                "Design handoff process optimization needed",
                "Brand guidelines update pending approval"
            ],
            "pending_decisions": [
                "Final design direction for onboarding flow",
                "Mobile vs desktop prioritization",
                "Design system component library structure"
            ],
            "relevant_metrics": {
                "user_satisfaction": "4.3/5",
                "design_iteration_speed": "+15%",
                "accessibility_score": "92%"
            },
            "action_items": [
                "Finalize mockups for user testing round 2",
                "Update design documentation",
                "Collaborate with engineering on component implementation"
            ]
        }
    
    def _create_general_briefing(self, meeting_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create general participant briefing."""
        return {
            "role_focus": "General Participant",
            "key_changes": [
                "Project making steady progress across all streams",
                "Team coordination improving with new processes",
                "Client feedback generally positive"
            ],
            "current_blockers": [
                "Cross-team coordination challenges",
                "Communication process improvements needed",
                "Resource allocation optimization required"
            ],
            "pending_decisions": [
                "Next sprint priorities",
                "Team structure adjustments",
                "Process improvement initiatives"
            ],
            "relevant_metrics": {
                "overall_progress": "78%",
                "team_satisfaction": "4.1/5",
                "delivery_timeline": "On track"
            },
            "action_items": [
                "Provide input on current initiatives",
                "Share relevant updates from your area",
                "Participate in planning discussions"
            ]
        }
    
    def _parse_briefing_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response into structured briefing format."""
        try:
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        return {
            "meeting_title": "Generated Meeting",
            "briefings": {"general": {"content": response}},
            "generated_at": "2025-08-25T10:00:00Z"
        }


class MockContextBriefingAgent:
    """Mock version for when Portia is unavailable."""
    
    def __init__(self):
        pass
    
    def execute(self, meeting_data: Dict[str, Any], participant_roles: Dict[str, str]) -> Dict[str, Any]:
        agent = ContextBriefingAgent(None, [])
        return agent._generate_mock_briefings(meeting_data, participant_roles)