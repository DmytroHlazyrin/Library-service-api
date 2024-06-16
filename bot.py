import logging
import os

from decouple import config
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_service.settings')  # замените 'your_project_name' на имя вашего проекта
application = get_wsgi_application()

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TG_BOT_TOKEN = config("TG_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    await update.message.reply_text(f"Добро пожаловать! Ваш chat_id: {chat_id}")


def main() -> None:
    app = ApplicationBuilder().token(TG_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    scheduler = AsyncIOScheduler()
    scheduler.start()
    app.run_polling()


if __name__ == "__main__":
    main()
