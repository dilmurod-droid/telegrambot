
from aiogram import types

button_for_lu=types.ReplyKeyboardMarkup(keyboard=[
    [
        types.KeyboardButton(text="vocabulary test ✏️"),
        types.KeyboardButton(text="My Profile 👤")
    ]
],resize_keyboard=True)

admins=types.ReplyKeyboardMarkup(keyboard=[
    [
        types.KeyboardButton(text="Users👥"),
    ]
],resize_keyboard=True)