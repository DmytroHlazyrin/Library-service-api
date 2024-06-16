from datetime import datetime
import logging
import os
import django

from decouple import config
from botSend import send_report, send_message

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_service.settings')
django.setup()

from borrowing.models import Borrowing

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
    await update.message.reply_text(f"🙏Добро пожаловать! Ваш chat_id: {chat_id}")


def main() -> None:
    app = ApplicationBuilder().token(TG_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    scheduler = AsyncIOScheduler()
    scheduler.start()
    app.run_polling()


def get_borrowing_report():
    borrowings = Borrowing.objects.filter(actual_return_date=None)
    will_be_expired_soon = []
    already_expired = []

    now = datetime.now().date()
    for borrowing in borrowings:
        book_title = borrowing.book.title
        borrowing_date = borrowing.borrow_date.strftime("%Y-%m-%d")
        expected_return_date = borrowing.expected_return_date.strftime("%Y-%m-%d")
        borrowing_id = str(borrowing.id)
        email = borrowing.user.email

        days_until_due = (borrowing.expected_return_date - now).days

        string = (f"Book: {book_title}"
                  f"\n    Borrowed on: {borrowing_date}"
                  f"\n    Due: {expected_return_date}"
                  f"\n    Borrowing ID: {borrowing_id}"
                  f"\n    From: {email}")
        if days_until_due == 1:
            will_be_expired_soon.append(string)
        elif days_until_due <= 0:
            already_expired.append(string)

    report_lines = []

    if already_expired:
        if report_lines:
            report_lines.append("")
        report_lines.append("❌ Already expired:")
        for i, item in enumerate(already_expired, 1):
            report_lines.append(f"{i}. {item}")

    if will_be_expired_soon:
        report_lines.append("📅 Will be expired soon:")
        for i, item in enumerate(will_be_expired_soon, 1):
            report_lines.append(f"\t{i}. {item}")

    if report_lines:
        send_report(report_lines)
    else:
        send_message("No borrowings are due soon or already expired.")


if __name__ == "__main__":
    main()
