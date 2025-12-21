from ui.city_ui import *
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

SHOW_POPULATION_GAME_ACTION = "show_population"
SHOW_MONEY_START_GAME_ACTION = "show_money"
BUILD_GAME_ACTION = "build"

CITY_KEY = "city"
WAITING_FOR_CITY_NAME = "waiting_for_city_name"

async def population_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    city = context.user_data.get(CITY_KEY)

    if (query.data == SHOW_POPULATION_GAME_ACTION):
        await query.edit_message_text(f"Current population size: {city.population}")

async def money_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if (query.data == SHOW_MONEY_START_GAME_ACTION):
        await query.edit_message_text("Money")

async def build_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if (query.data == BUILD_GAME_ACTION):
        await query.edit_message_text("Build")

async def handle_city_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get(WAITING_FOR_CITY_NAME):
        return
    
    name = update.message.text
    city = City(name)

    context.user_data[CITY_KEY] = city
    context.user_data[WAITING_FOR_CITY_NAME] = False

    await update.message.reply_text(f"City '{name}' created!")

    await send_city_actions(update, context)

async def create_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.message.reply_text("How would you name your city?")
    context.user_data[WAITING_FOR_CITY_NAME] = True

async def send_city_actions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    population_button = InlineKeyboardButton(
        text="Show population",
        callback_data=SHOW_POPULATION_GAME_ACTION
    )

    money_button = InlineKeyboardButton(
        text="Show money",
        callback_data=SHOW_MONEY_START_GAME_ACTION
    )

    build_button = InlineKeyboardButton(
        text="Build",
        callback_data=BUILD_GAME_ACTION
    )
    
    keyboard = [[population_button, money_button, build_button]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        text="Choose an action:",
        reply_markup=reply_markup
    )

async def start_simulation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await create_city(update, context)