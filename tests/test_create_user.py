import pytest
import requests
import allure
from helpers import UserHelper
from data import TestData

@allure.suite("Тестирование создания пользователя")
class TestCreateUser:
    
    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user_success(self):
        payload = UserHelper.generate_user_payload()
        response = requests.post(TestData.CREATE_USER_URL, json=payload)
        
        assert response.status_code == 200
        assert response.json().get("success") is True
        
        token = response.json().get("accessToken")
        if token:
            headers = {"Authorization": token}
            requests.delete(TestData.USER_URL, headers=headers)

    @allure.title("Ошибка при создании уже существующего пользователя")
    def test_create_existing_user_error(self, create_user):
        _, payload = create_user
        response = requests.post(TestData.CREATE_USER_URL, json=payload)
        
        assert response.status_code == 403
        assert response.json().get("success") is False
        assert response.json().get("message") == "User already exists"

    @allure.title("Ошибка создания пользователя при отсутствии обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field_error(self, missing_field):
        payload = UserHelper.generate_user_payload()
        del payload[missing_field]
        
        response = requests.post(TestData.CREATE_USER_URL, json=payload)
        
        assert response.status_code == 403
        assert response.json().get("success") is False
        assert response.json().get("message") == "Email, password and name are required fields"
