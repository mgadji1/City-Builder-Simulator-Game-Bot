from models.city import *
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

SHOW_POPULATION_GAME_ACTION = "show_population"
SHOW_MONEY_START_GAME_ACTION = "show_money"
BUILD_GAME_ACTION = "build"
SHOW_HAPPINESS_LEVEL_ACTION = "show_happiness_level"
BACK_ACTION = "back"
START_GAME_ACTION = "start_game"

GAME_STARTED = "game_started"

CITY_KEY = "city"
WAITING_FOR_CITY_NAME = "waiting_for_city_name"
WAITING_FOR_BUILDING_COORDINATES_AND_TYPE = "waiting_for_building_coordinates"

async def back_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == BACK_ACTION:
        context.user_data[WAITING_FOR_BUILDING_COORDINATES_AND_TYPE] = False
        await send_city_actions(update, context)

async def population_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    city = context.user_data.get(CITY_KEY)

    if query.data == SHOW_POPULATION_GAME_ACTION:
        back_button = InlineKeyboardButton(
            text="Back",
            callback_data=BACK_ACTION
        )

        keyboard = [[back_button]]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(text=f"Current population size: {city.population}", reply_markup=reply_markup)

async def money_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    city = context.user_data.get(CITY_KEY)
    city.earn_money()

    if query.data == SHOW_MONEY_START_GAME_ACTION:
        back_button = InlineKeyboardButton(
            text="Back",
            callback_data=BACK_ACTION
        )

        keyboard = [[back_button]]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(text=f"Current money amount: {round(city.money, 2)}", reply_markup=reply_markup)

def get_building_types() -> str:
    text = "Building types:\n"
    for key, values in building_types.items():
        text += f"{key} -> {values}(cost = {building_costs[key]}, income = {building_incomes[key]}, happiness impact = {building_happiness_impact[key]})\n"
    
    return text

async def handle_building_coordinates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get(WAITING_FOR_BUILDING_COORDINATES_AND_TYPE):
        return

    coordinates_and_type = update.message.text.split(" ")
    type = coordinates_and_type[0]
    x = int(coordinates_and_type[1])
    y = int(coordinates_and_type[2])

    city = context.user_data[CITY_KEY]

    build_result = city.build(type, x, y)

    await update.message.reply_text(build_result)

async def build_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    city = context.user_data.get(CITY_KEY)

    if query.data == BUILD_GAME_ACTION:
        context.user_data[WAITING_FOR_BUILDING_COORDINATES_AND_TYPE] = True

        building_types_list = get_building_types()

        back_button = InlineKeyboardButton(
            text="Back",
            callback_data=BACK_ACTION
        )

        keyboard = [[back_button]]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(text=f"City '{city.name}' (E means empty cell): \n\n{city.map.show_city_map()}\n{building_types_list}\nChoose building type and input coordinates(from 1 to 10)\nFormat: <Type> <x> <y>", reply_markup=reply_markup)

async def happiness_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    city = context.user_data.get(CITY_KEY)

    if query.data == SHOW_HAPPINESS_LEVEL_ACTION:
        back_button = InlineKeyboardButton(
            text="Back",
            callback_data=BACK_ACTION
        )

        keyboard = [[back_button]]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(text=f"Current happiness level: {city.happiness}", reply_markup=reply_markup)

async def handle_city_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get(WAITING_FOR_CITY_NAME):
        return
    
    name = update.message.text
    city = City(name)

    context.user_data[CITY_KEY] = city
    context.user_data[WAITING_FOR_CITY_NAME] = False

    await update.message.reply_text(f"City '{name}' created!")

    context.user_data[GAME_STARTED] = True

    await send_city_actions(update, context)

async def create_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.message.reply_text("How would you name your city?")
    context.user_data[WAITING_FOR_CITY_NAME] = True

async def send_city_actions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = context.user_data[CITY_KEY]
    
    if city.is_game_over():
        await handle_game_over(update, context)
        return
    
    if city.is_game_win():
        await handle_game_win(update, context)
        return

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

    happiness_button = InlineKeyboardButton(
        text="Show happiness level",
        callback_data=SHOW_HAPPINESS_LEVEL_ACTION
    )
    
    keyboard = [[population_button, money_button, build_button, happiness_button]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    main_menu_text = "Your goal is to make townspeople happy(hapiness >= 100)\nChoose an action:"

    if update.callback_query:
        query = update.callback_query
        await query.answer()

        await query.edit_message_text(
            text=main_menu_text,
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            text=main_menu_text,
            reply_markup=reply_markup
        )

async def start_simulation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await create_city(update, context)

async def handle_game_over(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_chat.send_message(
        "💀 Your actions led to catastrophe in your city.\nYou lost. Game restarted."
    )

    context.user_data.clear()

    start_button = InlineKeyboardButton(
        text="Start game!",
        callback_data=START_GAME_ACTION
    )

    reply_markup = InlineKeyboardMarkup([[start_button]])

    await update.effective_chat.send_message(
        "Press button to start a new game.",
        reply_markup=reply_markup
    )

async def handle_game_win(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_chat.send_message(
        "🏆 Congratulations!\nYour city has reached a perfect state.\nYou won the game!"
    )

    context.user_data.clear()

    start_button = InlineKeyboardButton(
        text="Start new game",
        callback_data=START_GAME_ACTION
    )

    reply_markup = InlineKeyboardMarkup([[start_button]])

    await update.effective_chat.send_message(
        "Do you want to start a new game?",
        reply_markup=reply_markup
    )
