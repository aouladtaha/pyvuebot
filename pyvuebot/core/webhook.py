"""Webhook management for Telegram bot integration."""
import requests
import click
from typing import Dict, Any, Optional
from pathlib import Path


class WebhookManager:
    """Manages Telegram bot webhook setup and configuration."""

    def __init__(self):
        """Initialize the webhook manager."""
        self.telegram_api_base = "https://api.telegram.org/bot"

    def setup_webhook(self, bot_token: str, webapp_url: str, custom_path: Optional[str] = None) -> Dict[str, Any]:
        """Set up a Telegram bot webhook."""
        if not bot_token or not webapp_url:
            raise ValueError("Bot token and web app URL are required")

        # Normalize the webapp URL (remove trailing slash)
        webapp_url = webapp_url.rstrip('/')

        # Determine webhook path
        webhook_path = custom_path if custom_path else "/api/telegram/webhook"

        # Ensure webhook path starts with a slash
        if not webhook_path.startswith('/'):
            webhook_path = f"/{webhook_path}"

        # Construct the full webhook URL
        webhook_url = f"{webapp_url}{webhook_path}"

        # Set up parameters for the API request
        params = {
            "url": webhook_url,
            "max_connections": 40,  # Default value
            # Common update types
            "allowed_updates": ["message", "edited_message", "callback_query"]
        }

        # Make the API request to set the webhook
        api_url = f"{self.telegram_api_base}{bot_token}/setWebhook"
        response = requests.post(api_url, json=params)

        # Parse and return the response
        result = response.json()
        return result

    def get_webhook_info(self, bot_token: str) -> Dict[str, Any]:
        """Get information about the current webhook."""
        if not bot_token:
            raise ValueError("Bot token is required")

        api_url = f"{self.telegram_api_base}{bot_token}/getWebhookInfo"
        response = requests.get(api_url)

        result = response.json()
        return result

    def delete_webhook(self, bot_token: str, drop_pending: bool = False) -> Dict[str, Any]:
        """Delete the current webhook."""
        if not bot_token:
            raise ValueError("Bot token is required")

        api_url = f"{self.telegram_api_base}{bot_token}/deleteWebhook"
        params = {"drop_pending_updates": "true" if drop_pending else "false"}
        response = requests.get(api_url, params=params)

        result = response.json()
        return result

    def detect_project_type(self) -> bool:
        """Determine if current directory is a PyVueBot project."""
        config_path = Path.cwd() / "pyvuebot.json"
        return config_path.exists()
