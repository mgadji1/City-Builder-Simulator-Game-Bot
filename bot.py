import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from simulation import *
from router import *

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
        await start_simulation(update, context)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(CallbackQueryHandler(start_button_callback, pattern=START_GAME_ACTION))
    app.add_handler(CallbackQueryHandler(population_button_callback, pattern=SHOW_POPULATION_GAME_ACTION))
    app.add_handler(CallbackQueryHandler(money_button_callback, pattern=SHOW_MONEY_START_GAME_ACTION))
    app.add_handler(CallbackQueryHandler(build_button_callback, pattern=BUILD_GAME_ACTION))
    app.add_handler(CallbackQueryHandler(back_button_callback, pattern=BACK_ACTION))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_router))

    print("Bot is running")

    app.run_polling()

if __name__ == "__main__":
    main()