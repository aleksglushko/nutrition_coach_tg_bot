from pymongo import MongoClient
from typing import Optional, Any

import pymongo
import uuid
from datetime import datetime
import config

class Database:
    def __init__(self):
        self.client = pymongo.MongoClient(config.MONGODB_URI)
        self.db = self.client['nutrition_bot']
        self.dialog_collection = self.db['dialog']
       # self.food = self.db['food']
        self.user_collection = self.db['user']

    def check_if_user_exists(self, user_id: int, raise_exception: bool = False):
        if self.user_collection.count_documents({"_id": user_id}) > 0:
            return True
        else:
            if raise_exception:
                raise ValueError(f"User {user_id} does not exist")
            else:
                return False
            
    def add_new_user(self, user_id: int, chat_id: int, username: str = "", 
                     first_name: str = "", last_name: str = "", goal: str = "weight_loss",
                     gender: str = "", weight: str = "", weight_goal: str="", height: str = "",
                     breakfast: list=[], lunch: list=[], dinner: list=[], allergic_to: list=[],
                     first_feedback: bool=True, timezone: str=""):
        user_dict = {
            "_id": user_id,
            "chat_id": chat_id,

            "username": username,
            "first_name": first_name,
            "last_name": last_name,

            "goal": goal,
            "gender": gender,
            "weight": weight,
            "weight_goal": weight_goal,
            "height": height,

            "breakfast": breakfast,
            "lunch": lunch,
            "dinner": dinner,
            "allergic_to": allergic_to,

            "first_feedback": first_feedback,

            "timezone": timezone,
            "last_interaction": datetime.now(),
            "first_seen": datetime.now(),

            "current_dialog_id": None,
        }
        # food_dict = {
        #     "_id": user_id,
        #     "chat_id": chat_id,
            
        #     "last_interaction": datetime.now(),
        # }
        if not self.check_if_user_exists(user_id):
            self.user_collection.insert_one(user_dict)
            # self.food.insert_one(food_dict)

    def start_new_dialog(self, user_id: int):
        self.check_if_user_exists(user_id, raise_exception=True)

        dialog_id = str(uuid.uuid4())
        dialog_dict = {
            "_id": dialog_id,
            "user_id": user_id,
            "start_time": datetime.now(),
            "messages": []
        }

        # add new dialog
        self.dialog_collection.insert_one(dialog_dict)

        # update user's current dialog
        self.user_collection.update_one(
            {"_id": user_id},
            {"$set": {"current_dialog_id": dialog_id}}
        )

        return dialog_id
    
    def get_user_attribute(self, user_id: int, key: str):
        self.check_if_user_exists(user_id, raise_exception=True)
        user_dict = self.user_collection.find_one({"_id": user_id})

        if key not in user_dict:
            return None

        return user_dict[key]
    
    def set_user_attribute(self, user_id: int, key: str, value: Any):
        self.check_if_user_exists(user_id, raise_exception=True)
        self.user_collection.update_one({"_id": user_id, }, {"$set": {key: value}})

    # def get_food_attribute(self, user_id: int, key: str):
    #     self.check_if_user_exists(user_id, raise_exception=True)
    #     user_dict = self.food_preferences.find_one({"_id": user_id})

    #     if key not in user_dict:
    #         return None

    #     return user_dict[key]
    
    # def set_food_attribute(self, user_id: int, key: str, value: Any):
    #     self.check_if_user_exists(user_id, raise_exception=True)
    #     self.food.update_one({"_id": user_id}, {"$set": {key: value}})

    def get_dialog_messages(self, user_id: int, dialog_id: Optional[str] = None):
        self.check_if_user_exists(user_id, raise_exception=True)

        if dialog_id is None:
            dialog_id = self.get_user_attribute(user_id, "current_dialog_id")

        dialog_dict = self.dialog_collection.find_one({"_id": dialog_id, "user_id": user_id})
        return dialog_dict["messages"]
    
    def set_dialog_messages(self, user_id: int, dialog_messages: list, dialog_id: Optional[str] = None):
        self.check_if_user_exists(user_id, raise_exception=True)

        if dialog_id is None:
            dialog_id = self.get_user_attribute(user_id, "current_dialog_id")

        self.dialog_collection.update_one(
            {"_id": dialog_id, "user_id": user_id},
            {"$set": {"messages": dialog_messages}}
        )
