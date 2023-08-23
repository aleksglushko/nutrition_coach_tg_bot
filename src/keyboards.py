from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

greet_kb = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(KeyboardButton('Hello! 👋'))

gender_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(KeyboardButton('Male'), KeyboardButton('Female'), KeyboardButton('Other'))

breakfast_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(KeyboardButton('Cereal'), KeyboardButton('Eggs'), KeyboardButton('Joghurt'))

lunch_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(KeyboardButton('Soup'), KeyboardButton('Pasta'), KeyboardButton('Rice'))

dinner_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(KeyboardButton('Salad'), KeyboardButton('Chicken'), KeyboardButton('Fish'))

recomm_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(KeyboardButton('Breakfast'), KeyboardButton('Lunch'), KeyboardButton('Dinner'), KeyboardButton('Snack'))


feedback_btn = InlineKeyboardButton("Get feedback", callback_data="get_feedback")
recipe_btn = InlineKeyboardButton("Get recipe", callback_data="get_recipe")
question_btn = InlineKeyboardButton("Ask me", callback_data="ask_question")
recommendation_btn = InlineKeyboardButton("Get recommendation", callback_data="get_recommendation")

feedback_recommendation_question_kb = InlineKeyboardMarkup().add(feedback_btn).add(recommendation_btn).add(question_btn)
recipe_recommendation_kb = InlineKeyboardMarkup().add(recipe_btn).add(recommendation_btn)
