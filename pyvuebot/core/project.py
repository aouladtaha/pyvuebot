"""Project management for PyVueBot."""
from pathlib import Path
import json
import subprocess
from typing import Optional
from .template import TemplateManager


class Project:
    """Manages Telegram Mini App project operations."""

    def __init__(self, name: str, template: str = "task_manager"):
        self.name = name
        self.template = template
        self.root_path = Path.cwd() / name
        self.config_file = "pyvuebot.json"

    @classmethod
    def load_current(cls) -> "Project":
        """Load project from current directory."""
        current_dir = Path.cwd()
        config_path = current_dir / "pyvuebot.json"

        if not config_path.exists():
            raise ValueError(
                f"Not a PyVueBot project directory (missing {config_path})")

        with config_path.open() as f:
            config = json.load(f)

        project = cls(name=config["name"], template=config["template"])
        project.root_path = current_dir  # Override root_path for existing project
        return project

    def create_structure(self):
        """Create project structure from template."""
        if self.root_path.exists():
            raise ValueError(f"Directory already exists: {self.root_path}")

        template_manager = TemplateManager()
        template_manager.create_project(
            template_name=self.template,
            project_path=self.root_path
        )
        self._create_config()

    def install_dependencies(self):
        """Install project dependencies."""
        if not self.root_path.exists():
            raise ValueError(f"Project directory not found: {self.root_path}")

        npm_result = subprocess.run(
            ["npm", "install"],
            cwd=self.root_path,
            capture_output=True,
            text=True
        )
        if npm_result.returncode != 0:
            raise RuntimeError(f"npm install failed: {npm_result.stderr}")

        req_file = self.root_path / "requirements.txt"
        if req_file.exists():
            pip_result = subprocess.run(
                ["pip", "install", "-r", "requirements.txt"],
                cwd=self.root_path,
                capture_output=True,
                text=True
            )
            if pip_result.returncode != 0:
                raise RuntimeError(f"pip install failed: {pip_result.stderr}")

    def start_dev(self):
        """Start development servers."""
        if not self.root_path.exists():
            raise ValueError(f"Project directory not found: {self.root_path}")
        subprocess.run(["npm", "run", "dev"], cwd=self.root_path)

    def build(self):
        """Build project for production."""
        if not self.root_path.exists():
            raise ValueError(f"Project directory not found: {self.root_path}")
        subprocess.run(["npm", "run", "build"], cwd=self.root_path)

    def deploy(self):
        """Deploy project to Vercel."""
        if not self.root_path.exists():
            raise ValueError(f"Project directory not found: {self.root_path}")
        subprocess.run(["vercel", "--prod"], cwd=self.root_path)

    def _create_config(self):
        """Create project configuration file."""
        config = {
            "name": self.name,
            "template": self.template,
            "version": "0.1.0"
        }

        config_path = self.root_path / self.config_file
        with config_path.open("w") as f:
            json.dump(config, f, indent=2)
