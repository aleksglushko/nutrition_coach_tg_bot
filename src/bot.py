import asyncio
import logging
import os
import database
import openai_api
import keyboards as kb

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from datetime import datetime
from dotenv import load_dotenv
from messages import MESSAGES
from prompts import PROMPTS
from tools import if_simmilar
from stickers import STICKERS

class MyFormatter(logging.Formatter):
    def format(self, record):
        formatted = super().format(record)
        formatted = formatted.encode("utf-8").decode("unicode_escape")
        return formatted

formatter = MyFormatter('%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

from concurrent.futures import ThreadPoolExecutor
executor_asyncio = ThreadPoolExecutor(max_workers=32)

db = database.Database()

async def register_user_if_not_exists(message: types.Message):
    
    if not db.check_if_user_exists(message.from_user.id):
        db.add_new_user(
            user_id=message.from_user.id,
            chat_id=message.chat.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name
        )
        db.start_new_dialog(message.from_user.id)

    if db.get_user_attribute(message.from_user.id, "current_dialog_id") is None:
        db.start_new_dialog(message.from_user.id)

##################

class Allergence(StatesGroup):
    allergy = State()

class Feedback(StatesGroup):
    answer = State()

class Recomendation(StatesGroup):
    when = State()

class Question(StatesGroup):
    question = State()
    
class Recipe(StatesGroup):
    dish_name = State()

class Form(StatesGroup):
    gender = State()
    weight = State()
    weight_goal = State()
    height = State()
    timezone = State()

# token should be either stored in .env or as github token
if os.getenv("GITHUB_ACTIONS"):
    bot_token = os.getenv("TG_BOT_TOKEN")
else:
    load_dotenv()
    bot_token = os.getenv("TG_BOT_TOKEN")

bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(Command('start'), state='*')
async def start(message: types.Message, state: FSMContext):    
    await state.finish()
    await register_user_if_not_exists(message)
    db.set_user_attribute(message.from_user.id, "last_interaction", datetime.now())
    db.set_user_attribute(message.from_user.id, "first_feedback", True)
    db.start_new_dialog(message.from_user.id)

    await bot.send_sticker(message.chat.id, STICKERS['hi'])
    await bot.send_message(message.chat.id, f"Hello, {message.from_user.first_name}! 👋 \n\n" + MESSAGES['start'], 
                           reply_markup=kb.greet_kb, parse_mode='Markdown')

@dp.message_handler(Text(equals='Hello! 👋'))
async def gender_button_click(message: types.Message):
    await bot.send_message(message.chat.id, 
                        f"{message.from_user.first_name}, {MESSAGES['gender']}",
                        reply_markup=kb.gender_keyboard)
    await Form.gender.set()

@dp.message_handler(state=Form.gender)
async def gender_button_click(message: types.Message, state: FSMContext):
    await register_user_if_not_exists(message)
    db.set_user_attribute(message.from_user.id, "last_interaction", datetime.now())
    db.set_user_attribute(message.from_user.id, "gender", message.text)
    await bot.send_message(message.from_user.id, MESSAGES["weight"])
    await state.update_data(gender=message.text)
    await Form.next()

@dp.message_handler(state=Form.weight)
async def process_weight(message: types.Message, state: FSMContext):
    await register_user_if_not_exists(message)
    db.set_user_attribute(message.from_user.id, "last_interaction", datetime.now())
    try:
        int(message.text)
    except:
        await bot.send_message(message.from_user.id, "Seem you put the wrong number, try again.")
        await Form.weight.set()
    if int(message.text) < 40 or int(message.text) > 200:
        await bot.send_message(message.from_user.id, "Seem you put the wrong number, try again.")
        await Form.weight.set()
    else:
        db.set_user_attribute(message.from_user.id, "weight", message.text)
        await bot.send_message(message.from_user.id, MESSAGES["weight_goal"])
        await state.update_data(weight=message.text)
        await Form.next()
    
@dp.message_handler(state=Form.weight_goal)
async def process_weight_goal(message: types.Message, state: FSMContext):
    await register_user_if_not_exists(message)
    db.set_user_attribute(message.from_user.id, "last_interaction", datetime.now())
    db.set_user_attribute(message.from_user.id, "weight_goal", message.text)
    try:
        int(message.text)
    except:
        await bot.send_message(message.from_user.id, "Seem you put the wrong number, try again.")
        await Form.weight_goal.set()
    if int(message.text) < 40 or int(message.text) > 200:
        await bot.send_message(message.from_user.id, "Seem you put the wrong number, try again.")
        await Form.weight_goal.set()
    else:
        curr_weight = db.get_user_attribute(message.from_user.id, "weight")
        goal = ""
        goal_msg = ""
        if int(curr_weight) < int(message.text):
            goal = "gain weight"
            goal_msg = "Gain weight"
        elif int(curr_weight) == int(message.text):
            goal = "maintain weight"
            goal_msg = "Mantain weight"
        else:
            goal = "lose weight"
            goal_msg = "Lose weight"
        db.set_user_attribute(message.from_user.id, "goal", goal)
        await bot.send_message(message.from_user.id, goal_msg + " may seem like a daunting task, but we can do it. 😉!")
        await bot.send_message(message.from_user.id, MESSAGES["height"])
        await state.update_data(weight_goal=message.text)
        await Form.next()

@dp.message_handler(state=Form.height)
async def process_height(message: types.Message, state: FSMContext):
    await register_user_if_not_exists(message)
    db.set_user_attribute(message.from_user.id, "last_interaction", datetime.now())
    try:
        int(message.text)
    except:
        await bot.send_message(message.from_user.id, "Seem you put the wrong number, try again.")
        await Form.height.set()
    if int(message.text) < 40 or int(message.text) > 240:
        await bot.send_message(message.from_user.id, "Seem you put the wrong number, try again.")
        await Form.height.set()
    else:
        db.set_user_attribute(message.from_user.id, "height", message.text)
        await state.update_data(weight=message.text)
        await bot.send_sticker(message.chat.id, STICKERS['super'])
        await bot.send_message(message.from_user.id, MESSAGES["breakfast"], reply_markup=kb.breakfast_keyboard)
        await state.finish()

@dp.message_handler(lambda message: message.text in ['Cereal', 'Eggs', 'Joghurt'])
async def breakfast_handler(message: types.Message, state: FSMContext):
    await register_user_if_not_exists(message)
    db.set_user_attribute(message.from_user.id, "last_interaction", datetime.now())
    db.set_user_attribute(message.from_user.id, "breakfast", [message.text])
    await bot.send_message(message.from_user.id, MESSAGES["lunch"], reply_markup=kb.lunch_keyboard)

@dp.message_handler(lambda message: message.text in ['Soup', 'Pasta', 'Rice'])
async def lunch_handler(message: types.Message, state: FSMContext):
    await register_user_if_not_exists(message)
    db.set_user_attribute(message.from_user.id, "last_interaction", datetime.now())
    db.set_user_attribute(message.from_user.id, "lunch", [message.text])
    await bot.send_message(message.from_user.id, MESSAGES["dinner"], reply_markup=kb.dinner_keyboard)

@dp.message_handler(lambda msg: msg.text in ['Salad', 'Chicken', 'Fish'])
async def dinner_handler(message: types.Message, state: FSMContext):
    await register_user_if_not_exists(message)
    db.set_user_attribute(message.from_user.id, "last_interaction", datetime.now())
    db.set_user_attribute(message.from_user.id, "dinner", [message.text])
    await bot.send_message(message.from_user.id, MESSAGES['allergence'])
    await Allergence.allergy.set()

@dp.message_handler(state=Allergence.allergy)
async def process_weight(message: types.Message, state: FSMContext):
    await register_user_if_not_exists(message)
    db.set_user_attribute(message.from_user.id, "last_interaction", datetime.now())
    db.set_user_attribute(message.from_user.id, "allergic_to", message.text)
    await bot.send_message(message.from_user.id, MESSAGES["first_feedback"])
    await state.finish()
    await Feedback.answer.set()

@dp.callback_query_handler(lambda c: c.data == 'get_recipe')
async def trigger_feedback_cb(query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await register_user_if_not_exists(query.message)
    db.set_user_attribute(query.message.from_user.id, "last_interaction", datetime.now())
    await bot.send_message(query.message.chat.id, "Write the name of the dish or a list of the foods you want to make it with?", reply_markup=None)
    await Recipe.dish_name.set()

@dp.message_handler(commands='get_recipe')
async def trigger_feedback(message: types.Message, state: FSMContext):
    await state.finish()
    await register_user_if_not_exists(message)
    db.set_user_attribute(message.from_user.id, "last_interaction", datetime.now())
    await bot.send_message(message.chat.id, "Write the name of the dish or a list of the foods you want to make it with?", reply_markup=None)
    await Recipe.dish_name.set()

@dp.message_handler(state=Recipe.dish_name)
async def process_recipe(message: types.Message, state: FSMContext):
    await register_user_if_not_exists(message)
    db.set_user_attribute(message.from_user.id, "last_interaction", datetime.now())

    if len(message.text) == 0 or message.text == None:
        await bot.send_message(message.chat.id, "You didn't write anything, try again.")
        await Question.question.set()

    prompt_addition = f"I want to get a recipe for {message.text}. "
    messages = [{"role": "system", "content": PROMPTS['recipe'][0] + prompt_addition + PROMPTS['recipe'][1]},]

    sticker_message = await bot.send_sticker(message.chat.id, STICKERS['wait'])
    waiting_message = await bot.send_message(message.chat.id, "Thinking about the question....\nUsually it takes about 30 seconds, please wait.")
    
    sticker_message_id = sticker_message.message_id
    waiting_message_id = waiting_message.message_id

    loop = asyncio.get_event_loop()

    response = await loop.run_in_executor(executor_asyncio, openai_api.get_gpt_response, messages)
    await bot.delete_message(message.chat.id, sticker_message_id)
    await bot.edit_message_text(response, message.chat.id, waiting_message_id)

    await state.finish()

@dp.callback_query_handler(lambda c: c.data == "ask_question")
async def trigger_question(query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await register_user_if_not_exists(query.message)
    db.set_user_attribute(query.message.from_user.id, "last_interaction", datetime.now())
    await bot.send_message(query.message.chat.id, "Write down what question you want to ask a nutritionist 👩‍💻", reply_markup=None)
    await Question.question.set()

@dp.message_handler(commands='ask_question')
async def trigger_question(message: types.Message, state: FSMContext):
    await state.finish()
    await register_user_if_not_exists(message)
    db.set_user_attribute(message.from_user.id, "last_interaction", datetime.now())
    await bot.send_message(message.chat.id, "Write down what question you want to ask a nutritionist 👩‍💻", reply_markup=None)
    await Question.question.set()

@dp.message_handler(state=Question.question)
async def process_feedback(message: types.Message, state: FSMContext):
    await register_user_if_not_exists(message)
    db.set_user_attribute(message.from_user.id, "last_interaction", datetime.now())

    if len(message.text) == 0 or message.text == None:
        await bot.send_message(message.chat.id, "You didn't write the question(s), try again.")
        await Question.question.set()
    
    prompt_addition = f"My question is {message.text}. "
    messages = [{"role": "system", "content": PROMPTS['ask_me'][0] + prompt_addition + PROMPTS['ask_me'][1]},]

    sticker_message = await bot.send_sticker(message.chat.id, STICKERS['wait'])
    waiting_message = await bot.send_message(message.chat.id, "Thinking about the question....\nUsually it takes about 30 seconds, please wait.")
    
    sticker_message_id = sticker_message.message_id
    waiting_message_id = waiting_message.message_id

    loop = asyncio.get_event_loop()

    response = await loop.run_in_executor(executor_asyncio, openai_api.get_gpt_response, messages)
    await bot.delete_message(message.chat.id, sticker_message_id)
    await bot.edit_message_text(response, message.chat.id, waiting_message_id)

    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'get_feedback')
async def trigger_feedback_cb(query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.send_message(query.message.chat.id, "What food do you want feedback on? Write in commas what you ate 🙂", reply_markup=None)
    await Feedback.answer.set()

@dp.message_handler(commands='get_feedback')
async def trigger_feedback(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.chat.id, "What food do you want feedback on? Write in commas what you ate 🙂", reply_markup=None)
    await Feedback.answer.set()

@dp.message_handler(state=Feedback.answer)
async def process_feedback(message: types.Message, state: FSMContext):
    await register_user_if_not_exists(message)
    db.set_user_attribute(message.from_user.id, "last_interaction", datetime.now())

    if len(message.text) == 0 or message.text == None:
        await bot.send_message(message.chat.id, "You didn't tell me what you ate, try again.")
        return
    
    first_name = db.get_user_attribute(message.from_user.id, "first_name")
    goal = db.get_user_attribute(message.from_user.id, "goal")

    allergic_response = db.get_user_attribute(message.from_user.id, 'allergic_to')# + I'm allergic to {allergic_to}
    allergic_template = ['нет', 'нету']
    if_not_allergic = if_simmilar(allergic_response, allergic_template)
    allergic_status = f"In regards to my allergy, I am allergic to {allergic_response}." if not if_not_allergic else "I am not allergic to anything."
    
    gender = f"My gender is {db.get_user_attribute(message.from_user.id, 'gender')}. " 
    prompt_addition = f"I ate {message.text}. My goal is to {goal}. " + allergic_status + gender + f"In the reply I want you to greet using my name: {first_name}"
    messages = [{"role": "system", "content": PROMPTS['feedback'][0] + prompt_addition + PROMPTS['feedback'][1]},]

    sticker_message = await bot.send_sticker(message.chat.id, STICKERS['wait'])
    sticker_message_id = sticker_message.message_id

    waiting_message = await bot.send_message(message.chat.id, "I'm writing feedback...\nUsually it takes about 30 seconds, please wait.")
    waiting_message_id = waiting_message.message_id

    loop = asyncio.get_event_loop()

    response = await loop.run_in_executor(executor_asyncio, openai_api.get_gpt_response, messages)
    await bot.delete_message(message.chat.id, sticker_message_id)
    await bot.edit_message_text(response, message.chat.id, waiting_message_id)

    first_feedback = db.get_user_attribute(message.from_user.id, "first_feedback")
    print(f"If this is the first feedback: {first_feedback}")
    if first_feedback:
        db.set_user_attribute(message.from_user.id, "first_feedback", False) 
        await state.finish()
        await bot.send_sticker(message.chat.id, STICKERS['hooray'])
        await bot.send_message(message.chat.id, MESSAGES['finish_onboarding'], reply_markup=kb.feedback_recommendation_question_kb)

        # TODO: set timezone
    else:
        await state.update_data(feedback=message.text)
        await state.finish()

async def send_daily_message(user_id):
    await bot.send_message(user_id, "Good morning! Here's your daily message...")

@dp.callback_query_handler(lambda c: c.data == "get_recommendation")
async def get_recommendation_cb(query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await register_user_if_not_exists(query.message)
    db.set_user_attribute(query.message.from_user.id, "last_interaction", datetime.now())
    await bot.send_message(query.message.chat.id, "What meal do you want to get recommendations for?👩‍🍳", reply_markup=kb.recomm_keyboard)
    await Recomendation.when.set()

@dp.message_handler(commands=['get_recommendation'])
async def get_recommendation(message: types.Message, state: FSMContext):
    await state.finish()
    await register_user_if_not_exists(message)
    db.set_user_attribute(message.from_user.id, "last_interaction", datetime.now())
    await bot.send_message(message.from_user.id, "What meal do you want to get recommendations for?👩‍🍳", reply_markup=kb.recomm_keyboard)
    await Recomendation.when.set()

@dp.message_handler(state=Recomendation.when)
async def process_recommend(message: types.Message, state: FSMContext):
    await register_user_if_not_exists(message)
    db.set_user_attribute(message.from_user.id, "last_interaction", datetime.now())
    
    if message.text == 'Breakfast':
        breakfast_lunch_dinner = f"I want to cook something for breakfast."
    elif message.text == 'Lunch':
        breakfast_lunch_dinner = f"I want to cook something for lunch."
    elif message.text == 'Dinner':
        breakfast_lunch_dinner = f"I want to cook something for a light dinner."
    else:   
        breakfast_lunch_dinner = f"I want a recommendation for a snack."
    goal = f"My goal is to {db.get_user_attribute(message.from_user.id, 'goal')}." 
    gender = f"My gender is {db.get_user_attribute(message.from_user.id, 'gender')}. " 
    weight = f"My weight is {db.get_user_attribute(message.from_user.id, 'weight')}. " 
    weight_goal = f"My weight goal is {db.get_user_attribute(message.from_user.id, 'weight_goal')}. "
    height = f"My height is {db.get_user_attribute(message.from_user.id, 'height')}. " 
    allergic_to = f"Please consider that I'm allergic to {db.get_user_attribute(message.from_user.id, 'allergic_to')}."
    breakfast = f"For breakfast, I prefer {db.get_user_attribute(message.from_user.id, 'breakfast')}, "
    lunch = f"for lunch, I like {db.get_user_attribute(message.from_user.id, 'lunch')}, "
    dinner = f"and for dinner, I prefer {db.get_user_attribute(message.from_user.id, 'dinner')}. "

    prompt_addition = breakfast_lunch_dinner + goal + gender + weight + weight_goal + height + breakfast + lunch + dinner + allergic_to 
    messages = [{"role": "system", "content": PROMPTS['recommend'][0] + prompt_addition + PROMPTS['recommend'][1]},]

    sticker_message = await bot.send_sticker(message.chat.id, STICKERS['wait'])
    sticker_message_id = sticker_message.message_id

    waiting_message = await bot.send_message(message.chat.id, "Thinking about the question....\nUsually it takes about 30 seconds, please wait.", reply_markup=None)
    waiting_message_id = waiting_message.message_id

    loop = asyncio.get_event_loop()

    response = await loop.run_in_executor(executor_asyncio, openai_api.get_gpt_response, messages)

    await bot.delete_message(message.chat.id, sticker_message_id)
    await bot.edit_message_text(response, message.chat.id, waiting_message_id, reply_markup=kb.recipe_recommendation_kb)
    await state.finish()

@dp.message_handler(commands=['help'])
async def list_preferences(message: types.Message, state: FSMContext):
    await state.finish()
    register_user_if_not_exists(message)
    db.set_user_attribute(message.from_user.id, "last_interaction", datetime.now())
    await bot.send_message(message.chat.id, f"{MESSAGES['help']}", reply_markup=None)

async def on_shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

if __name__ == '__main__':
    
    executor.start_polling(dp, 
                           on_shutdown=on_shutdown)