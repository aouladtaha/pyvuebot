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
        
        # Ask about configuring environment variables
        result['setup_env'] = click.confirm(
            "Do you want to configure environment variables now?", 
            default=False
        )
        
        # Environment variables dictionary
        result['env_vars'] = {}
        
        if result['setup_env']:
            # Parse .env.example from the selected template if it exists
            env_example_path = self.templates_dir / result['template'] / ".env.example"
            if env_example_path.exists():
                env_vars = self._parse_env_example(env_example_path)
                
                click.echo("\nPlease provide values for the environment variables:")
                for key, default in env_vars.items():
                    # If default is empty string, show no default
                    hide_default = default == ""
                    result['env_vars'][key] = click.prompt(
                        f"{key}", 
                        default=default,
                        show_default=not hide_default
                    )
        
        return result
    
    def _parse_env_example(self, env_path: Path) -> Dict[str, str]:
        """Parse .env.example file to extract variable names and default values."""
        env_vars = {}
        try:
            with open(env_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                        
                    if "=" in line:
                        key, value = line.split("=", 1)
                        # Remove quotes from value if present
                        value = value.strip().strip('"\'')
                        env_vars[key.strip()] = value
        except Exception as e:
            click.echo(f"Warning: Could not parse environment example file: {e}")
        
        return env_vars