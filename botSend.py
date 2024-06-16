import requests
from decouple import config

TG_BOT_TOKEN = config("TG_TOKEN")


def send_message(message: str):
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    data = {"chat_id": config("YOUR_CHAT_ID", cast=int), "text": message}
    response = requests.post(url, data=data)


def send_report(report_lines: list):
    message = "\n".join(report_lines)
    send_message(message)
