from portia import Portia
from portia.cli import CLIExecutionHooks
from typing import Dict, List, Any
import json

class PreReadCollectorAgent:
    """Agent for collecting relevant documents and generating pre-read packets."""
    
    PROMPT = """
    You are a Pre-Read Document Collector Agent. Your task is to gather all relevant documents for meeting preparation.
    
    Based on meeting context and participant information:
    1. Search for GitHub PRs and issues involving participants
    2. Find relevant documentation pages (Notion, Confluence, etc.)
    3. Identify Slack/Teams discussions related to meeting topics
    4. Collect recent updates and changes relevant to the meeting
    5. Prioritize documents by relevance and importance
    
    For each document, provide:
    - Document title and type
    - Source (GitHub, Notion, Slack, etc.)
    - Relevance score (1-10)
    - Brief summary
    - Key points for meeting preparation
    - Direct link/reference
    
    Focus on actionable content that will help participants prepare effectively.
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
    
    def execute(self, meeting_context: Dict[str, Any]) -> Dict[str, Any]:
        """Collect relevant pre-read documents."""
        print("📚 Pre-Read Collector Agent: Gathering relevant documents...")
        
        if not self.has_portia:
            return self._generate_mock_preread(meeting_context)
        
        try:
            prompt = f"""
            {self.PROMPT}
            
            Meeting Context:
            {json.dumps(meeting_context, indent=2)}
            
            Find and prioritize relevant documents for this meeting.
            """
            
            result = self.agent.run(prompt, end_user="preread_collector")
            
            if result and result.outputs and result.outputs.final_output:
                output = result.outputs.final_output.value
                print("✅ Pre-read documents collected.")
                return self._parse_preread_response(output)
            else:
                return self._generate_mock_preread(meeting_context)
                
        except Exception as e:
            print(f"❌ Pre-read collection failed: {e}")
            return self._generate_mock_preread(meeting_context)
    
    def _generate_mock_preread(self, meeting_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock pre-read packet."""
        meeting_title = meeting_context.get('meeting_title', 'Team Meeting')
        participants = meeting_context.get('participants', [])
        
        return {
            "meeting_title": meeting_title,
            "preread_summary": "Essential documents and updates for meeting preparation",
            "documents": [
                {
                    "title": "Project Status Dashboard",
                    "type": "Dashboard",
                    "source": "Internal Tools",
                    "relevance_score": 9,
                    "summary": "Current project metrics, progress indicators, and key performance data",
                    "key_points": [
                        "Sprint progress: 75% complete",
                        "3 critical issues pending resolution", 
                        "Performance metrics showing 15% improvement"
                    ],
                    "link": "https://dashboard.internal.com/project-status",
                    "last_updated": "2 hours ago"
                },
                {
                    "title": "Technical Architecture RFC",
                    "type": "Technical Document",
                    "source": "GitHub",
                    "relevance_score": 8,
                    "summary": "Proposed changes to system architecture and implementation approach",
                    "key_points": [
                        "Migration to microservices architecture",
                        "Database optimization strategies",
                        "API versioning approach"
                    ],
                    "link": "https://github.com/team/rfcs/pull/42",
                    "last_updated": "1 day ago"
                },
                {
                    "title": "Design System Updates",
                    "type": "Design Documentation",
                    "source": "Figma/Notion",
                    "relevance_score": 7,
                    "summary": "Latest changes to design system components and guidelines",
                    "key_points": [
                        "New button component variants",
                        "Updated color palette",
                        "Accessibility improvements"
                    ],
                    "link": "https://notion.so/design-system-v2.1",
                    "last_updated": "3 days ago"
                },
                {
                    "title": "Recent Slack Discussions",
                    "type": "Communication Thread",
                    "source": "Slack",
                    "relevance_score": 6,
                    "summary": "Key discussions and decisions from relevant Slack channels",
                    "key_points": [
                        "Performance optimization approaches discussed",
                        "Deployment timeline concerns raised",
                        "Resource allocation decisions pending"
                    ],
                    "link": "slack://channel?team=T123&id=C456",
                    "last_updated": "6 hours ago"
                }
            ],
            "action_items_context": [
                "Review architecture RFC before technical discussion",
                "Prepare feedback on design system changes",
                "Come ready with performance optimization ideas",
                "Consider resource allocation proposals"
            ]
        }
    
    def _parse_preread_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response into structured pre-read format."""
        try:
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        # Fallback parsing
        return {
            "meeting_title": "Generated Meeting",
            "preread_summary": response[:300] + "...",
            "documents": [],
            "action_items_context": ["Review AI-generated summary"]
        }


class MockPreReadCollectorAgent:
    """Mock version for when Portia is unavailable."""
    
    def __init__(self):
        pass
    
    def execute(self, meeting_context: Dict[str, Any]) -> Dict[str, Any]:
        agent = PreReadCollectorAgent(None, [])
        return agent._generate_mock_preread(meeting_context)