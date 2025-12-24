import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from simulation import *
from router import *

load_dotenv()

TOKEN = os.getenv("TOKEN")

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

    if query.data == START_GAME_ACTION:
        await query.edit_message_text("Game started!")
        await start_simulation(update, context)

async def actions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get(GAME_STARTED):
        await update.message.reply_text(text="Start game first!")
        return
    
    await send_city_actions(update, context)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start - starts game\n/help - prints bot commands\n/actions - prints city actions")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("actions", actions))
    app.add_handler(CommandHandler("help", help))

    app.add_handler(CallbackQueryHandler(start_button_callback, pattern=START_GAME_ACTION))
    app.add_handler(CallbackQueryHandler(population_button_callback, pattern=SHOW_POPULATION_GAME_ACTION))
    app.add_handler(CallbackQueryHandler(money_button_callback, pattern=SHOW_MONEY_START_GAME_ACTION))
    app.add_handler(CallbackQueryHandler(build_button_callback, pattern=BUILD_GAME_ACTION))
    app.add_handler(CallbackQueryHandler(happiness_button_callback, pattern=SHOW_HAPPINESS_LEVEL_ACTION))
    app.add_handler(CallbackQueryHandler(back_button_callback, pattern=BACK_ACTION))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_router))

    print("Bot is running")

    app.run_polling()

if __name__ == "__main__":
    main()