from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

greet_kb = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(KeyboardButton('Привет! 👋'))

gender_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(KeyboardButton('Мужчина'), KeyboardButton('Женщина'), KeyboardButton('Другое'))

breakfast_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(KeyboardButton('Овсянка'), KeyboardButton('Яйца'), KeyboardButton('Йогурт'))

lunch_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(KeyboardButton('Суп'), KeyboardButton('Паста '), KeyboardButton('Крупа'))

dinner_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(KeyboardButton('Салат'), KeyboardButton('Курица'), KeyboardButton('Рыба'))

recomm_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(KeyboardButton('Завтрак'), KeyboardButton('Обед'), KeyboardButton('Ужин'), KeyboardButton('Перекус'))

recommendation_btn = InlineKeyboardButton("Получить рецепт", callback_data="get_recipe")
feedback_btn = InlineKeyboardButton("Получить фидбек", callback_data="get_feedback")
feedback_recommendation_kb = InlineKeyboardMarkup().add(recommendation_btn).add(feedback_btn)
