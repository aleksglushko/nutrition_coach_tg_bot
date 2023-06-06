start_message = "На связи *бот-нутрициолог* 🤖\n\nРад, что ты хочешь улучшить свое питание, чтобы похудеть или набрать мышцы 💪\n\nТы уже знаешь немного про меня.\
Будет здорово, если ты тоже расскажешь чуть-чуть про себя. Так я смогу сделать рекомендации персонализированными 👩‍🔬\n\nНажми на кнопку 'Привет!' и мы начнем онбординг 🙂"

gender_message = "укажи свой пол, пожалуйста."
weight_message = "Хорошо. А какой твой текущий вес? Напиши цифру в кг."
weight_goal_message = "Отлично. Какой твой желаемый вес? Напиши цифру в кг."
height_message = "Какой у тебя сейчас рост? Укажи цифру в см."

breakfast_message = "Теперь давай узнаем твои предпочтения.\n\nВыбери наилучший вариант завтрака для тебя из опций ниже."
lunch_message = "Что из этого ты выберешь съесть на обед? Отметь один наилучший вариант."
dinner_message = "Что из этого ты предпочтёшь съесть на ужин? Выбери один наилучший вариант."
allergence_message = "Очень важный момент. Есть ли у тебя аллергия на какую-то еду? Перечисли продукты через запятую. Например: орехи, рыба. Если нет аллергий, то напиши 'нет'."
first_feedback = "Расскажи, что ты съел(а) вчера. Перечисли все продукты, которые ты ел(а) в течение дня вчера через запятую. И я пришлю тебе фидбек с рекомендациями."

finish_onboarding_message = "Поздравляю! Ты прошел онбординг! \nНадеюсь мой фидбек был полезным для тебя👩‍🔬\n\nЕсли ты захочешь снова получить от меня фидбек на твою еду и рекомендации, ты можешь отправить команду /get_feedback и написать, что ты съел.\n\n\
Также, ты можешь использовать другие команды:\n/get_recommendation - получить рекомендацию, что съесть на завтрак/обед/ужин/перекус.\n\
/ask_question - задать нутрициологу любой вопрос про питание.\n/get_recipe - получить рецепт.\n/start - пройти онбординг заново, чтобы изменить свои ответы.\n\
/help - узнать про возможности бота."

timezone_message = "Последний вопрос, укажи свой часовой пояс, чтобы я мог вовремя прислать тебе рекомендации на день"

help_message="""Варианты общения со мной 🤖:
/get_recommendation - получить рекомендацию, что съесть
/get_feedback - получить фидбек на еду
/ask_question - задать вопрос про питание
/get_recipe - получить рецепт 
/help - узнать про возможности бота
/start - пройти онбординг заново, чтобы изменить свои ответы
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

