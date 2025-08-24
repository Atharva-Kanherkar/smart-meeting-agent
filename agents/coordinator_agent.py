# agents/coordinator_agent.py

import json
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

    IMPORTANT: ENSURE THE FINAL OUTPUT IS CLEARLY STRUCTURED IN JSON FORMAT OR MARKDOWN.

    Format your response as a well-structured markdown document with clear headings and bullet points.
    """

    def __init__(self, config, tools):
        self.agent = Portia(
            config=config,
            tools=tools,
            execution_hooks=CLIExecutionHooks(),
        )

    def execute(self, calendar_data, people_data, technical_data, slack_data=""):
        """Execute meeting preparation coordination."""
        print("🎯 Agent 6: Coordinating final meeting briefing...")

        try:
            # Process and format input data
            processed_data = self._process_input_data(
                calendar_data, people_data, technical_data, slack_data
            )

            combined_prompt = f"""
            {self.PROMPT}

            Here is the research data from other agents:

            CALENDAR DATA:
            {processed_data['calendar']}

            PEOPLE RESEARCH:
            {processed_data['people']}

            TECHNICAL CONTEXT:
            {processed_data['technical']}

            SLACK COMMUNICATION CONTEXT:
            {processed_data['slack']}

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

                # Format the final output
                return self._format_final_output(output)
            else:
                print("⚠️ No coordinator output returned. Using fallback.")
                return self._create_structured_briefing(processed_data)

        except Exception as e:
            print(f"❌ Coordinator failed: {e}")
            print("🔄 Creating structured briefing...")
            processed_data = self._process_input_data(
                calendar_data, people_data, technical_data, slack_data
            )
            return self._create_structured_briefing(processed_data)

    def _process_input_data(self, calendar_data, people_data, technical_data, slack_data):
        """Process and format input data for better handling."""

        def format_data(data):
            if not data:
                return "No data available"

            if isinstance(data, dict):
                try:
                    return json.dumps(data, indent=2, ensure_ascii=False)
                except (TypeError, ValueError):
                    return str(data)
            elif isinstance(data, list):
                try:
                    return json.dumps(data, indent=2, ensure_ascii=False)
                except (TypeError, ValueError):
                    return "\n".join([str(item) for item in data])
            else:
                return str(data)

        return {
            "calendar": format_data(calendar_data),
            "people": format_data(people_data),
            "technical": format_data(technical_data),
            "slack": format_data(slack_data),
        }

    def _truncate_prompt(self, prompt):
        """Truncate prompt if too long while preserving structure."""
        sections = prompt.split("\n\n")
        truncated_sections = []
        total_length = 0
        max_length = 3500  # Leave room for headers and structure

        for section in sections:
            if total_length + len(section) > max_length:
                remaining_length = max_length - total_length
                if remaining_length > 100:  # Only truncate if we have reasonable space left
                    truncated_sections.append(section[:remaining_length] + "... [truncated]")
                break
            else:
                truncated_sections.append(section)
                total_length += len(section)

        return "\n\n".join(truncated_sections)

    def _format_final_output(self, output):
        """Format the final output for better presentation."""
        if not output:
            return "No output generated"

        formatted_output = output.strip()

        # Ensure proper markdown formatting
        if not formatted_output.startswith("#"):
            formatted_output = f"# Meeting Preparation Briefing\n\n{formatted_output}"

        return formatted_output

    def _create_structured_briefing(self, processed_data):
        """Create a well-structured briefing when the main agent fails."""
        briefing_sections = [
            "# Meeting Preparation Briefing",
            "",
            "## 📅 Meeting Overview",
            self._format_section_content(processed_data["calendar"]),
            "",
            "## 👥 Attendee Information",
            self._format_section_content(processed_data["people"]),
            "",
            "## 🔧 Technical Context",
            self._format_section_content(processed_data["technical"]),
            "",
            "## 💬 Slack Communications",
            self._format_section_content(processed_data["slack"]),
            "",
            "## 🎯 Key Preparation Points",
            "- Review attendee backgrounds and recent work",
            "- Understand technical context and current challenges",
            "- Note recent team discussions and decisions from Slack",
            "- Prepare for likely discussion topics based on all available context",
            "- Consider any action items or follow-ups mentioned in communications",
            "",
            "## 📋 Action Items",
            "- [ ] Review all attendee profiles",
            "- [ ] Prepare talking points for technical discussions",
            "- [ ] Follow up on any pending Slack conversations",
            "- [ ] Gather additional context if needed",
            "",
            "---",
            "*Generated by Smart Meeting Agent - Please review all sections for accuracy.*",
        ]

        return "\n".join(briefing_sections)

    def _format_section_content(self, content):
        """Format section content with proper indentation and structure."""
        if content == "No data available":
            return "*No information available for this section.*"

        # If content looks like JSON, try to format it better
        try:
            if content.strip().startswith(("{", "[")):
                parsed = json.loads(content)
                if isinstance(parsed, dict):
                    formatted_items = []
                    for key, value in parsed.items():
                        formatted_items.append(f"- **{key}**: {value}")
                    return "\n".join(formatted_items)
                elif isinstance(parsed, list):
                    return "\n".join([f"- {item}" for item in parsed])
        except (json.JSONDecodeError, TypeError):
            pass

        # For regular text, add some basic formatting
        lines = content.split("\n")
        formatted_lines = []

        for line in lines:
            line = line.strip()
            if line:
                if line.startswith("-") or line.startswith("*"):
                    formatted_lines.append(line)
                else:
                    formatted_lines.append(f"- {line}")

        return "\n".join(formatted_lines) if formatted_lines else "*No content available.*"


class SimpleCoordinatorAgent:
    """Simplified coordinator that doesn't rely on LLM calls."""

    def __init__(self, config, tools):
        pass

    def execute(self, calendar_data, people_data, technical_data, slack_data=""):
        """Create a simple structured briefing."""

        def format_json_data(data):
            """Format data as JSON if possible, otherwise as string."""
            if isinstance(data, (dict, list)):
                try:
                    return json.dumps(data, indent=2, ensure_ascii=False)
                except (TypeError, ValueError):
                    return str(data)
            return str(data) if data else "No data available"

        return f"""# Meeting Preparation Briefing

## 📅 Meeting Overview
{format_json_data(calendar_data)}

## 👥 Attendee Information
{format_json_data(people_data)}

## 🔧 Technical Context
{format_json_data(technical_data)}

## 💬 Slack Communications
{format_json_data(slack_data)}

## 🎯 Key Preparation Points
- Review attendee backgrounds and recent work
- Understand technical context and current challenges
- Note recent team discussions and decisions from Slack
- Prepare for likely discussion topics based on all available context
- Consider any action items or follow-ups mentioned in communications

## 📋 Recommended Actions
- [ ] Study attendee profiles and their recent contributions
- [ ] Prepare technical talking points and questions
- [ ] Review recent Slack discussions for context
- [ ] Identify potential collaboration opportunities
- [ ] Prepare follow-up items for post-meeting

---
*Generated by Smart Meeting Agent - {self._get_timestamp()}*
"""

    def _get_timestamp(self):
        """Get current timestamp for the briefing."""
        from datetime import datetime

        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
