import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone

from datetime import datetime
import database

import openai_api

from messages import MESSAGES
from prompts import PROMPTS
from stickers import STICKERS, GIFS
import keyboards as kb
from keyboards import timezone_options

from config import TG_BOT_TOKEN
from prompts import assistant_initialization_prompt

import logging
# logging.basicConfig(format='%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
#                     level=logging.DEBUG, encoding="cp1251")
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
##################

scheduler = AsyncIOScheduler()

from concurrent.futures import ThreadPoolExecutor
executor_asyncio = ThreadPoolExecutor(max_workers=32)

# database related 
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
    
class Receipt(StatesGroup):
    dish_name = State()

class Form(StatesGroup):
    gender = State()
    weight = State()
    weight_goal = State()
    height = State()
    timezone = State()

bot = Bot(token=TG_BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(Command('start'), state='*')
async def start(message: types.Message, state: FSMContext):    
    await state.finish()
    await register_user_if_not_exists(message)
    db.set_user_attribute(message.from_user.id, "last_interaction", datetime.now())
    db.set_user_attribute(message.from_user.id, "first_feedback", True)
    db.start_new_dialog(message.from_user.id)

    await bot.send_sticker(message.chat.id, STICKERS['hi'])
    #with open("/Users/aleksandr.glushko/Coding/nutrition_bot/src/images/nutrition_coach_welcome.jpg", "rb") as photo:
    #    await bot.send_photo(message.chat.id, photo=photo)
    await bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! 👋 \n\n" + MESSAGES['start'], 
                           reply_markup=kb.greet_kb, parse_mode='Markdown')
    

######### onboarding

@dp.message_handler(Text(equals='Привет, Коуч! 👋'))
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
        await bot.send_message(message.from_user.id, "Кажется ты указал неправильный вес, попробуй еще раз.")
        await Form.weight.set()
    if int(message.text) < 40 or int(message.text) > 200:
        await bot.send_message(message.from_user.id, "Кажется ты указал неправильный вес, попробуй еще раз.")
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
        await bot.send_message(message.from_user.id, "Кажется ты указал неправильный вес, попробуй еще раз.")
        await Form.weight_goal.set()
    if int(message.text) < 40 or int(message.text) > 200:
        await bot.send_message(message.from_user.id, "Кажется ты указал неправильный вес, попробуй еще раз.")
        await Form.weight_goal.set()
    else:
        curr_weight = db.get_user_attribute(message.from_user.id, "weight")
        goal = ""
        if int(curr_weight) < int(message.text):
            goal = "gain weight"
        elif int(curr_weight) == int(message.text):
            goal = "maintain weight"
        else:
            goal = "lose weight"
        db.set_user_attribute(message.from_user.id, "goal", goal)
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
        await bot.send_message(message.from_user.id, "Кажется ты указал неправильный рост, попробуй еще раз.")
        await Form.height.set()
    if int(message.text) < 40 or int(message.text) > 240:
        await bot.send_message(message.from_user.id, "Кажется ты указал неправильный рост, попробуй еще раз.")
        await Form.height.set()
    else:
        db.set_user_attribute(message.from_user.id, "height", message.text)
        await state.update_data(weight=message.text)
        await bot.send_sticker(message.chat.id, STICKERS['super'])
        await bot.send_message(message.from_user.id, MESSAGES["breakfast"], reply_markup=kb.breakfast_keyboard)
        await state.finish()

@dp.message_handler(lambda message: message.text in ['Овсянка', 'Яйца', 'Йогурт'])
async def breakfast_handler(message: types.Message, state: FSMContext):
    await register_user_if_not_exists(message)
    db.set_user_attribute(message.from_user.id, "last_interaction", datetime.now())
    db.set_user_attribute(message.from_user.id, "breakfast", [message.text])
    await bot.send_message(message.from_user.id, MESSAGES["lunch"], reply_markup=kb.lunch_keyboard)

@dp.message_handler(lambda message: message.text in ['Суп', 'Паста', 'Рис'])
async def lunch_handler(message: types.Message, state: FSMContext):
    await register_user_if_not_exists(message)
    db.set_user_attribute(message.from_user.id, "last_interaction", datetime.now())
    db.set_user_attribute(message.from_user.id, "lunch", [message.text])
    await bot.send_message(message.from_user.id, MESSAGES["dinner"], reply_markup=kb.dinner_keyboard)

@dp.message_handler(lambda msg: msg.text in ['Салат', 'Курица', 'Лосось', 'Креветки'])
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

@dp.message_handler(commands='get_recipe')
async def trigger_feedback(message: types.Message, state: FSMContext):
    await register_user_if_not_exists(message)
    db.set_user_attribute(message.from_user.id, "last_interaction", datetime.now())
    await bot.send_message(message.chat.id, "Какое блюдо тебя интересует?")
    await Receipt.dish_name.set()

@dp.message_handler(state=Receipt.dish_name)
async def process_receipt(message: types.Message, state: FSMContext):
    await register_user_if_not_exists(message)
    db.set_user_attribute(message.from_user.id, "last_interaction", datetime.now())

    if len(message.text) == 0 or message.text == None:
        await bot.send_message(message.chat.id, "Ты ничего не написал(а), попробуй еще раз.")
        await Question.question.set()

    prompt_addition = f"I want to get a receipt for {message.text}. "
    messages = [{"role": "system", "content": PROMPTS['receipt'][0] + prompt_addition + PROMPTS['receipt'][1]},]

    sticker_message = await bot.send_sticker(message.chat.id, STICKERS['wait'])
    waiting_message = await bot.send_message(message.chat.id, "Думаю над вопросом...\nОбычно это занимает около 30 секунд, пожалуйста, ожидайте.")
    
    sticker_message_id = sticker_message.message_id
    waiting_message_id = waiting_message.message_id

    loop = asyncio.get_event_loop()

    response = await loop.run_in_executor(executor_asyncio, openai_api.get_gpt_response, messages)
    await bot.delete_message(message.chat.id, sticker_message_id)
    await bot.edit_message_text(response, message.chat.id, waiting_message_id)

    await state.finish()

@dp.message_handler(commands='ask_question')
async def trigger_feedback(message: types.Message, state: FSMContext):
    await register_user_if_not_exists(message)
    db.set_user_attribute(message.from_user.id, "last_interaction", datetime.now())
    await bot.send_message(message.chat.id, "Напиши, какой вопрос ты хочешь задать нутрициологу? 👩‍💻")
    await Question.question.set()

@dp.message_handler(state=Question.question)
async def process_feedback(message: types.Message, state: FSMContext):
    await register_user_if_not_exists(message)
    db.set_user_attribute(message.from_user.id, "last_interaction", datetime.now())

    if len(message.text) == 0 or message.text == None:
        await bot.send_message(message.chat.id, "Ты не написал(а) вопрос, попробуй еще раз.")
        await Question.question.set()
    
    prompt_addition = f"My question is {message.text}. "
    messages = [{"role": "system", "content": PROMPTS['ask_me'][0] + prompt_addition + PROMPTS['ask_me'][1]},]

    sticker_message = await bot.send_sticker(message.chat.id, STICKERS['wait'])
    waiting_message = await bot.send_message(message.chat.id, "Думаю над вопросом...\nОбычно это занимает около 30 секунд, пожалуйста, ожидайте.")
    
    sticker_message_id = sticker_message.message_id
    waiting_message_id = waiting_message.message_id

    loop = asyncio.get_event_loop()

    response = await loop.run_in_executor(executor_asyncio, openai_api.get_gpt_response, messages)
    await bot.delete_message(message.chat.id, sticker_message_id)
    await bot.edit_message_text(response, message.chat.id, waiting_message_id)

    await state.finish()

@dp.message_handler(commands='get_feedback')
async def trigger_feedback(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, "На какую еду ты хочешь получить фидбек? Напиши через запятую, что ты съел 🙂?")
    await Feedback.answer.set()

@dp.message_handler(state=Feedback.answer)
async def process_feedback(message: types.Message, state: FSMContext):
    await register_user_if_not_exists(message)
    db.set_user_attribute(message.from_user.id, "last_interaction", datetime.now())

    if len(message.text) == 0 or message.text == None:
        await bot.send_message(message.chat.id, "Ты не рассказал(а), что кушал(а), попробуй еще раз.")
        return
    
    goal = db.get_user_attribute(message.from_user.id, "goal")
    allergic_to = db.get_user_attribute(message.from_user.id, 'allergic_to')
    gender = f"My gender is {db.get_user_attribute(message.from_user.id, 'gender')}. " 
    prompt_addition = f"I ate {message.text}. My goal is to {goal}. I'm allergic to {allergic_to} " + gender
    messages = [{"role": "system", "content": PROMPTS['feedback'][0] + prompt_addition + PROMPTS['feedback'][1]},]

    sticker_message = await bot.send_sticker(message.chat.id, STICKERS['wait'])
    sticker_message_id = sticker_message.message_id

    waiting_message = await bot.send_message(message.chat.id, "Составляю фидбек...\nОбычно это занимает около 30 секунд, пожалуйста, ожидайте.")
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
        await bot.send_message(message.chat.id, MESSAGES['finish_onboarding'])

        # for timezone
        # await bot.send_message(message.from_user.id, MESSAGES["timezone"], reply_markup=kb.timezone_kb)
        # await Form.timezone.set()
    else:
        await state.update_data(feedback=message.text)
        await state.finish()

# @dp.message_handler(commands=['set_timezone'])
# async def get_recommendation(message: types.Message):
#     await bot.send_message(message.from_user.id, MESSAGES["timezone"], reply_markup=kb.timezone_kb)
#     await Form.timezone.set()

# @dp.message_handler(state=Form.timezone)
# async def process_weight(message: types.Message, state: FSMContext):
#     await register_user_if_not_exists(message)
#     db.set_user_attribute(message.from_user.id, "last_interaction", datetime.now())
#     if message.text in timezone_options:
#         db.set_user_attribute(message.from_user.id, "timezone", message.text)

#         await bot.send_sticker(message.chat.id, STICKERS['hooray'])
#         await bot.send_message(message.chat.id, MESSAGES['finish_onboarding'])
#         # ask user in case he want a reminder and then schedule
#         schedule_job(message.from_user.id, message.text)
#         await state.finish()
#     else:
#         await bot.send_message(message.from_user.id, "Invalid option. Please select a valid timezone.")

async def send_daily_message(user_id):
    await bot.send_message(user_id, "Good morning! Here's your daily message...")

@dp.message_handler(commands=['get_recommendation'])
async def get_recommendation(message: types.Message):
    await register_user_if_not_exists(message)
    db.set_user_attribute(message.from_user.id, "last_interaction", datetime.now())
    await bot.send_message(message.from_user.id, "На какой приём пищи ты хочешь получить рекомендации?👩‍🍳", reply_markup=kb.recomm_keyboard)
    await Recomendation.when.set()

@dp.message_handler(state=Recomendation.when)
async def process_recommend(message: types.Message, state: FSMContext):
    await register_user_if_not_exists(message)
    db.set_user_attribute(message.from_user.id, "last_interaction", datetime.now())
    
    if message.text == 'Завтрак':
        breakfast_lunch_dinner = f"I want to cook something for breakfast."
    elif message.text == 'Обед':
        breakfast_lunch_dinner = f"I want to cook something for lunch."
    elif message.text == 'Ужин':
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

    waiting_message = await bot.send_message(message.chat.id, "Составляю рекомендацию...\nОбычно это занимает около 30 секунд, пожалуйста, ожидайте.", reply_markup=None)
    waiting_message_id = waiting_message.message_id

    loop = asyncio.get_event_loop()

    response = await loop.run_in_executor(executor_asyncio, openai_api.get_gpt_response, messages)

    await bot.delete_message(message.chat.id, sticker_message_id)
    await bot.edit_message_text(response, message.chat.id, waiting_message_id)
    await state.finish()

@dp.message_handler(commands=['help'])
async def list_preferences(message: types.Message):
    register_user_if_not_exists(message)
    db.set_user_attribute(message.from_user.id, "last_interaction", datetime.now())
    await bot.send_message(message.chat.id, f"{MESSAGES['help']}")

# @dp.message_handler()
# async def echo_message(msg: types.Message):
#     await bot.send_message(msg.from_user.id, msg.text)

async def send_daily_message(user_id):
    await bot.send_message(user_id, "Good morning! Here's your daily message...")

def schedule_job(user_id, user_timezone="Europe/Paris"):
    scheduler.add_job(send_daily_message, 'cron', id=str(user_id), hour=8, args=[user_id], timezone=timezone(user_timezone))

def update_user_timezone(user_id, new_timezone):
    try:
        scheduler.remove_job(str(user_id))
    except Exception as err:
        print("Exception during deleting the scheduler job: ", err)

    schedule_job(user_id, new_timezone)

async def on_startup(dp):
    # import filters
    # import middlewares
    # filters.setup(dp)
    # middlewares.setup(dp)

    scheduler.start()

async def on_shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    scheduler.remove_all_jobs()

if __name__ == '__main__':
    
    executor.start_polling(dp, 
                           on_startup=on_startup, 
                           on_shutdown=on_shutdown)