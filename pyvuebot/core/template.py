"""Template management for PyVueBot."""
from pathlib import Path
import shutil
import os
import re
from typing import Dict, Any, Optional


class TemplateManager:
    """Manages project templates and variable substitution."""

    def __init__(self):
        self.templates_dir = Path(__file__).parent.parent / "templates"
        self.template_var_pattern = re.compile(r'{{(.*?)}}')

    def create_project(self, template_name: str, project_path: Path, variables: Dict[str, Any] = None):
        """Create new project from template with variable substitution."""
        template_path = self.templates_dir / template_name
        if not template_path.exists():
            raise ValueError(f"Template not found: {template_name}")

        # Create base project structure
        shutil.copytree(template_path, project_path)

        # Apply template variables if provided
        if variables:
            self._process_template_variables(project_path, variables)

    def _process_template_variables(self, project_path: Path, variables: Dict[str, Any]):
        """Process and replace template variables in all applicable files."""
        # Define which file extensions to process
        text_extensions = {'.py', '.js', '.vue',
                           '.html', '.json', '.md', '.txt', '.toml'}

        for root, _, files in os.walk(project_path):
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix in text_extensions:
                    self._replace_variables_in_file(file_path, variables)

    def _replace_variables_in_file(self, file_path: Path, variables: Dict[str, Any]):
        """Replace template variables in a single file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Replace all template variables
            modified = False
            for match in self.template_var_pattern.finditer(content):
                var_name = match.group(1).strip()
                if var_name in variables:
                    content = content.replace(
                        match.group(0), str(variables[var_name]))
                    modified = True

            # Only write back if changes were made
            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
        except UnicodeDecodeError:
            # Skip binary files
            pass
        except Exception as e:
            print(f"Warning: Could not process {file_path}: {e}")
