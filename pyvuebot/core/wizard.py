"""Setup wizard for interactive project configuration."""
import os
import click
from typing import Dict, Any, List, Optional
from pathlib import Path


class SetupWizard:
    """Interactive setup wizard for project configuration."""

    def __init__(self):
        """Initialize the setup wizard."""
        self.templates_dir = Path(__file__).parent.parent / "templates"

    def get_available_templates(self) -> List[str]:
        """Return a list of available templates."""
        return [d.name for d in self.templates_dir.iterdir() if d.is_dir()]

    def run_wizard(self, project_name: Optional[str] = None) -> Dict[str, Any]:
        """Run the interactive setup wizard to collect project configuration."""
        result = {}

        # Project name
        if project_name:
            result['name'] = project_name
        else:
            result['name'] = click.prompt("Project name", type=str)

        # Template selection
        templates = self.get_available_templates()
        if not templates:
            raise ValueError("No templates available")

        template_index = 1
        click.echo("\nAvailable templates:")
        for i, template in enumerate(templates, 1):
            if template == "task_manager":
                template_index = i
            click.echo(f"{i}. {template}")

        selected = click.prompt(
            "Select template",
            type=click.IntRange(1, len(templates)),
            default=template_index
        )
        result['template'] = templates[selected-1]

        # Project description
        result['description'] = click.prompt(
            "Project description",
            default=f"A Telegram Mini App created with PyVueBot"
        )

        # Additional configurations
        result['setup_bot'] = click.confirm(
            "Do you want to set up a Telegram bot for this project?",
            default=False
        )

        if result['setup_bot']:
            result['bot_token'] = click.prompt(
                "Telegram Bot Token",
                default="",
                show_default=False
            )

        result['setup_database'] = click.confirm(
            "Do you want to set up Supabase integration?",
            default=True
        )

        return result
