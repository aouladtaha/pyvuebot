import os
from typing import Optional
from fastapi import APIRouter, Request, HTTPException, status
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/telegram", tags=["telegram"])

# Get configuration from environment
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    logger.warning("No TELEGRAM_BOT_TOKEN provided!")

WEB_APP_URL = os.environ.get("WEB_APP_URL", "")
if not WEB_APP_URL:
    logger.warning("No WEB_APP_URL provided!")

# Bot command handlers


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message with the web app button."""
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

    if not WEB_APP_URL:
        await update.message.reply_text(
            "Welcome! However, the web app URL is not configured properly."
        )
        return

    keyboard = [
        [
            InlineKeyboardButton(
                "Open Task Manager",
                web_app=WebAppInfo(url=WEB_APP_URL)
            )
        ]
    ]

    await update.message.reply_text(
        "Welcome to Task Manager Bot! Click the button below to manage your tasks:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    logger.info(f"Start command used by user {update.effective_user.id}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a help message."""
    await update.message.reply_text(
        "This bot helps you manage your tasks. Commands:\n"
        "/start - Start the bot and open the task manager\n"
        "/help - Show this help message\n"
        "/tasks - View your current tasks"
    )
    logger.info(f"Help command used by user {update.effective_user.id}")


async def tasks_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show task manager link."""
    if not WEB_APP_URL:
        await update.message.reply_text(
            "Sorry, the task manager is not configured properly."
        )
        return

    from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

    keyboard = [
        [
            InlineKeyboardButton(
                "Manage Your Tasks",
                web_app=WebAppInfo(url=WEB_APP_URL)
            )
        ]
    ]

    await update.message.reply_text(
        "Click below to view and manage your tasks:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    logger.info(f"Tasks command used by user {update.effective_user.id}")

# Initialize bot application (done once when module loads)
application: Optional[Application] = None


def init_application() -> Optional[Application]:
    """Initialize the bot application with handlers."""
    global application

    if not TOKEN:
        logger.error("Cannot initialize bot: No token provided")
        return None

    if application is not None:
        logger.info("Bot application already initialized")
        return application

    try:
        # Create application
        application = Application.builder().token(TOKEN).build()

        # Add handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("tasks", tasks_command))

        logger.info("Bot application initialized successfully")
        return application
    except Exception as e:
        logger.error(f"Failed to initialize bot application: {e}")
        return None


# Initialize application when module loads
application = init_application()


@router.post("/webhook")
async def webhook(request: Request):
    """Handle incoming updates from Telegram."""
    if not TOKEN:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Bot token not configured"
        )

    try:
        # Get update data
        data = await request.json()
        logger.info(
            f"Received update: {data.get('update_id', 'No update_id')}")

        # Create bot instance
        bot = Bot(token=TOKEN)

        # Process update directly without Application
        update = Update.de_json(data, bot)

        # Handle commands directly
        if update.message and update.message.text:
            text = update.message.text
            if text.startswith('/start'):
                await start_command(update, None)
            elif text.startswith('/help'):
                await help_command(update, None)
            elif text.startswith('/tasks'):
                await tasks_command(update, None)

        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error processing update: {e}")
        return {
            "status": "error",
            "message": str(e)
        }


@router.get("/setup-webhook")
async def setup_webhook(webhook_url: str = None):
    """Setup webhook for the bot."""
    if not TOKEN:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Bot token not configured"
        )

    if not webhook_url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="webhook_url parameter is required"
        )

    try:
        bot = Bot(token=TOKEN)
        # First, delete any existing webhook
        await bot.delete_webhook(drop_pending_updates=True)

        # Set new webhook
        success = await bot.set_webhook(url=webhook_url)
        if success:
            webhook_info = await bot.get_webhook_info()
            logger.info(f"Webhook set to: {webhook_info.url}")
            return {
                "status": "success",
                "message": f"Webhook set to {webhook_url}",
                "webhook_info": {
                    "url": webhook_info.url,
                    "has_custom_certificate": webhook_info.has_custom_certificate,
                    "pending_update_count": webhook_info.pending_update_count,
                }
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to set webhook"
            )
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
