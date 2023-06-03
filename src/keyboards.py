from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton

greet_kb = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(KeyboardButton('Привет, Коуч! 👋'))

gender_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(KeyboardButton('Мужчина'), KeyboardButton('Женщина'), KeyboardButton('Другое'))

breakfast_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(KeyboardButton('Овсянка'), KeyboardButton('Яйца'), KeyboardButton('Йогурт'))

lunch_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(KeyboardButton('Суп'), KeyboardButton('Паста '), KeyboardButton('Рис'))

dinner_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(KeyboardButton('Салат'), KeyboardButton('Курица'), KeyboardButton('Лосось'))

recomm_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(KeyboardButton('Завтрак'), KeyboardButton('Обед'), KeyboardButton('Ужин'), KeyboardButton('Перекус'))



timezone_options = [
    "America/New_York",    # Eastern Time
    "America/Chicago",     # Central Time
    "America/Denver",      # Mountain Time
    "America/Los_Angeles", # Pacific Time
    "Europe/London",       # British Time
    "Europe/Paris",        # Central European Time
    "Asia/Kolkata",        # Indian Standard Time
    "Asia/Shanghai",       # China Standard Time
    "Asia/Tokyo",          # Japan Standard Time
    "Australia/Sydney",    # Australian Eastern Time
]

timezone_kb = ReplyKeyboardMarkup(resize_keyboard=True)
for timezone in timezone_options:
    timezone_kb.add(KeyboardButton(timezone))

