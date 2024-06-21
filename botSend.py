import requests
from decouple import config

TG_BOT_TOKEN = config("TG_TOKEN")


def send_message(message: str):
    """
    Sends a message to a specified Telegram chat
    using the bot token and chat ID.
    """
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    data = {"chat_id": config("YOUR_CHAT_ID", cast=int), "text": message}
    requests.post(url, data=data)


def send_report(report_lines: list):
    """
    Sends a report by joining a list of report lines into
    a single message and sending it via Telegram.
    """
    message = "\n".join(report_lines)
    send_message(message)
