"""Webhook management commands for PyVueBot CLI."""
import click
import os
from pathlib import Path
from ...core.webhook import WebhookManager


@click.group()
def webhook():
    """Manage Telegram bot webhooks."""
    pass


@webhook.command("set")
@click.option("--token", help="Telegram bot token")
@click.option("--url", help="Web app URL")
@click.option("--path", help="Custom webhook path")
def set_webhook(token, url, path):
    """Set up a new Telegram bot webhook."""
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


@webhook.command("info")
@click.option("--token", help="Telegram bot token")
def webhook_info(token):
    """Check current webhook status and configuration."""
    webhook_manager = WebhookManager()

    # Handle token
    if not token:
        # Try to get from .env file
        env_path = Path.cwd() / ".env"
        if env_path.exists():
            with open(env_path, "r") as f:
                for line in f:
                    if line.strip().startswith("TELEGRAM_BOT_TOKEN="):
                        token_value = line.split(
                            "=", 1)[1].strip().strip('"\'')
                        if token_value:
                            token = token_value
                            click.echo(f"Using bot token from .env file")
                            break

    # If still no token, prompt for it
    if not token:
        token = click.prompt("Telegram bot token", type=str)

    # Get webhook info
    info = webhook_manager.get_webhook_info(token)

    if info.get("ok"):
        result = info.get("result", {})
        click.echo("📊 Webhook Information:")
        click.echo("─" * 40)

        if result.get("url"):
            click.echo(f"URL: {result.get('url')}")
            click.echo(
                f"Custom certificate: {'Yes' if result.get('has_custom_certificate') else 'No'}")
            click.echo(
                f"Pending updates: {result.get('pending_update_count', 0)}")
            click.echo(f"Max connections: {result.get('max_connections', 40)}")

            if result.get("ip_address"):
                click.echo(f"IP Address: {result.get('ip_address')}")

            if result.get("last_error_date"):
                import datetime
                error_date = datetime.datetime.fromtimestamp(
                    result.get("last_error_date"))
                click.echo(
                    f"Last error: {error_date} - {result.get('last_error_message', 'Unknown error')}")

            click.echo("─" * 40)
            click.echo("✅ Webhook is active")
        else:
            click.echo("❌ No webhook set")
    else:
        click.echo(f"❌ Failed to get webhook info: {info.get('description')}")


@webhook.command("delete")
@click.option("--token", help="Telegram bot token")
@click.option("--drop-pending", is_flag=True, help="Drop pending updates when deleting webhook")
def delete_webhook(token, drop_pending):
    """Delete the current webhook."""
    webhook_manager = WebhookManager()

    # Handle token
    if not token:
        # Try to get from .env file
        env_path = Path.cwd() / ".env"
        if env_path.exists():
            with open(env_path, "r") as f:
                for line in f:
                    if line.strip().startswith("TELEGRAM_BOT_TOKEN="):
                        token_value = line.split(
                            "=", 1)[1].strip().strip('"\'')
                        if token_value:
                            token = token_value
                            click.echo(f"Using bot token from .env file")
                            break

    # If still no token, prompt for it
    if not token:
        token = click.prompt("Telegram bot token", type=str)

    # Get current webhook info first
    info = webhook_manager.get_webhook_info(token)

    if info.get("ok") and info.get("result", {}).get("url"):
        current_url = info["result"]["url"]
        click.echo(f"Current webhook URL: {current_url}")

        if not click.confirm("Are you sure you want to delete this webhook?", default=False):
            click.echo("Operation cancelled.")
            return

        if drop_pending and info["result"].get("pending_update_count", 0) > 0:
            count = info["result"].get("pending_update_count", 0)
            click.echo(
                f"There are {count} pending updates that will be dropped.")
            if not click.confirm("Continue and drop pending updates?", default=False):
                drop_pending = False

    # Delete the webhook
    result = webhook_manager.delete_webhook(token, drop_pending)

    if result.get("ok"):
        click.echo("✅ Webhook deleted successfully")
        if drop_pending:
            click.echo("All pending updates have been dropped")
    else:
        click.echo(f"❌ Failed to delete webhook: {result.get('description')}")
