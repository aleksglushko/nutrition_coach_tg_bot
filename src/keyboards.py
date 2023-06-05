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


feedback_btn = InlineKeyboardButton("Получить фидбек", callback_data="get_feedback")
recipe_btn = InlineKeyboardButton("Получить рецепт", callback_data="get_recipe")
question_btn = InlineKeyboardButton("Задать вопрос", callback_data="ask_question")
recommendation_btn = InlineKeyboardButton("Получить рекомендацию", callback_data="get_recommendation")

feedback_recommendation_question_kb = InlineKeyboardMarkup().add(feedback_btn).add(recommendation_btn).add(question_btn)
recipe_recommendation_kb = InlineKeyboardMarkup().add(recipe_btn).add(recommendation_btn)
