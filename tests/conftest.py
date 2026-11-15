import pytest
import requests
from helpers import UserHelper
from data import TestData

@pytest.fixture(scope="function")
def create_user():
    response, payload = UserHelper.register_new_user_and_return_data()
    yield response, payload
    
    if response.status_code == 200:
        token = response.json().get("accessToken")
        if token:
            headers = {"Authorization": token}
            requests.delete(TestData.USER_URL, headers=headers)
