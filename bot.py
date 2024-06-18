import logging
import os

import django
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from decouple import config
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_service.settings")
django.setup()


TG_BOT_TOKEN = config("TG_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the /start command,
    sending a welcome message along with the user's chat ID.
    """
    chat_id = update.message.chat_id
    await update.message.reply_text(f"🙏Welcome! Your chat_id: {chat_id}")


def main() -> None:
    """
    Sets up the Telegram bot application and
    starts polling for updates. Also, initializes
    the async scheduler.
    """
    app = ApplicationBuilder().token(TG_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    scheduler = AsyncIOScheduler()
    scheduler.start()
    app.run_polling()


if __name__ == "__main__":
    main()
