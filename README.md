
<img width="1084" alt="Screenshot 2023-08-23 at 17 12 28" src="https://github.com/aleksglushko/nutrition_coach_tg_bot/assets/33725021/5f091976-2364-473a-bd10-efae7e914952">

# Nutrify is a telegram bot connected to OpenAI API GPT model. 
An example of a telegram bot with a onboarding-story for a user with MongoDB interaction. Easy to deploy on any container. Current version is English, managable in `src/messages.py`. 

Nutrify is an MVP to test the audience needs with regards of nutrition goals. As a bot, one can find the process of interaction easier than using a full-scale App with a vast amount of UI features. Telegram platform offers easy to use built in functions for user interactions.

Nutrify - a simple way to log food, get feedback about a meal, discover & share healthy food ideas, track your nutrition progress, and be a part of a huge community of people who have the same goal to lose weight. 

One needs to create `.env` file with the following tokens: 
```code
TG_BOT_TOKEN = ''
OPENAI_TOKEN = ''
MONGODB_URI = ''
```
run
`python src/bot.py`

TODO:
- change onboarding buttons to callback buttons
- unify message sources
- unify handlers
- tracking framework for every new user
- db backup
- automatic db rollout
- add CD part to digital ocean as a container
- full coverage tests