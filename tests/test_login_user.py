import allure
from data import TestData
import requests


@allure.step("Авторизовать пользователя")
def login_user(payload):
  return requests.post(TestData.LOGIN_USER_URL, json=payload)


@allure.suite("Тестирование авторизации пользователя")
class TestLoginUser:

  @allure.title("Успешный логин существующим пользователем")
  def test_login_user_success(self, create_user):
    _, payload = create_user
    login_payload = {"email": payload["email"], "password": payload["password"]}

    response = login_user(login_payload)

    assert response.status_code == 200
    assert response.json().get("success") is True
    assert "accessToken" in response.json()

  @allure.title("Ошибка авторизации с неверным логином/паролем")
  def test_login_user_wrong_credentials_error(self):
    login_payload = {
        "email": TestData.WRONG_EMAIL,
        "password": TestData.WRONG_PASSWORD,
    }

    response = login_user(login_payload)

    assert response.status_code == 401
    assert response.json().get("success") is False
