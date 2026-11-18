import allure
from data import TestData
from helpers import UserHelper
import pytest
import requests


@allure.step("Удалить пользователя")
def delete_user(headers):
  return requests.delete(TestData.USER_URL, headers=headers)


@pytest.fixture(scope="function")
def create_user():
  response, payload = UserHelper.register_new_user_and_return_data()
  yield response, payload

  if response.status_code == 200:
    token = response.json().get("accessToken")
    if token:
      headers = {"Authorization": token}
      delete_user(headers)


@pytest.fixture(scope="function")
def delete_user_after_test():
  user_data = {}
  yield user_data

  token = user_data.get("token")
  if token:
    headers = {"Authorization": token}
    delete_user(headers)
