from telegram import Update
from telegram.ext import ContextTypes

from simulation import *

async def message_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get(WAITING_FOR_CITY_NAME):
        await handle_city_name(update, context)
        return
    
    if context.user_data.get(WAITING_FOR_BUILDING_COORDINATES_AND_TYPE):
        await handle_building_coordinates(update, context)
        return