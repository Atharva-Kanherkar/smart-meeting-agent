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
    4. Key Discussion Points (likely topics based on context)
    5. Preparation Recommendations (what to review or prepare)
    
    Keep the briefing concise but comprehensive, focusing on actionable insights.
    """
    
    def __init__(self, config, tools):
        self.agent = Portia(
            config=config, 
            tools=tools, 
            execution_hooks=CLIExecutionHooks()
        )
    
    def execute(self, calendar_data, people_data, technical_data):
        """Execute meeting preparation coordination."""
        print("🎯 Agent 4: Coordinating final meeting briefing...")
        
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
                print("⚠️ No briefing generated. Creating simple briefing.")
                return self._create_simple_briefing(calendar_data, people_data, technical_data)
                
        except Exception as e:
            print(f"❌ Coordination failed: {e}")
            print("🔄 Creating fallback briefing...")
            return self._create_simple_briefing(calendar_data, people_data, technical_data)
    
    def _truncate_prompt(self, prompt):
        """Truncate prompt if too long while preserving structure."""
        # Keep the main prompt and truncate the data sections
        lines = prompt.split('\n')
        truncated_lines = []
        
        for line in lines:
            if len('\n'.join(truncated_lines)) > 3500:
                truncated_lines.append("... [data truncated for brevity] ...")
                break
            truncated_lines.append(line)
        
        return '\n'.join(truncated_lines)
    
    def _create_simple_briefing(self, calendar_data, people_data, technical_data):
        """Create a simple briefing when the main agent fails."""
        
        # Extract meeting title from calendar data
        meeting_title = "Meeting"
        if "Title:" in calendar_data:
            title_line = [line for line in calendar_data.split('\n') if 'Title:' in line]
            if title_line:
                meeting_title = title_line[0].split('Title:')[1].strip()
        
        # Count attendees
        attendee_count = calendar_data.count('@') if calendar_data else 0
        
        briefing = f"""
# 📋 Meeting Preparation Briefing

## 📅 Meeting Overview
**Meeting:** {meeting_title}
**Attendees:** {attendee_count} participants
**Status:** Preparation completed

## 👥 Attendee Summary
{self._extract_attendee_summary(people_data)}

## 🔧 Technical Context
{self._extract_technical_summary(technical_data)}

## 📝 Key Preparation Points
- Review attendee backgrounds and roles
- Familiarize yourself with technical context
- Prepare discussion points based on meeting topic
- Consider follow-up actions and next steps

## 🎯 Meeting Objectives
Based on the context, this appears to be a {meeting_title} discussion focusing on:
- Technical implementation details
- Project coordination and planning
- Stakeholder alignment and decision-making

---
*This briefing was automatically generated from calendar, people, and technical research.*
        """.strip()
        
        return briefing
    
    def _extract_attendee_summary(self, people_data: str) -> str:
        """Extract a simple attendee summary."""
        if not people_data or len(people_data.strip()) == 0:
            return "Attendee research data not available."
        
        # Extract key points from people data
        lines = people_data.split('\n')
        summary_lines = []
        
        for line in lines:
            if '@' in line or 'Role:' in line or 'Background:' in line:
                summary_lines.append(line.strip())
                if len(summary_lines) >= 10:  # Limit to key points
                    break
        
        return '\n'.join(summary_lines) if summary_lines else "Attendee information processed."
    
    def _extract_technical_summary(self, technical_data: str) -> str:
        """Extract a simple technical summary."""
        if not technical_data or len(technical_data.strip()) == 0:
            return "Technical context data not available."
        
        # Extract key technical points
        lines = technical_data.split('\n')
        summary_lines = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['project', 'technical', 'system', 'technology', 'development']):
                summary_lines.append(line.strip())
                if len(summary_lines) >= 8:  # Limit to key points
                    break
        
        return '\n'.join(summary_lines) if summary_lines else "Technical context processed."


class SimpleCoordinatorAgent:
    """Simplified coordinator that doesn't rely on LLM calls."""
    
    def __init__(self, config=None, tools=None):
        # Don't initialize Portia to avoid potential issues
        pass
    
    def execute(self, calendar_data, people_data, technical_data):
        """Create briefing without LLM calls."""
        print("🎯 Agent 4: Creating meeting briefing (simplified mode)...")
        
        try:
            briefing = self._create_comprehensive_briefing(calendar_data, people_data, technical_data)
            print("✅ Meeting briefing completed.")
            print(f"Preview: {briefing[:200]}...")
            return briefing
        except Exception as e:
            print(f"❌ Briefing creation failed: {e}")
            return "Meeting briefing could not be generated due to technical issues."
    
    def _create_comprehensive_briefing(self, calendar_data, people_data, technical_data):
        """Create a comprehensive briefing using template-based approach."""
        
        from datetime import datetime
        
        # Parse the input data
        meetings = self._parse_calendar_data(calendar_data)
        attendees = self._parse_people_data(people_data)
        tech_context = self._parse_technical_data(technical_data)
        
        # Generate briefing sections
        overview = self._format_meeting_overview(meetings)
        profiles = self._format_attendee_profiles(attendees)
        discussion_points = self._generate_discussion_points(meetings, tech_context)
        
        # Combine into comprehensive briefing
        briefing = f"""
# 📋 Meeting Briefing - {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 📅 Meeting Overview
{overview}

## 👥 Attendee Profiles
{profiles}

## 🔧 Technical Context
{tech_context}

## 🎯 Key Discussion Points
{discussion_points}

## 📝 Preparation Recommendations
- Review attendee backgrounds and their recent work
- Familiarize yourself with the technical context and current project status
- Prepare questions about project progress and next steps
- Consider potential blockers and solutions
- Think about resource allocation and timeline implications

## 🚀 Meeting Success Factors
- Clear agenda and objectives
- Active participation from all attendees
- Actionable outcomes and next steps
- Follow-up plan and timeline

---
*Generated by Smart Meeting Agent*
        """.strip()
        
        return briefing
    
    def _parse_calendar_data(self, calendar_data):
        """Parse calendar data into structured format."""
        meetings = []
        if not calendar_data:
            return meetings
        
        # Extract meeting information
        lines = calendar_data.split('\n')
        current_meeting = {}
        
        for line in lines:
            line = line.strip()
            if line.startswith('**Meeting') and line.endswith(':**'):
                if current_meeting:
                    meetings.append(current_meeting)
                current_meeting = {}
            elif 'Title:' in line:
                current_meeting['title'] = line.split('Title:')[1].strip()
            elif 'Date:' in line:
                current_meeting['date'] = line.split('Date:')[1].strip()
            elif 'Time:' in line:
                current_meeting['time'] = line.split('Time:')[1].strip()
            elif 'Attendees:' in line:
                attendees = line.split('Attendees:')[1].strip()
                current_meeting['attendees'] = [email.strip() for email in attendees.split(',')]
            elif 'Location:' in line:
                current_meeting['location'] = line.split('Location:')[1].strip()
            elif 'Context:' in line:
                current_meeting['context'] = line.split('Context:')[1].strip()
        
        if current_meeting:
            meetings.append(current_meeting)
        
        return meetings
    
    def _parse_people_data(self, people_data):
        """Parse people data into list of attendees."""
        attendees = []
        if not people_data:
            return attendees
        
        # Extract attendee information
        lines = people_data.split('\n')
        current_person = {}
        
        for line in lines:
            line = line.strip()
            if '@' in line and line.startswith('**') and line.endswith(')**'):
                if current_person:
                    attendees.append(current_person)
                # Extract name and email
                parts = line.strip('*').split('(')
                if len(parts) >= 2:
                    email = parts[0].strip()
                    name = parts[1].rstrip(')').strip()
                    current_person = {'email': email, 'name': name}
                else:
                    current_person = {'email': line.strip('*'), 'name': 'Unknown'}
            elif 'Role:' in line:
                current_person['role'] = line.split('Role:')[1].strip()
            elif 'Background:' in line:
                current_person['background'] = line.split('Background:')[1].strip()
            elif 'Expertise:' in line:
                current_person['expertise'] = line.split('Expertise:')[1].strip()
            elif 'Context:' in line:
                current_person['context'] = line.split('Context:')[1].strip()
        
        if current_person:
            attendees.append(current_person)
        
        return attendees
    
    def _parse_technical_data(self, technical_data):
        """Parse and summarize technical data."""
        if not technical_data:
            return "No technical context available"
        
        # Extract key technical information
        lines = technical_data.split('\n')
        key_points = []
        
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['project', 'system', 'technology', 'framework', 'language']):
                if line and not line.startswith('#'):
                    key_points.append(f"• {line}")
                    if len(key_points) >= 5:
                        break
        
        return '\n'.join(key_points) if key_points else "Technical context analysis completed"
    
    def _format_meeting_overview(self, meetings):
        """Format meeting overview section."""
        if not meetings:
            return "No upcoming meetings found."
        
        overview_parts = []
        for i, meeting in enumerate(meetings, 1):
            title = meeting.get('title', 'Untitled Meeting')
            date = meeting.get('date', 'TBD')
            time = meeting.get('time', 'TBD')
            location = meeting.get('location', 'TBD')
            attendee_count = len(meeting.get('attendees', []))
            
            overview_parts.append(f"""
**Meeting {i}: {title}**
- 📅 Date: {date}
- ⏰ Time: {time}
- 📍 Location: {location}
- 👥 Attendees: {attendee_count} participants
            """.strip())
        
        return '\n\n'.join(overview_parts)
    
    def _format_attendee_profiles(self, attendees):
        """Format attendee profiles section."""
        if not attendees:
            return "No attendee information available."
        
        profiles = []
        for attendee in attendees:
            name = attendee.get('name', 'Unknown')
            email = attendee.get('email', 'Unknown')
            role = attendee.get('role', 'Unknown')
            background = attendee.get('background', 'Not specified')
            
            profiles.append(f"""
**{name}** ({email})
- Role: {role}
- Background: {background}
            """.strip())
        
        return '\n\n'.join(profiles)
    
    def _generate_discussion_points(self, meetings, tech_context):
        """Generate likely discussion points."""
        points = []
        
        # Add meeting-specific points
        for meeting in meetings:
            title = meeting.get('title', '')
            context = meeting.get('context', '')
            
            if 'gsoc' in title.lower() or 'gsoc' in context.lower():
                points.extend([
                    "Google Summer of Code project progress review",
                    "Student developer milestone achievements",
                    "Mentor feedback and guidance",
                    "Timeline and deliverable discussions"
                ])
            
            if 'workflow' in title.lower() or 'workflow' in context.lower():
                points.extend([
                    "Workflow system architecture and design",
                    "Implementation challenges and solutions",
                    "Performance optimization strategies",
                    "Integration requirements and dependencies"
                ])
        
        # Add general technical discussion points
        if 'project' in tech_context.lower():
            points.extend([
                "Technical requirements and specifications",
                "Code review and quality assurance",
                "Testing strategies and coverage",
                "Documentation and knowledge sharing"
            ])
        
        # Remove duplicates and limit to most relevant
        unique_points = list(dict.fromkeys(points))[:8]
        
        if not unique_points:
            unique_points = [
                "Project status updates and progress review",
                "Technical challenges and proposed solutions",
                "Resource allocation and timeline planning", 
                "Next steps and action items"
            ]
        
        return '\n'.join([f"• {point}" for point in unique_points])