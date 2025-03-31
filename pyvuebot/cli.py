"""CLI entry point for PyVueBot."""
import click
import os
import shutil
import json
from pathlib import Path
from .core.project import Project
from .core.template import TemplateManager
from .core.wizard import SetupWizard
from .core.webhook import WebhookManager


@click.group()
def cli():
    """PyVueBot CLI for Telegram Mini Apps."""
    pass

# Existing commands remain the same...


@cli.command()
@click.option("--token", help="Telegram bot token")
@click.option("--url", help="Web app URL")
@click.option("--path", help="Custom webhook path")
@click.option("--delete", is_flag=True, help="Delete webhook instead of setting it")
@click.option("--drop-pending", is_flag=True, help="Drop pending updates when deleting webhook")
def webhook(token, url, path, delete, drop_pending):
    """Set up or delete a Telegram bot webhook."""
    webhook_manager = WebhookManager()

    # Check if we're in a PyVueBot project
    is_pyvuebot_project = webhook_manager.detect_project_type()

    # Handle token
    if not token:
        # Try to get from .env file if we're in a project directory
        env_path = Path.cwd() / ".env"
        if env_path.exists():
            with open(env_path, "r") as f:
                for line in f:
                    if line.strip().startswith("TELEGRAM_BOT_TOKEN="):
                        token_value = line.split(
                            "=", 1)[1].strip().strip('"\'')
                        if token_value:
                            token = token_value
                            click.echo(f"Found bot token in .env file")
                            break

    # If still no token, prompt for it
    if not token:
        token = click.prompt("Telegram bot token", type=str)

    # Handle delete operation
    if delete:
        if click.confirm("Are you sure you want to delete the webhook?", default=False):
            result = webhook_manager.delete_webhook(token, drop_pending)
            if result.get("ok"):
                click.echo("✅ Webhook deleted successfully")
            else:
                click.echo(
                    f"❌ Failed to delete webhook: {result.get('description')}")
        return

    # Get current webhook info
    info = webhook_manager.get_webhook_info(token)
    if info.get("ok") and info.get("result", {}).get("url"):
        current_url = info["result"]["url"]
        click.echo(f"Current webhook URL: {current_url}")
        if not click.confirm("Do you want to set a new webhook URL?", default=True):
            return

    # Handle URL
    if not url:
        if is_pyvuebot_project:
            # Check if there's a vercel.json file with deployed URL
            vercel_path = Path.cwd() / "vercel.json"
            if vercel_path.exists():
                click.echo(
                    "Note: If you've deployed to Vercel, use the deployed URL.")

        url = click.prompt(
            "Web app URL (e.g., https://my-app.vercel.app)", type=str)

    # Handle path
    default_path = "/api/telegram/webhook" if is_pyvuebot_project else None
    if not path:
        if is_pyvuebot_project:
            click.echo(f"Using default webhook path: {default_path}")
            path = default_path
        else:
            path = click.prompt(
                "Webhook path (e.g., /api/webhook)",
                default="/webhook" if not default_path else default_path
            )

    # Set up the webhook
    result = webhook_manager.setup_webhook(token, url, path)

    if result.get("ok"):
        click.echo("✅ Webhook set up successfully")
        webhook_url = f"{url.rstrip('/')}{path}"
        click.echo(f"Webhook URL: {webhook_url}")

        # Save to .env file if we're in a project
        if is_pyvuebot_project:
            try:
                env_path = Path.cwd() / ".env"
                env_content = []

                # Read existing .env content
                if env_path.exists():
                    with open(env_path, "r") as f:
                        env_content = f.readlines()

                # Update environment variables
                updated_token = False
                updated_url = False

                for i, line in enumerate(env_content):
                    if line.strip().startswith("TELEGRAM_BOT_TOKEN="):
                        env_content[i] = f'TELEGRAM_BOT_TOKEN="{token}"\n'
                        updated_token = True
                    elif line.strip().startswith("WEB_APP_URL="):
                        env_content[i] = f'WEB_APP_URL="{url}"\n'
                        updated_url = True

                # Add variables if they don't exist
                if not updated_token:
                    env_content.append(f'TELEGRAM_BOT_TOKEN="{token}"\n')
                if not updated_url:
                    env_content.append(f'WEB_APP_URL="{url}"\n')

                # Write back to .env
                with open(env_path, "w") as f:
                    f.writelines(env_content)

                click.echo("Updated .env file with token and URL")
            except Exception as e:
                click.echo(f"Warning: Could not update .env file: {e}")
    else:
        click.echo(f"❌ Failed to set up webhook: {result.get('description')}")


if __name__ == "__main__":
    cli()
