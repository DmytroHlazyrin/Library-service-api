## Instructions on how to set up a Telegram bot

## 1. Access BotFather
Open Telegram and search for `@BotFather`. This is the official bot to manage your bots.

## 2. Create a bot
Use the `/newbot` command to create a new bot. Follow BotFather's instructions to name and tokenize your bot.

## 3. Add TG_TOKEN to .env
Create a `.env` file in your code directory and add your bot's token there:

```
TG_TOKEN=your_bot_token
```

## 4. Install dependencies from `requirements.txt`.
Make sure you have all the required dependencies installed. Add the following dependencies to your `requirements.txt`:

```
pip install -r requirements.txt
```

```
python-telegram-bot==20.0
python-decouple==3.6
requests==2.28.1
```

## 5. Run bot.py and click on Start, or type /start
Run the `bot.py` script and in Telegram send the command `/start` to your bot. You will receive a message with your `chat_id` in response:

```
Welcome! Your chat_id: 000000000
```

## 6. Add chat_id to .env
Add the received `chat_id` to the `.env` file:

```
YOUR_CHAT_ID=your_chat_id
```

## 7. Example Usage
Create a file `send_message.py` and add the following code to send a message to your bot:

```
[otherfile.py]

import bot

report_lines = [
    "Today's report:",
    "1. Task 1 - overdue",
    "2. Task 2 - completed",
    "3. Task 3 in progress."
    "4. Task 4 is overdue."
]


if __name__ == '__main__':
    bot.send_message("awddawadw112111")
    bot.send_report(report_lines)

```

Run `otherfile.py` to send a message to the specified `chat_id`.

## Example project structure

```
.
├─── .env
├─── bot.py
├─── botSend.py
├─── otherfile.py
└─── requirements.txt
```
