start_message = "Привет! 👋 \n\nНа связи твой личный бот-нутрициолог 🤖\n\nМоя миссия - помочь тебе правильно питаться, чтобы ты смог достигнуть своих целей, будь то похудение, поддержание веса или набор мышечной массы. \n\nВот что я могу для тебя сделать: \n 1. Оценивать твои приемы пищи и советовать, как можно их улучшить.\n\n 2. Подсказывать идеи блюд на завтрак, обед, ужин или перекус, исходя из твоих предпочтений.\n\n 3. Отвечать на все твои вопросы о питании.\n\n\nНо, для начала мне потребуется узнать о тебе немного больше, чтобы мои советы были максимально адаптированы под тебя. Подготовься к небольшому вопроснику, который я сейчас тебе отправлю. Жду твоих ответов!"

gender_message = "Пожалуйста, укажи свой пол."
weight_message = "Хорошо. А какой твой текущий вес? Напиши цифру в кг."
weight_goal_message = "Отлично. Какой твой желаемый вес? Напиши цифру в кг."
height_message = "Какой у тебя сейчас рост? Укажи цифру в см."

breakfast_message = "Теперь давай узнаем твои предпочтения.\n\nВыбери наилучший вариант завтрака для тебя из опций ниже."
lunch_message = "Что из этого ты выберешь съесть на обед? Отметь один наилучший вариант."
dinner_message = "Что из этого ты предпочтёшь съесть на ужин? Выбери один наилучший вариант."

allergence_message = "Очень важный момент. Есть ли у тебя аллергия на какую-то еду? Перечисли продукты через запятую. Если нет аллергий, то напиши нет.\nНапример: орехи, рыба"
first_feedback = "Расскажи, что ты съел(а) вчера. Перечисли все продукты, которые ты ел(а) в течение дня вчера через запятую. И я пришлю тебе фидбек с рекомендациями."

finish_onboarding_message = "Поздравляю! Ты прошел онбординг! \nЧтобы снова получить от меня фидбек на еду и рекомендации, как можно её улучшить, отправь команду /get_feedback и напиши, что ты съел.\n\n\
Если тебе нужна помощь с выбором, что съесть на завтрак/обед/ужин, набери команду /get_recommendation. \n\n\
Для изменения ответов на вопросы из онбординга, нажми кнопку /start и пройди онбординг заново. \n\n\
Если ты забудешь, как пользоваться ботом, нажми на /help."

timezone_message = "Последний вопрос, укажи свой часовой пояс, чтобы я мог вовремя прислать тебе рекомендации на день"

help_message="""Команды:
/get_recommendation - Узнать, что съесть / Получить рекомендацию, что съесть
/get_feedback - Получить фидбек на еду
/ask_me - Задать вопрос нутрициологу
/get_receipt - Получить рецепт по названию
/set_timezon - удалить, установить часовой пояс, чтобы я присылал тебе рекомендации каждое утро
/help - Общий списк команд
/start - Пройти онбординг заново
"""

MESSAGES = {
    'start': start_message,
    'gender': gender_message,
    'weight': weight_message,
    'weight_goal': weight_goal_message,
    'height': height_message,
    'breakfast': breakfast_message,
    'lunch': lunch_message,
    'dinner': dinner_message,
    'allergence': allergence_message,
    'first_feedback': first_feedback,
    'timezone': timezone_message,
    'finish_onboarding': finish_onboarding_message,
    'help': help_message,
}

