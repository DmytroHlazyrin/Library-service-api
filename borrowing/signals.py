from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Borrowing
from botSend import send_message


@receiver(
    post_save,
    sender=Borrowing,
    dispatch_uid="send_telegram_message_on_borrowing_creation",
)
def send_telegram_message_on_borrowing_creation(
        sender, instance, created, **kwargs
):
    """
    Sends a Telegram message when a new Borrowing instance is created.
    """
    if created:
        message = (f"✅ Created new borrowing:\n"
                   f"ID: {instance.id}\n"
                   f"User {instance.user}:\n"
                   f"Book: {instance.book}\n"
                   f"({instance.borrow_date})")
        send_message(message)
