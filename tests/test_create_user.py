import allure
from data import TestData
from helpers import UserHelper
import pytest
import requests


@allure.step("Создать пользователя")
def register_user(payload):
  return requests.post(TestData.CREATE_USER_URL, json=payload)


@allure.suite("Тестирование создания пользователя")
class TestCreateUser:

  @allure.title("Успешное создание уникального пользователя")
  def test_create_unique_user_success(self, delete_user_after_test):
    payload = UserHelper.generate_user_payload()
    response = register_user(payload)

    delete_user_after_test["token"] = response.json().get("accessToken")

    assert response.status_code == 200
    assert response.json().get("success") is True

  @allure.title("Ошибка при создании уже существующего пользователя")
  def test_create_existing_user_error(self, create_user):
    _, payload = create_user
    response = register_user(payload)

    assert response.status_code == 403
    assert response.json().get("success") is False
    assert response.json().get("message") == "User already exists"

  @allure.title("Ошибка создания пользователя при отсутствии обязательного поля")
  @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
  def test_create_user_missing_field_error(self, missing_field):
    payload = UserHelper.generate_user_payload()
    del payload[missing_field]

    response = register_user(payload)

    assert response.status_code == 403
    assert response.json().get("success") is False
    assert (
        response.json().get("message")
        == "Email, password and name are required fields"
    )
