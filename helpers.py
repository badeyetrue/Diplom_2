import random
import string
import requests
from data import TestData

class UserHelper:
    @staticmethod
    def generate_random_string(length=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    @staticmethod
    def generate_user_payload():
        return {
            "email": f"altai_{UserHelper.generate_random_string()}@yandex.ru",
            "password": UserHelper.generate_random_string(12),
            "name": f"Altai_{UserHelper.generate_random_string(5)}"
        }

    @staticmethod
    def register_new_user_and_return_data():
        payload = UserHelper.generate_user_payload()
        response = requests.post(TestData.CREATE_USER_URL, json=payload)
        return response, payload
