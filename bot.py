import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, Application, CommandHandler, CallbackQueryHandler

load_dotenv()

TOKEN = os.getenv("TOKEN")

START_GAME_ACTION = "start_game"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_button = InlineKeyboardButton(
        text="Start game!",
        callback_data=START_GAME_ACTION
    )
    
    keyboard = [[start_button]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Hello! Welcome to City Builder Simulator! Press button to start!",
        reply_markup=reply_markup
    )

async def start_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if (query.data == START_GAME_ACTION):
        await query.edit_message_text("Game started!")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(start_button_callback))

    print("Bot is running")

    app.run_polling()

if __name__ == "__main__":
    main()