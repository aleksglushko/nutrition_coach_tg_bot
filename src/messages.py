start_message = "Here's the *nutritionist bot*. 🤖\n\nGlad you want to improve your diet to lose weight or gain muscle 💪\n\nYou already know a little bit about me.\
It would be great if you could tell me a little bit about yourself too. That way I can personalise the recommendations 👩‍🔬\n\nClick on the 'Hello!' button and we'll start onboarding 🙂"

gender_message = "State your gender, please."
weight_message = "Good. What's your current weight? Write the number in kilograms."
weight_goal_message = "That's great. What is your desired weight? Write the number in kg."
height_message = "What is your current height? Give a figure in cm."

breakfast_message = "Now let's find out what your preferences are.\n\nPick the best breakfast option for you from the options below."
lunch_message = "Which of these would you choose to eat for lunch? Tick one of the best options."
dinner_message = "Which of these would you rather eat for dinner? Choose one best option."
allergence_message = "Very important point. Are you allergic to any foods? List the foods in commas. For example: nuts, fish. If you are not allergic, then write 'no'."
first_feedback = "Tell what you ate yesterday. List all the foods you ate during the day yesterday, separated by commas. And I'll send you feedback with recommendations."

finish_onboarding_message = "Congratulations! You made it through onboarding! \nI hope my feedback was helpful to you👩‍🔬\n\nIf you want to get feedback on your food and recommendations from me again, you can send the /get_feedback command and post what you ate.\n\n\
Also, you can use other commands:\n/get_recommendation - get a recommendation on what to eat for breakfast/lunch/dinner/snack.\n\
/ask_question - ask the nutritionist any nutrition question.\n/get_recipe - get a cooking recipe.\n/start - re-boarding to change your answers.\n\
/help - learn about the bot's capabilities."

timezone_message = "One last question, state your time zone so I can send you your recommendations for the day on time."

help_message="""Options for communicating with me 🤖:
/get_recommendation - get a recommendation on what to eat
/get_feedback - get feedback on the food
/ask_question - ask a nutritional question
/get_recipe - get a cooking recipe
/help - learn about the bot's capabilities
/start - re-boarding to change your answers.
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

