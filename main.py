from telegram.ext import (Updater, Filters, CallbackContext,CommandHandler, MessageHandler,ConversationHandler)
from telegram import KeyboardButton, ReplyKeyboardMarkup  , Update

from data_sourse import DataSource
import os, threading, time, datetime

ENTER_MESSAGE, ENTER_TIME = range(2)
dataSource = DataSource(os.environ.get("DATABASE_URL"))
TOKEN = os.getenv('TOKEN')

URL = "postgres://telegram_bot_user:password@localhost:5432/telegram_bot_01"


ADD_REMINDER_TEXT = 'Add a reminder⏰'
INTERVAL = 30


def start_handler(update, context):
    update.message.reply_text("Hello, creator!", reply_markup=add_reminder_button())

def add_reminder_button():
    keyboard = [[KeyboardButton(ADD_REMINDER_TEXT)]]
    return ReplyKeyboardMarkup(keyboard)

def add_reminder_handler(update:Update, context: CallbackContext):
    update.message.reply_text('Please enter a message for the reminder:')
    return ENTER_MESSAGE

def enter_message_handler(update:Update, context: CallbackContext):
    context.user_data["message_text"]= update.message.text
    update.message.reply_text('Please enter a time for the reminder (format: DD/MM/YYYY HH:MM):')
    return ENTER_TIME

def enter_time_handler(update:Update, context: CallbackContext):
    message_text = context.user_data["message_text"]
    try:
        time = datetime.datetime.strptime(update.message.text, '%d/%m/%Y %H:%M')
        message_data= dataSource.create_reminder(update.message.chat_id, message_text, time)
        update.message.reply_text("Your reminder has been set: " + message_data.__repr__())
    except ValueError:
        updates.message.reply_text("Invalid date format. Please use DD/MM/YYYY HH:MM.")
        return ENTER_TIME
    return ConversationHandler.END

def start_check_reminders_task():
    thread = threading.Thread(target=check_reminders,daemon=True)
    thread.start()

def check_reminders():
    while True:
        for reminder_data in dataSource.get_all_reminders():
            if reminder_data.should_be_fired():
                dataSource.fire_reminder(reminder_data.reminder_id)
                updater.bot.send_message(reminder_data.chat_id,reminder_data.message)
        time.sleep(INTERVAL)

if __name__ == '__main__':
    PORT = int(os.environ.get("PORT", 80))
    updater = Updater(TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler("start", start_handler))
    conv_handler = ConversationHandler (
        entry_points=[MessageHandler(Filters.regex(ADD_REMINDER_TEXT), add_reminder_handler)],
        states={
            ENTER_MESSAGE: [MessageHandler(Filters.text & ~Filters.command, enter_message_handler)],
            ENTER_TIME: [MessageHandler(Filters.text & ~Filters.command, enter_time_handler)]
        },
        fallbacks=[]
    )
    updater.dispatcher.add_handler(conv_handler)
    dataSource.create_tables()
    start_check_reminders_task()
    webhook_url = f"https://test-bot-tt8t.onrender.com/{TOKEN}"  # Replace with your actual URL
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    updater.bot.set_webhook(webhook_url)
    updater.idle()
