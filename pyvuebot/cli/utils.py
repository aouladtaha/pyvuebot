"""Utility functions for the CLI."""
from pathlib import Path
from typing import Optional


def get_token_from_env(env_path: Optional[Path] = None) -> Optional[str]:
    """Extract bot token from .env file."""
    if not env_path:
        env_path = Path.cwd() / ".env"

    if not env_path.exists():
        return None

    try:
        with open(env_path, "r") as f:
            for line in f:
                if line.strip().startswith("TELEGRAM_BOT_TOKEN="):
                    token_value = line.split("=", 1)[1].strip().strip('"\'')
                    if token_value:
                        return token_value
    except Exception:
        pass

    return None


def update_env_file(env_path: Path, updates: dict) -> bool:
    """Update values in .env file."""
    if not env_path.exists():
        # Create new file with updates
        with open(env_path, "w") as f:
            for key, value in updates.items():
                f.write(f'{key}="{value}"\n')
        return True

    try:
        # Read existing content
        with open(env_path, "r") as f:
            env_content = f.readlines()

        updated_keys = set()

        # Update existing values
        for i, line in enumerate(env_content):
            for key, value in updates.items():
                if line.strip().startswith(f"{key}="):
                    env_content[i] = f'{key}="{value}"\n'
                    updated_keys.add(key)

        # Add missing values
        for key, value in updates.items():
            if key not in updated_keys:
                env_content.append(f'{key}="{value}"\n')

        # Write back
        with open(env_path, "w") as f:
            f.writelines(env_content)

        return True
    except Exception:
        return False
