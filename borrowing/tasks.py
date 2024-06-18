from datetime import datetime

from celery import shared_task

from borrowing.models import Borrowing
from botSend import send_report, send_message


@shared_task
def get_borrowing_report():
    """
    Generates a report of borrowings that will expire soon and those that have
    already expired.
    Sends a formatted message with the report details via Telegram.
    """
    borrowings = Borrowing.objects.filter(actual_return_date=None)
    will_be_expired_soon = []
    already_expired = []

    now = datetime.now().date()
    for borrowing in borrowings:
        book_title = borrowing.book.title
        borrowing_date = borrowing.borrow_date.strftime("%Y-%m-%d")
        expected_return_date = borrowing.expected_return_date.strftime(
            "%Y-%m-%d")
        borrowing_id = str(borrowing.id)
        email = borrowing.user.email

        days_until_due = (borrowing.expected_return_date - now).days

        string = (
            f"Book: {book_title}"
            f"\n    Borrowed on: {borrowing_date}"
            f"\n    Due: {expected_return_date}"
            f"\n    Borrowing ID: {borrowing_id}"
            f"\n    From: {email}"
        )
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
