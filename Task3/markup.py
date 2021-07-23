from aiogram import types

# --- Play Button ---
start_markup = types.InlineKeyboardMarkup()
start_button = types.InlineKeyboardButton('Начать играть', callback_data='play')
start_markup.add(start_button)
