from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

import json
import os

# Your bot token (replace with your actual token)
BOT_TOKEN = '7820441579:AAEBag3Ncp53GhJd48BRCg_RzJ9HYi0-IQ4'

# File to store custom responses
RESPONSES_FILE = "responses.json"

# Load existing responses or create an empty dictionary
if os.path.exists(RESPONSES_FILE):
    with open(RESPONSES_FILE, "r") as file:
        responses = json.load(file)
else:
    responses = {
        "hello": "Hi there! How can I assist you?",
        "help": "Sure! What do you need help with?",
        "price": "Our prices start from $10. Let me know what you're looking for.",
        "bot": "I am a Telegram Auto-Responder Bot! Want one for yourself?",
        "hi": "what's going on?",
    }

# Function to save responses to a file
def save_responses():
    with open(RESPONSES_FILE, "w") as file:
        json.dump(responses, file)

# Function to handle the /start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome! I am your Auto-Responder Bot.")

# Function to add new responses
def add_response(update: Update, context: CallbackContext):
    if len(context.args) < 2:
        update.message.reply_text("Usage: /add <keyword> <response>")
        return
    
    keyword = context.args[0].lower()
    response = " ".join(context.args[1:])
    
    responses[keyword] = response
    save_responses()
    
    update.message.reply_text(f"Added response: {keyword} → {response}")

# Function to handle messages
def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text.lower()

    # Check if message contains a keyword
    for keyword in responses:
        if keyword in user_message:
            update.message.reply_text(responses[keyword])
            return

    # Default response
    update.message.reply_text("I'm not sure how to respond to that.")

# Main function to run the bot
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("add", add_response))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
