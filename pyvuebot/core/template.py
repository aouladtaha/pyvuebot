"""Template management for PyVueBot."""
from pathlib import Path
import shutil
from typing import Optional

class TemplateManager:
    """Manages project templates."""
    
    def __init__(self):
        self.templates_dir = Path(__file__).parent.parent / "templates"

    def create_project(self, template_name: str, project_path: Path):
        """Create new project from template."""
        template_path = self.templates_dir / template_name
        if not template_path.exists():
            raise ValueError(f"Template not found: {template_name}")

        shutil.copytree(template_path, project_path)